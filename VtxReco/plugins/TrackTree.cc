#include "TTree.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/METReco/interface/METFwd.h"
#include "DataFormats/METReco/interface/PFMET.h"
#include "DataFormats/METReco/interface/PFMETFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "RecoVertex/VertexTools/interface/VertexDistance3D.h"
#include "RecoVertex/VertexTools/interface/VertexDistanceXY.h"
#include "SoftDisplacedVertices/SoftDVDataFormats/interface/GenInfo.h"

struct trackInfo
{
  std::vector<double> track_vx;
  std::vector<double> track_vy;
  std::vector<double> track_vz;
  std::vector<double> track_pt;
  std::vector<double> track_pt_err;
  std::vector<double> track_eta;
  std::vector<double> track_phi;
  std::vector<double> track_dxybs;
  std::vector<double> track_dxypv;
  std::vector<double> track_dxy_err;
  std::vector<double> track_dzbs;
  std::vector<double> track_dzpv;
  std::vector<double> track_dz_err;
  std::vector<double> track_nhits;
  std::vector<double> track_nlayers;
  std::vector<double> track_normchi2;
  std::vector<double> track_dphimet;
  std::vector<double> track_dphijet;
  std::vector<double> track_drjet;
};

class TrackTree : public edm::EDAnalyzer {
  public:
    explicit TrackTree(const edm::ParameterSet&);
    void analyze(const edm::Event&, const edm::EventSetup&);

  private:
    virtual void beginJob() override;
    virtual void endJob() override;
    void initEventStructure();
    
    const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
    const edm::EDGetTokenT<reco::VertexCollection> primary_vertex_token;
    const edm::EDGetTokenT<reco::TrackCollection> tracks_token;
    const edm::EDGetTokenT<reco::PFJetCollection> jet_token;
    const edm::EDGetTokenT<reco::PFMETCollection> met_token;
    
    bool debug;

    TTree *trackTree;
    trackInfo *tkInfo;

    VertexDistanceXY distcalc_2d;
    VertexDistance3D distcalc_3d;
};

TrackTree::TrackTree(const edm::ParameterSet& cfg)
  : beamspot_token(consumes<reco::BeamSpot>(cfg.getParameter<edm::InputTag>("beamspot_token"))),
    primary_vertex_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("primary_vertex_token"))),
    tracks_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("tracks"))),
    jet_token(consumes<reco::PFJetCollection>(cfg.getParameter<edm::InputTag>("jet_token"))),
    met_token(consumes<reco::PFMETCollection>(cfg.getParameter<edm::InputTag>("met_token")))
{
  tkInfo = new trackInfo;
}

void TrackTree::analyze(const edm::Event& event, const edm::EventSetup&) {
  initEventStructure();

  edm::Handle<reco::BeamSpot> beamspot;
  event.getByToken(beamspot_token, beamspot);

  const reco::Vertex fake_bs_vtx(beamspot->position(), beamspot->covariance3D());

  edm::Handle<reco::VertexCollection> primary_vertices;
  event.getByToken(primary_vertex_token, primary_vertices);
  const reco::Vertex* primary_vertex = &primary_vertices->at(0);
  if (primary_vertices->size()==0)
    throw cms::Exception("TrackTree") << "No Primary Vertices available!";

  edm::Handle<reco::TrackCollection> tracks;
  event.getByToken(tracks_token, tracks);

  edm::Handle<reco::PFJetCollection> jets;
  event.getByToken(jet_token, jets);

  edm::Handle<reco::PFMETCollection> mets;
  event.getByToken(met_token, mets);

  const auto& met = mets->at(0);

  int jet_leading_idx = -1;
  double jet_pt_max = -1;
  for(size_t ijet=0; ijet<jets->size(); ++ijet){
    const auto& jet = jets->at(ijet);
    if (jet.pt()>jet_pt_max) {
      jet_leading_idx = ijet;
      jet_pt_max = jet.pt();
    }
  }
  const auto& leading_jet = jets->at(jet_leading_idx);

  for (size_t i=0; i<tracks->size(); ++i){
    reco::TrackRef tk(tracks, i);
    
    if (fabs(tk->eta()) > 2.5)
      continue;

    tkInfo->track_vx.push_back(tk->vx());
    tkInfo->track_vy.push_back(tk->vy());
    tkInfo->track_vz.push_back(tk->vz());
    tkInfo->track_pt.push_back(tk->pt());
    tkInfo->track_pt_err.push_back(tk->ptError());
    tkInfo->track_eta.push_back(tk->eta());
    tkInfo->track_phi.push_back(tk->phi());
    tkInfo->track_dxybs.push_back(tk->dxy(*beamspot));
    tkInfo->track_dxypv.push_back(tk->dxy(primary_vertex->position()));
    tkInfo->track_dxy_err.push_back(tk->dxyError());
    tkInfo->track_dzbs.push_back(tk->dz((*beamspot).position()));
    tkInfo->track_dzpv.push_back(tk->dz(primary_vertex->position()));
    tkInfo->track_dz_err.push_back(tk->dzError());
    tkInfo->track_nhits.push_back(tk->hitPattern().numberOfValidHits());
    tkInfo->track_nlayers.push_back(tk->hitPattern().trackerLayersWithMeasurement());
    tkInfo->track_normchi2.push_back(tk->normalizedChi2());
    tkInfo->track_dphimet.push_back(reco::deltaPhi(tk->phi(), met.phi()));
    tkInfo->track_dphijet.push_back(reco::deltaPhi(tk->phi(), leading_jet.phi()));
    tkInfo->track_drjet.push_back(reco::deltaR(tk->eta(),tk->phi(),leading_jet.eta(),leading_jet.phi()));
  }

  trackTree->Fill();

}

