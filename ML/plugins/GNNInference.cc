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

    std::vector<std::string> input_names_emb_;
    std::vector<std::string> input_names_gnn_;
    std::vector<std::vector<int64_t>> input_shapes_;
    //FloatArrays data_; // each stream hosts its own data
};

GNNInference::GNNInference(const edm::ParameterSet &iConfig, const NNArray *cache)
  : input_names_emb_(iConfig.getParameter<std::vector<std::string>>("input_names_emb")),
    input_names_gnn_(iConfig.getParameter<std::vector<std::string>>("input_names_gnn")),
    input_shapes_() {
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

  int ntks = 10;
  int n_features = 11;
  FloatArrays inputdata;
  std::vector<float> tk_vars;
  for (int i=0; i<ntks; ++i){
    for (int j=0; j<n_features; ++j){
      tk_vars.push_back(float(i+0.1*j));
    }
  }
  inputdata.push_back(tk_vars);

  std::vector<std::vector<int64_t>> ishape = {{ntks,n_features}};

  std::vector<float> emb = globalCache()->at(0)->run(input_names_emb_, inputdata, ishape, {}, ntks)[0];

  std::cout << "EMB Output " << std::endl;
  for (auto &e : emb){
      std::cout << e << " ";
  }
  std::cout << std::endl;

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
  std::cout << "Edge built." << std::endl;

  FloatArrays input_GNN;
  std::vector<std::vector<int64_t>> input_shape_GNN;
  input_GNN.push_back(tk_vars);
  input_shape_GNN.push_back({1,ntks,n_features});
  std::vector<float> edge_idx;
  int64_t n_edges = sender_idx.size();
  edge_idx.insert(edge_idx.end(),sender_idx.begin(),sender_idx.end());
  edge_idx.insert(edge_idx.end(),receiver_idx.begin(),receiver_idx.end());
  //input_GNN.push_back(edge_idx);
  //input_shape_GNN.push_back({1,2,n_edges});
  input_GNN.push_back(distance);
  input_shape_GNN.push_back({1,n_edges});

  std::cout << "GNN input ready." << std::endl;
  std::cout << n_edges << std::endl;
  for (auto& e : input_GNN[1]){
    std::cout << e << " ";
  }
  std::cout << std::endl;
  FloatArrays gnn = globalCache()->at(1)->run(input_names_gnn_, input_GNN, input_shape_GNN, {}, 1);

  std::cout << "GNN Output " << std::endl;
  for (auto &e : gnn){
    std::cout << "size " << e.size() << std::endl;
    for(auto &ie : e){
      std::cout << ie << " ";
    }
    std::cout << std::endl;
  }
  std::cout << std::endl;

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

DEFINE_FWK_MODULE(GNNInference);
