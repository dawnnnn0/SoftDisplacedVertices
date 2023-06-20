#include "TTree.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/METReco/interface/METFwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "RecoVertex/VertexTools/interface/VertexDistance3D.h"
#include "RecoVertex/VertexTools/interface/VertexDistanceXY.h"

struct eventInfo
{
  int n_vtx;
  std::vector<double> jet_pt;
  std::vector<double> jet_eta;
  std::vector<double> jet_phi;
  double met_pt;
  double met_phi;
  std::vector<double> vtx_x;
  std::vector<double> vtx_y;
  std::vector<double> vtx_z;
  std::vector<double> vtx_ntracks;
  std::vector<double> vtx_ndof;
  std::vector<double> vtx_lxy;
  std::vector<double> vtx_lxy_err;
  std::vector<double> vtx_dphi_jet1;
  std::vector<double> vtx_dphi_met;
  std::vector<double> vtx_acollinearity;
};

class EventHistos : public edm::EDAnalyzer {
  public:
    explicit EventHistos(const edm::ParameterSet&);
    void analyze(const edm::Event&, const edm::EventSetup&);

  private:
    virtual void beginJob() override;
    virtual void endJob() override;
    void initEventStructure();
    
    const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
    const edm::EDGetTokenT<reco::PFJetCollection> jet_token;
    const edm::EDGetTokenT<reco::METCollection> met_token;
    const edm::EDGetTokenT<reco::VertexCollection> vtx_token;

    TTree *eventTree;
    eventInfo *evInfo;

    VertexDistanceXY distcalc_2d;
    VertexDistance3D distcalc_3d;
};

EventHistos::EventHistos(const edm::ParameterSet& cfg)
  : beamspot_token(consumes<reco::BeamSpot>(cfg.getParameter<edm::InputTag>("beamspot_token"))),
    jet_token(consumes<reco::PFJetCollection>(cfg.getParameter<edm::InputTag>("jet_token"))),
    met_token(consumes<reco::METCollection>(cfg.getParameter<edm::InputTag>("met_token"))),
    vtx_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("vtx_token")))
{
  evInfo = new eventInfo;
}

void EventHistos::analyze(const edm::Event& event, const edm::EventSetup&) {
  initEventStructure();
  edm::Handle<reco::PFJetCollection> jets;
  event.getByToken(jet_token, jets);

  edm::Handle<reco::METCollection> mets;
  event.getByToken(met_token, mets);

  edm::Handle<reco::VertexCollection> vertices;
  event.getByToken(vtx_token, vertices);

  int jet_leading_idx = -1;
  double jet_pt_max = -1;
  for(size_t ijet=0; ijet<jets->size(); ++ijet){
    const reco::PFJet& jet = jets->at(ijet);
    evInfo->jet_pt.push_back(jet.pt());
    evInfo->jet_eta.push_back(jet.eta());
    evInfo->jet_phi.push_back(jet.phi());
    if (jet.pt()>jet_pt_max) {
      jet_leading_idx = ijet;
      jet_pt_max = jet.pt();
    }
  }

  const reco::MET& met = mets->at(0);
  evInfo->met_pt = met.pt();
  evInfo->met_phi = met.phi();

  edm::Handle<reco::BeamSpot> beamspot;
  event.getByToken(beamspot_token, beamspot);

  const reco::PFJet& leading_jet = jets->at(jet_leading_idx);
  const reco::Vertex fake_bs_vtx(beamspot->position(), beamspot->covariance3D());
  evInfo->n_vtx = vertices->size();
  for(size_t ivtx=0; ivtx<vertices->size(); ++ivtx) {
    const reco::Vertex& vtx = vertices->at(ivtx);
    math::XYZVector l_vector = vtx.position() - beamspot->position();
    const auto d = distcalc_2d.distance(vtx, fake_bs_vtx);

    evInfo->vtx_x.push_back(vtx.x());
    evInfo->vtx_y.push_back(vtx.y());
    evInfo->vtx_z.push_back(vtx.z());
    evInfo->vtx_ntracks.push_back(vtx.tracksSize());
    evInfo->vtx_ndof.push_back(vtx.normalizedChi2());
    evInfo->vtx_lxy.push_back(d.value());
    evInfo->vtx_lxy_err.push_back(d.error());
    evInfo->vtx_dphi_jet1.push_back(reco::deltaPhi(l_vector, leading_jet));
    evInfo->vtx_dphi_met.push_back(reco::deltaPhi(l_vector, met));
    evInfo->vtx_acollinearity.push_back(reco::deltaPhi(l_vector, vtx.p4()));
  }

}

void EventHistos::beginJob()
{
  edm::Service<TFileService> fs;
  eventTree = fs->make<TTree>( "tree_DV", "tree_DV" );

  eventTree->Branch("n_vtx",      &evInfo->n_vtx);
  eventTree->Branch("jet_pt",     &evInfo->jet_pt);
  eventTree->Branch("jet_eta",    &evInfo->jet_eta);
  eventTree->Branch("jet_phi",    &evInfo->jet_phi);
  eventTree->Branch("met_pt",     &evInfo->met_pt);
  eventTree->Branch("met_phi",    &evInfo->met_phi);
  eventTree->Branch("vtx_x",      &evInfo->vtx_x);
  eventTree->Branch("vtx_y",      &evInfo->vtx_y);
  eventTree->Branch("vtx_z",      &evInfo->vtx_z);
  eventTree->Branch("vtx_ntracks",&evInfo->vtx_ntracks);
  eventTree->Branch("vtx_ndof",   &evInfo->vtx_ndof);
  eventTree->Branch("vtx_lxy",    &evInfo->vtx_lxy);
  eventTree->Branch("vtx_lxy_err",&evInfo->vtx_lxy_err);
  eventTree->Branch("vtx_dphi_jet1", &evInfo->vtx_dphi_jet1);
  eventTree->Branch("vtx_dphi_met",  &evInfo->vtx_dphi_met);
  eventTree->Branch("vtx_acollinearity", &evInfo->vtx_acollinearity);

}

void EventHistos::endJob()
{}

void EventHistos::initEventStructure()
{
  evInfo->n_vtx = -1;
  evInfo->jet_pt.clear();
  evInfo->jet_eta.clear();
  evInfo->jet_phi.clear();
  evInfo->met_pt = -1;
  evInfo->met_phi = -1;
  evInfo->vtx_x.clear();
  evInfo->vtx_y.clear();
  evInfo->vtx_z.clear();
  evInfo->vtx_ntracks.clear();
  evInfo->vtx_ndof.clear();
  evInfo->vtx_lxy.clear();
  evInfo->vtx_lxy_err.clear();
  evInfo->vtx_dphi_jet1.clear();
  evInfo->vtx_dphi_met.clear();
  evInfo->vtx_acollinearity.clear();
}

DEFINE_FWK_MODULE(EventHistos);