void TrackTree::beginJob()
{
  edm::Service<TFileService> fs;
  trackTree = fs->make<TTree>( "tree_tks", "tree_tks" );

  trackTree->Branch("track_vx",       &tkInfo->track_vx);
  trackTree->Branch("track_vy",       &tkInfo->track_vy);
  trackTree->Branch("track_vz",       &tkInfo->track_vz);
  trackTree->Branch("track_pt",       &tkInfo->track_pt);
  trackTree->Branch("track_pt_err",   &tkInfo->track_pt_err);
  trackTree->Branch("track_eta",      &tkInfo->track_eta);
  trackTree->Branch("track_phi",      &tkInfo->track_phi);
  trackTree->Branch("track_dxybs",    &tkInfo->track_dxybs);
  trackTree->Branch("track_dxypv",    &tkInfo->track_dxypv);
  trackTree->Branch("track_dxy_err",  &tkInfo->track_dxy_err);
  trackTree->Branch("track_dzbs",     &tkInfo->track_dzbs);
  trackTree->Branch("track_dzpv",     &tkInfo->track_dzpv);
  trackTree->Branch("track_dz_err",   &tkInfo->track_dz_err);
  trackTree->Branch("track_nhits",    &tkInfo->track_nhits);
  trackTree->Branch("track_nlayers",  &tkInfo->track_nlayers);
  trackTree->Branch("track_normchi2", &tkInfo->track_normchi2);
  trackTree->Branch("track_dphimet",  &tkInfo->track_dphimet);
  trackTree->Branch("track_dphijet",  &tkInfo->track_dphijet);
  trackTree->Branch("track_drjet",    &tkInfo->track_drjet);

}

void TrackTree::endJob()
{}

void TrackTree::initEventStructure()
{
  tkInfo->track_vx.clear();
  tkInfo->track_vy.clear();
  tkInfo->track_vz.clear();
  tkInfo->track_pt.clear();
  tkInfo->track_pt_err.clear();
  tkInfo->track_eta.clear();
  tkInfo->track_phi.clear();
  tkInfo->track_dxybs.clear();
  tkInfo->track_dxypv.clear();
  tkInfo->track_dxy_err.clear();
  tkInfo->track_dzbs.clear();
  tkInfo->track_dzpv.clear();
  tkInfo->track_dz_err.clear();
  tkInfo->track_nhits.clear();
  tkInfo->track_nlayers.clear();
  tkInfo->track_normchi2.clear();
  tkInfo->track_dphimet.clear();
  tkInfo->track_dphijet.clear();
  tkInfo->track_drjet.clear();
}

DEFINE_FWK_MODULE(TrackTree);
