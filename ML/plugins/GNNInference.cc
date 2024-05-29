#include <memory>
#include <vector>
#include <iostream>

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "SoftDisplacedVertices/SoftDVDataFormats/interface/PFIsolation.h"

#include "PhysicsTools/ONNXRuntime/interface/ONNXRuntime.h"

using namespace cms::Ort;
typedef std::vector<std::unique_ptr<ONNXRuntime>> NNArray;

class GNNInference : public edm::stream::EDProducer<edm::GlobalCache<NNArray>> {
  public:
    explicit GNNInference(const edm::ParameterSet &, const NNArray *);
    
    static std::unique_ptr<NNArray> initializeGlobalCache(const edm::ParameterSet &);
    static void globalEndJob(const NNArray *);

  private:
    void beginJob();
    void produce(edm::Event&, const edm::EventSetup&) override;
    void endJob();

    float edge_dist(std::vector<float> v1, std::vector<float> v2);
    std::vector<float> track_input(reco::TrackRef tk, const reco::Vertex* pv, SoftDV::PFIsolation isoDR03);

    std::vector<std::string> input_names_emb_;
    std::vector<std::string> input_names_gnn_;
    std::vector<std::vector<int64_t>> input_shapes_;
    const edm::EDGetTokenT<reco::VertexCollection> primary_vertex_token;
    const edm::EDGetTokenT<reco::TrackCollection> tracks_token;
    edm::EDGetTokenT<std::vector<SoftDV::PFIsolation>> isoDR03Token_;
    //FloatArrays data_; // each stream hosts its own data
    //
    float edge_dist_cut_;
    float edge_gnn_cut_;
};

GNNInference::GNNInference(const edm::ParameterSet &iConfig, const NNArray *cache)
  : input_names_emb_(iConfig.getParameter<std::vector<std::string>>("input_names_emb")),
    input_names_gnn_(iConfig.getParameter<std::vector<std::string>>("input_names_gnn")),
    input_shapes_(),
    primary_vertex_token(consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("primary_vertex_token"))),
    tracks_token(consumes<reco::TrackCollection>(iConfig.getParameter<edm::InputTag>("tracks"))),
    isoDR03Token_(consumes<std::vector<SoftDV::PFIsolation>>(iConfig.getParameter<edm::InputTag>("isoDR03"))),
    edge_dist_cut_(iConfig.getParameter<float>("edge_dist_cut")),
    edge_gnn_cut_(iConfig.getParameter<float>("edge_gnn_cut")){
    //data_.emplace_back(10,0);
    produces<std::vector<std::vector<reco::Track>>>();
    }

std::unique_ptr<NNArray> GNNInference::initializeGlobalCache(const edm::ParameterSet &iConfig) {
  //ONNXRuntime* EMB = new ONNXRuntime(iConfig.getParameter<edm::FileInPath>("EMB_model_path").fullPath());
  //ONNXRuntime* GNN = new ONNXRuntime(iConfig.getParameter<edm::FileInPath>("GNN_model_path").fullPath());
  std::unique_ptr<NNArray> NNs = std::make_unique<NNArray>();
  NNs->push_back(std::make_unique<ONNXRuntime>(iConfig.getParameter<edm::FileInPath>("EMB_model_path").fullPath()));
  NNs->push_back(std::make_unique<ONNXRuntime>(iConfig.getParameter<edm::FileInPath>("GNN_model_path").fullPath()));
  return NNs;
}

void GNNInference::globalEndJob(const NNArray *cache) {}

