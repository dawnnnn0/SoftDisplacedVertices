// This module runs trained Particle Transformer ONNX model and produces
// the output score that predicts whether a vertex is LLP vertex or not
//
// FIXME: This module does not work with the current CMSSW version becuase 
// the ONNXRunTime is not compatible with the Partile Transformer ONNX model
// 

#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"

#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/NanoAOD/interface/FlatTable.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Math/interface/deltaPhi.h"

#include "PhysicsTools/ONNXRuntime/interface/ONNXRuntime.h"


using namespace cms::Ort;

class VtxMLTableProducer : public edm::stream::EDProducer<edm::GlobalCache<ONNXRuntime>> {
  public:
    explicit VtxMLTableProducer(const edm::ParameterSet &, const ONNXRuntime *);

    static std::unique_ptr<ONNXRuntime> initializeGlobalCache(const edm::ParameterSet &);
    static void globalEndJob(const ONNXRuntime *);

  private:
    void beginJob();
    void produce(edm::Event&, const edm::EventSetup&);
    void endJob();
    std::vector<float> makeinput(std::map<std::string, std::vector<float> > inputInfo, std::vector<std::string> var_names, int n_pf, std::map<std::string, std::pair<float, float>> norm_params, std::string paddingmode, float paddingconst);

    const edm::EDGetTokenT<reco::VertexCollection> primary_vertex_token;
    const edm::EDGetTokenT<reco::VertexCollection> vtx_token;
    const edm::EDGetTokenT<reco::TrackCollection> tk_token;

    //std::vector<std::string> input_names_;
    //std::vector<std::vector<int64_t>> input_shapes_;

    FloatArrays inputData_;
};

VtxMLTableProducer::VtxMLTableProducer(const edm::ParameterSet &iConfig, const ONNXRuntime *cache)
  : primary_vertex_token(consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("primary_vertex_token"))),
    vtx_token(consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("vtx_token"))),
    tk_token(consumes<reco::TrackCollection>(iConfig.getParameter<edm::InputTag>("tk_token"))){
    //input_names_(iConfig.getParameter<std::vector<std::string>>("input_names")),
    //input_shapes_()
    //produces<nanoaod::FlatTable>("SDVSecVtx");
}

std::unique_ptr<ONNXRuntime> VtxMLTableProducer::initializeGlobalCache(const edm::ParameterSet &iConfig) {
  return std::make_unique<ONNXRuntime>(iConfig.getParameter<edm::FileInPath>("model_path").fullPath());
}

void VtxMLTableProducer::globalEndJob(const ONNXRuntime *cache) {}

void VtxMLTableProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {

  edm::Handle<reco::VertexCollection> primary_vertices;
  iEvent.getByToken(primary_vertex_token, primary_vertices);
  const reco::Vertex* primary_vertex = 0;
  if (primary_vertices->size())
    primary_vertex = &primary_vertices->at(0);

  edm::Handle<reco::VertexCollection> vertices;
  iEvent.getByToken(vtx_token, vertices);

  edm::Handle<reco::TrackCollection> tracks;
  iEvent.getByToken(tk_token, tracks);

  const int n_pfs = 128;
  const int n_pfvectors = 4;
  const int n_pffeature = 14;
  const int n_pfmasks = 1;
  const double tk_pi_mass = 0.13957018;

  std::vector<std::string> pffeature_names = {"tk_pt_log","tk_E_log","tk_logptrel","tk_logerel","tk_deltaR","tk_nvalidhits","tk_normchi2","tk_pterrratio","tk_dxy_th","tk_dxyerr","tk_dz_th","tk_dzerr","tk_deta_Lvtx","tk_dphi_Lvtx"};
  std::vector<std::string> pfvector_names = {"tk_px","tk_py","tk_pz","tk_E"};
  std::vector<std::string> pfmask_names = {"tk_mask"};

  std::map<std::string, std::pair<float, float>> norm_params;
  norm_params["tk_pt_log"] = std::pair<float, float>(1.7,0.7);
  norm_params["tk_E_log"] = std::pair<float, float>(2.0,0.7);
  norm_params["tk_logptrel"] = std::pair<float, float>(-4.7,0.7);
  norm_params["tk_logerel"] = std::pair<float, float>(-4.7,0.7);
  norm_params["tk_deltaR"] = std::pair<float, float>(0.2,4.0);
  norm_params["tk_nvalidhits"] = std::pair<float, float>(15,0.25);

  std::vector<float> pffeatures_all;
  std::vector<float> pfvectors_all;
  std::vector<float> pfmasks_all;

  for(size_t ivtx=0; ivtx<vertices->size(); ++ivtx) {
    const reco::Vertex& vtx = vertices->at(ivtx);
    inputData_.clear();
    std::map<std::string, std::vector<float> > inputInfo;
    math::XYZVector l_vector = vtx.position() - primary_vertex->position();
    float vtx_E = vtx.p4().E(); 
    float vtx_pt = vtx.p4().pt();
    for (auto v_tk = vtx.tracks_begin(), vtke = vtx.tracks_end(); v_tk != vtke; ++v_tk){
      float pt = (*v_tk)->pt();
      ROOT::Math::LorentzVector<ROOT::Math::PxPyPzM4D<double> > vec;
      vec.SetPx((*v_tk)->px());
      vec.SetPy((*v_tk)->py());
      vec.SetPz((*v_tk)->pz());
      vec.SetM(tk_pi_mass);
      float dphi_Lvtx = reco::deltaPhi((**v_tk),l_vector);
      float deta_Lvtx = fabs((**v_tk).eta()-l_vector.eta());
      inputInfo["tk_mask"].push_back(1);
      inputInfo["tk_px"].push_back((*v_tk)->px());
      inputInfo["tk_py"].push_back((*v_tk)->py());
      inputInfo["tk_pz"].push_back((*v_tk)->pz());
      inputInfo["tk_E_log"].push_back(log(vec.E()));
      inputInfo["tk_E"].push_back(vec.E());
      inputInfo["tk_logptrel"].push_back(log(pt/vtx_pt));
      inputInfo["tk_pt_log"].push_back(pt);
      inputInfo["tk_logerel"].push_back(log(vec.E()/vtx_E));
      inputInfo["tk_deltaR"].push_back(std::hypot(deta_Lvtx, dphi_Lvtx));
      inputInfo["tk_nvalidhits"].push_back((*v_tk)->numberOfValidHits());
      inputInfo["tk_normchi2"].push_back((*v_tk)->normalizedChi2());
      inputInfo["tk_pterrratio"].push_back((*v_tk)->ptError()/pt);
      inputInfo["tk_dxy_th"].push_back(std::tanh((*v_tk)->dxy(primary_vertex->position())));
      inputInfo["tk_dxyerr"].push_back((*v_tk)->dxyError(primary_vertex->position(), primary_vertex->covariance()));
      inputInfo["tk_dz_th"].push_back(std::tanh((*v_tk)->dz(primary_vertex->position())));
      inputInfo["tk_dzerr"].push_back((*v_tk)->dzError());
      inputInfo["tk_deta_Lvtx"].push_back(deta_Lvtx);
      inputInfo["tk_dphi_Lvtx"].push_back(dphi_Lvtx);
    }

    std::vector<float> pffeature_values = makeinput(inputInfo, pffeature_names, n_pfs, norm_params, std::string("wrap"), 0);
    std::vector<float> pfvec_values = makeinput(inputInfo, pfvector_names, n_pfs, norm_params, std::string("wrap"), 0);
    std::vector<float> pfmask_values = makeinput(inputInfo, pfmask_names, n_pfs, norm_params, std::string("constant"), 0);

    // flattern the vectors
    for (auto& e : pffeature_values){
      pffeatures_all.push_back(e);
    }
    for (auto& e : pfvec_values){
      pfvectors_all.push_back(e);
    }
    for (auto& e : pfmask_values){
      pfmasks_all.push_back(e);
    }


    //int ntk = inputInfo["tk_mask"].size();

    //std::vector<std::vector<float>> pffeature_values;
    //for(const auto& vn : pffeature_names) {
    //  std::vector<float> pffeature_values_i;
    //  for (int i=0; i<n_pfs; ++i){
    //    int itk = i % ntk;
    //    float var = inputInfo[vn][itk];
    //    if (norm_params.find(vn)!=norm_params.end()){
    //      var = (var-norm_params[vn].first) / norm_params[vn].second // normalize the variable (v-center)/sigma
    //    }
    //    pffeature_values_i.push_back(var);
    //  }
    //  pffeature_values.push_back(pffeature_values_i);
    //}

  }

  std::vector<std::vector<float>> input_data = {pffeatures_all, pfvectors_all, pfmasks_all};
  std::vector<std::string> names = {"pf_features", "pf_vectors", "pf_mask"};
  std::vector<float> outputs = globalCache()->run(names, input_data, {})[0];
  std::cout << "ML output: ";
  for(auto& o:outputs){
    std::cout << o << ", ";
  }
  std::cout << std::endl;
}

std::vector<float> VtxMLTableProducer::makeinput(std::map<std::string, std::vector<float> > inputInfo, std::vector<std::string> var_names, int n_pf, std::map<std::string, std::pair<float, float>> norm_params, std::string paddingmode, float paddingconst){

    int ntk = inputInfo["tk_mask"].size();

    std::vector<float> vars_values;
    for (int i=0; i<n_pf; ++i){
      for(const auto& vn : var_names) {
          int itk = i % ntk;
          float var = inputInfo[vn][itk];
          if (norm_params.find(vn)!=norm_params.end()){
            var = (var-norm_params[vn].first) / norm_params[vn].second; // normalize the variable (v-center)/sigma
          }
          if (paddingmode=="constant" && i>ntk-1){
            var = paddingconst;
          }
          vars_values.push_back(var);
      }
    }

    //std::vector<std::vector<float>> vars_values;
    //for(const auto& vn : var_names) {
    //  std::vector<float> vars_values_i;
    //  for (int i=0; i<n_pf; ++i){
    //      int itk = i % ntk;
    //      float var = inputInfo[vn][itk];
    //      if (norm_params.find(vn)!=norm_params.end()){
    //        var = (var-norm_params[vn].first) / norm_params[vn].second; // normalize the variable (v-center)/sigma
    //      }
    //      if (paddingmode=="constant" && i>ntk-1){
    //        var = paddingconst;
    //      }
    //      vars_values_i.push_back(var);
    //  }
    //  vars_values.push_back(vars_values_i);
    //}
    return vars_values;
}

DEFINE_FWK_MODULE(VtxMLTableProducer);