void GNNInference::produce(edm::Event &iEvent, const edm::EventSetup &iSetup) {

  std::unique_ptr<std::vector<std::vector<reco::Track>>> results(new std::vector<std::vector<reco::Track>>);
  //std::unique_ptr<std::vector<std::vector<float>>> results (new std::vector<std::vector<float>>);
  //
  edm::Handle<reco::TrackCollection> tracks;
  iEvent.getByToken(tracks_token, tracks);

  edm::Handle<reco::VertexCollection> primary_vertices;
  iEvent.getByToken(primary_vertex_token, primary_vertices);
  const reco::Vertex* primary_vertex = &primary_vertices->at(0);
  if (primary_vertices->size()==0)
    throw cms::Exception("GNNInterface") << "No Primary Vertices available!";

  edm::Handle<std::vector<SoftDV::PFIsolation>> tracks_isoDR03;
  iEvent.getByToken(isoDR03Token_, tracks_isoDR03);
  if (tracks->size() != tracks_isoDR03->size())
    throw cms::Exception("GNNInference") << "Tracks mismatch with track IsoDR03!";

  int ntks = tracks->size();
  int n_features = 0;
  FloatArrays inputdata;
  std::vector<float> tks_vars;
  for (int i=0; i<ntks; ++i){
    SoftDV::PFIsolation isoDR03 = (*tracks_isoDR03)[i];
    reco::TrackRef tk(tracks, i);
    std::vector<float> tk_vars = track_input(tk,primary_vertex,isoDR03);
    n_features = tk_vars.size();
    tks_vars.insert(tks_vars.end(),tk_vars.begin(),tk_vars.end());
  }
  inputdata.push_back(tks_vars);

  std::vector<std::vector<int64_t>> tk_shape = {{ntks,n_features}};

  std::vector<float> emb = globalCache()->at(0)->run(input_names_emb_, inputdata, tk_shape, {}, ntks)[0];

  std::vector<int> sender_idx;
  std::vector<int> receiver_idx;
  std::vector<float> distance;

  for (int i=0;i<ntks;++i){
    for (int j=0;j<ntks;++j){
      if (i==j) continue;
      std::vector<float> emb_i(emb.begin()+i*16,emb.begin()+(i+1)*16);
      std::vector<float> emb_j(emb.begin()+j*16,emb.begin()+(j+1)*16);
      float d2 = edge_dist(emb_i,emb_j);
      if (d2<999){ // FIXME: the cut value on d2 should be revisited
        sender_idx.push_back(i);
        receiver_idx.push_back(j);
        distance.push_back(d2);
      }
    }
  }

  FloatArrays input_GNN;
  std::vector<std::vector<int64_t>> input_shape_GNN;
  input_GNN.push_back(tks_vars);
  input_shape_GNN.push_back({1,ntks,n_features});
  std::vector<float> edge_idx;
  int64_t n_edges = sender_idx.size();
  edge_idx.insert(edge_idx.end(),sender_idx.begin(),sender_idx.end());
  edge_idx.insert(edge_idx.end(),receiver_idx.begin(),receiver_idx.end());
  input_GNN.push_back(edge_idx);
  input_shape_GNN.push_back({1,2,n_edges});

  std::vector<float> gnn = globalCache()->at(1)->run(input_names_gnn_, input_GNN, input_shape_GNN, {}, 1)[0];

  if (gnn.size() != distance.size()) 
    throw cms::Exception("GNNInterface") << "Embedding distance and GNN prediction doesn't match!";

  // Select edges based on distance and gnn score
  std::vector<std::pair<int,int>> edges;
  for (size_t i=0; i<n_edges; ++i) {
    if ( (distance[i] > edge_dist_cut_) || (gnn[i] < edge_gnn_cut_) )
      continue;
    edges.push_back(std::pair<int,int>({sender_idx[i],receiver_idx[i]}));
  }

  // Remove single directed edges
  std::vector<std::pair<int,int>> edges_bi;
  for (size_t i=0; i<edges.size(); ++i) {
    if (edges[i].first>edges[i].second)
      continue;
    std::pair<int,int> inverse_edge({edges[i].second,edges[i].first});
    if (std::find(edges.begin(),edges.end(),inverse_edge) != edges.end()) {
      edges_bi.push_back(edges[i]);
    }
  }


  iEvent.put(std::move(results));
}

float GNNInference::edge_dist(std::vector<float> v1, std::vector<float> v2) {
  if (v1.size() != v2.size()){
    throw cms::Exception("GNNInference::edge_dist") << "Sizes of v1 and v2 do not match!";
  }
  float d2 = 0;
  for (size_t i=0; i<v1.size(); ++i){
    d2 += pow(v1[i]-v2[i],2);
  }
  return d2;
}

std::vector<float> GNNInference::track_input(reco::TrackRef tk, const reco::Vertex* pv, SoftDV::PFIsolation isoDR03) {
  float pt = tk->pt();
  float eta = tk->eta();
  float phi = tk->phi();
  float dxy = tk->dxy(pv->position());
  float dxyError = tk->dxyError(pv->position(), pv->covariance());
  float dz = tk->dz(pv->position());
  float dzError = tk->dzError();
  float ptError = tk->ptError();
  float normchi2 = tk->normalizedChi2();
  float nvalidhits = tk->numberOfValidHits();
  float pfRelIso03_all = (isoDR03.chargedHadronIso() +
                            std::max<double>(isoDR03.neutralHadronIso() +
                                             isoDR03.photonIso() -
                                             isoDR03.puChargedHadronIso()/2,0.0))
                          / tk->pt();

  std::vector<float> tk_vars = {pt,eta,phi,dxy,dxyError,dz,dzError,pfRelIso03_all,ptError,normchi2,nvalidhits};
  return tk_vars;
}

DEFINE_FWK_MODULE(GNNInference);
