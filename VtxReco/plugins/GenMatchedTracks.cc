#include "TTree.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "SoftDisplacedVertices/SoftDVDataFormats/interface/GenInfo.h"

struct gentkInfo
{
  double bs_x;
  double bs_y;
  double bs_z;
  double pv_x;
  double pv_y;
  double pv_z;
  std::vector<double> gen_pt;
  std::vector<double> gen_eta;
  std::vector<double> gen_phi;
  std::vector<double> gen_dxybs;
  std::vector<double> gen_dxybs_reco;
  std::vector<double> gen_dxypv;
  std::vector<double> gen_dxypv_reco;
  std::vector<double> gen_dzbs;
  std::vector<double> gen_dzpv;
  std::vector<double> gen_charge;
  std::vector<double> gen_vx;
  std::vector<double> gen_vy;
  std::vector<double> gen_vz;
  std::vector<bool> gen_match;
  std::vector<int> gen_llp_idx;
  std::vector<int> gen_tk_idx;
  std::vector<double> matched_track_vx;
  std::vector<double> matched_track_vy;
  std::vector<double> matched_track_vz;
  std::vector<double> matched_track_pt;
  std::vector<double> matched_track_pt_err;
  std::vector<double> matched_track_eta;
  std::vector<double> matched_track_phi;
  std::vector<double> matched_track_dxybs;
  std::vector<double> matched_track_dxypv;
  std::vector<double> matched_track_dxy_err;
  std::vector<double> matched_track_dzbs;
  std::vector<double> matched_track_dzpv;
  std::vector<double> matched_track_dz_err;
  std::vector<double> matched_track_dr;
  std::vector<double> matched_track_chi2;
  std::vector<double> matched_track_nhits;
  std::vector<double> matched_track_normchi2;
  std::vector<int> matched_track_n_gentk;
};


class GenMatchedTracks : public edm::EDProducer {
  typedef std::pair<double,std::vector<double>> Match; //the first element is chi2 and the second element is dr
  typedef std::pair<int, Match> MatchResult; //the first element is the index of matched track and the second element is Match

  public:
    explicit GenMatchedTracks(const edm::ParameterSet&);

  private:
    void produce(edm::Event&, const edm::EventSetup&) override;
    void initStructure();
    const edm::EDGetTokenT<std::vector<SoftDV::LLP>> llp_gen_token;
    const edm::EDGetTokenT<reco::TrackCollection> tracks_token;
    const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
    const edm::EDGetTokenT<reco::VertexCollection> primary_vertices_token;
    const bool histos;
    const bool debug;

    MatchResult matchtracks(const reco::GenParticle&, const edm::Handle<reco::TrackCollection>&, const SoftDV::Point& );
    Match matchchi2(const reco::GenParticle&, const reco::TrackRef&, const SoftDV::Point& );

    TTree *gentkTree;
    gentkInfo *gtInfo;

    TH1D* n_gentracks_LLP;
    TH1D* n_matched_tracks_LLP;
    TH1D* n_matched_tracks_gentrack;
    TH1D* tracks_pt;
    TH1D* tracks_eta;
    TH1D* tracks_phi;
    TH1D* tracks_dxy;
    TH1D* tracks_dxy_err;
    TH1D* tracks_dxy_sig;
    TH1D* tracks_dz;
    TH1D* tracks_dz_err;
    TH1D* tracks_dz_sig;
    TH1D* tracks_nhits;
    TH1D* tracks_normchi2;
    TH1D* sigmapt_ratio;
};

GenMatchedTracks::GenMatchedTracks(const edm::ParameterSet& cfg)
  : llp_gen_token(consumes<std::vector<SoftDV::LLP>>(cfg.getParameter<edm::InputTag>("llp_gen_token"))),
    tracks_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("tracks"))),
    beamspot_token(consumes<reco::BeamSpot>(cfg.getParameter<edm::InputTag>("beamspot"))),
    primary_vertices_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("primary_vertices"))),
    histos(cfg.getParameter<bool>("histos")),
    debug(cfg.getParameter<bool>("debug"))
{
  gtInfo = new gentkInfo;

  produces<std::vector<std::vector<reco::Track>>>();

  if (histos) {
    edm::Service<TFileService> fs;
    n_gentracks_LLP = fs->make<TH1D>("n_gentracks_LLP","n_gentracks_LLP",100,0,100);
    n_matched_tracks_LLP = fs->make<TH1D>("n_matched_tracks_LLP","n_matched_tracks_LLP",100,0,100);
    n_matched_tracks_gentrack = fs->make<TH1D>("n_matched_tracks_gentrack","n_matched_tracks_gentrack",100,0,100);
    tracks_pt = fs->make<TH1D>("tracks_pt","tracks_pt",250,0,50);
    tracks_eta = fs->make<TH1D>("tracks_eta","tracks_eta",50,-2.5,2.5);
    tracks_phi = fs->make<TH1D>("tracks_phi","tracks_phi",50,-3.15,3.15);
    tracks_dxy = fs->make<TH1D>("tracks_dxy","tracks_dxy",500,-0.2,0.2);
    tracks_dxy_err = fs->make<TH1D>("tracks_dxy_err","tracks_dxy_err",500,0,0.2);
    tracks_dxy_sig = fs->make<TH1D>("tracks_dxy_sig","tracks_dxy_sig",100,0,10);
    tracks_dz = fs->make<TH1D>("tracks_dz","tracks_dz",80,-20,20);
    tracks_dz_err = fs->make<TH1D>("tracks_dz_err","tracks_dz_err",100,0,1);
    tracks_dz_sig = fs->make<TH1D>("tracks_dz_sig","tracks_dz_sig",100,0,20);
    tracks_nhits = fs->make<TH1D>("tracks_nhits","tracks_nhits",20,0,20);
    tracks_normchi2 = fs->make<TH1D>("tracks_normchi2","tracks_normchi2",20,0,10);
    sigmapt_ratio = fs->make<TH1D>("sigmapt_ratio","sigmapt_ratio",50,0,0.1);

    gentkTree = fs->make<TTree>("gentkTree","gentkTree");
    gentkTree->Branch("bs_x",     &gtInfo->bs_x);
    gentkTree->Branch("bs_y",     &gtInfo->bs_y);
    gentkTree->Branch("bs_z",     &gtInfo->bs_z);
    gentkTree->Branch("pv_x",     &gtInfo->pv_x);
    gentkTree->Branch("pv_y",     &gtInfo->pv_y);
    gentkTree->Branch("pv_z",     &gtInfo->pv_z);
    gentkTree->Branch("gen_pt",   &gtInfo->gen_pt);
    gentkTree->Branch("gen_eta",  &gtInfo->gen_eta);
    gentkTree->Branch("gen_phi",  &gtInfo->gen_phi);
    gentkTree->Branch("gen_dxybs",  &gtInfo->gen_dxybs);
    gentkTree->Branch("gen_dxybs_reco",  &gtInfo->gen_dxybs_reco);
    gentkTree->Branch("gen_dxypv",  &gtInfo->gen_dxypv);
    gentkTree->Branch("gen_dxypv_reco",  &gtInfo->gen_dxypv_reco);
    gentkTree->Branch("gen_dzbs",   &gtInfo->gen_dzbs);
    gentkTree->Branch("gen_dzpv",   &gtInfo->gen_dzpv);
    gentkTree->Branch("gen_charge",&gtInfo->gen_charge);
    gentkTree->Branch("gen_vx",&gtInfo->gen_vx);
    gentkTree->Branch("gen_vy",&gtInfo->gen_vy);
    gentkTree->Branch("gen_vz",&gtInfo->gen_vz);
    gentkTree->Branch("gen_match", &gtInfo->gen_match);
    gentkTree->Branch("gen_llp_idx",&gtInfo->gen_llp_idx);
    gentkTree->Branch("gen_tk_idx",&gtInfo->gen_tk_idx);
    gentkTree->Branch("matched_track_vx",&gtInfo->matched_track_vx);
    gentkTree->Branch("matched_track_vy",&gtInfo->matched_track_vy);
    gentkTree->Branch("matched_track_vz",&gtInfo->matched_track_vz);
    gentkTree->Branch("matched_track_pt",   &gtInfo->matched_track_pt);
    gentkTree->Branch("matched_track_pt_err",   &gtInfo->matched_track_pt_err);
    gentkTree->Branch("matched_track_eta",  &gtInfo->matched_track_eta);
    gentkTree->Branch("matched_track_phi",  &gtInfo->matched_track_phi);
    gentkTree->Branch("matched_track_dxybs",  &gtInfo->matched_track_dxybs);
    gentkTree->Branch("matched_track_dxypv",  &gtInfo->matched_track_dxypv);
    gentkTree->Branch("matched_track_dxy_err",  &gtInfo->matched_track_dxy_err);
    gentkTree->Branch("matched_track_dzbs",       &gtInfo->matched_track_dzbs);
    gentkTree->Branch("matched_track_dzpv",       &gtInfo->matched_track_dzpv);
    gentkTree->Branch("matched_track_dz_err",   &gtInfo->matched_track_dz_err);
    gentkTree->Branch("matched_track_dr",   &gtInfo->matched_track_dr);
    gentkTree->Branch("matched_track_chi2",   &gtInfo->matched_track_chi2);
    gentkTree->Branch("matched_track_nhits",   &gtInfo->matched_track_nhits);
    gentkTree->Branch("matched_track_normchi2",   &gtInfo->matched_track_normchi2);
    gentkTree->Branch("matched_track_n_gentk",  &gtInfo->matched_track_n_gentk);
  }
}

void GenMatchedTracks::produce(edm::Event& event, const edm::EventSetup& setup) {

  initStructure();

  std::unique_ptr<std::vector<std::vector<reco::Track>>> matched_tracks(new std::vector<std::vector<reco::Track>>);

  edm::Handle<std::vector<SoftDV::LLP>> genllps;
  event.getByToken(llp_gen_token, genllps);

  edm::Handle<reco::TrackCollection> tracks;
  event.getByToken(tracks_token, tracks);

  edm::Handle<reco::BeamSpot> beamspot;
  event.getByToken(beamspot_token, beamspot);

  edm::Handle<reco::VertexCollection> primary_vertices;
  event.getByToken(primary_vertices_token, primary_vertices);
  const reco::Vertex* primary_vertex = &primary_vertices->at(0);
  if (primary_vertices->size()==0)
    throw cms::Exception("GenMatchedTracks") << "No Primary Vertices available!";

  gtInfo->bs_x = beamspot->position().x();
  gtInfo->bs_y = beamspot->position().y();
  gtInfo->bs_z = beamspot->position().z();
  gtInfo->pv_x = primary_vertex->position().x();
  gtInfo->pv_y = primary_vertex->position().y();
  gtInfo->pv_z = primary_vertex->position().z();
  std::vector<int> track_match(tracks->size(),0);

  for (size_t illp=0; illp<genllps->size(); ++illp){
    const auto& llp = genllps->at(illp);
    if (!llp.valid()) continue;
    std::vector<reco::Track> matched_tks;
    const auto gen_tks = llp.getGenTracks();
    if (histos) n_gentracks_LLP->Fill(gen_tks.size());
    if (debug){
      std::cout << "Processing LLP " << illp << " with gen tracks " << gen_tks.size() << " at x " << llp.decay_point().x() << " y " << llp.decay_point().y() << " z " << llp.decay_point().z() << std::endl;
    }
    int n_matched_tracks = 0;
    for (const auto& gtk:gen_tks){
      if (debug) {
        std::cout << "LLP gen track pt " << gtk.pt() << " eta " << gtk.eta() << " phi " << gtk.phi() << std::endl;
      }
      const auto matchres = matchtracks(gtk, tracks, primary_vertex->position());
      gtInfo->gen_pt.push_back(gtk.pt());
      gtInfo->gen_eta.push_back(gtk.eta());
      gtInfo->gen_phi.push_back(gtk.phi());
      gtInfo->gen_dxybs.push_back(gen_dxy(gtk,beamspot->position()));
      gtInfo->gen_dxybs_reco.push_back(gen_dxy_reco(gtk,beamspot->position()));
      gtInfo->gen_dxypv.push_back(gen_dxy(gtk,primary_vertex->position()));
      gtInfo->gen_dxypv_reco.push_back(gen_dxy_reco(gtk,primary_vertex->position()));
      gtInfo->gen_dzbs.push_back(gen_dz(gtk,beamspot->position()));
      gtInfo->gen_charge.push_back(gtk.charge());
      gtInfo->gen_vx.push_back(gtk.vx());
      gtInfo->gen_vy.push_back(gtk.vy());
      gtInfo->gen_vz.push_back(gtk.vz());
      gtInfo->gen_llp_idx.push_back(illp);
      gtInfo->gen_tk_idx.push_back(matchres.first);
      if (matchres.first!=-1){
        gtInfo->gen_match.push_back(true);
        n_matched_tracks += 1;
        track_match[matchres.first] += 1;
        reco::TrackRef tk(tracks, matchres.first);

        if (debug) {
          std::cout << "  Matched track pt " << tk->pt() << " eta " << tk->eta() << " phi " << tk->phi() << " dxy " << tk->dxy(*beamspot) << " dz " << tk->dz((*beamspot).position()) << ". And dr " << matchres.second.second[0] << std::endl;
        }

        gtInfo->matched_track_vx.push_back(tk->vx());
        gtInfo->matched_track_vy.push_back(tk->vy());
        gtInfo->matched_track_vz.push_back(tk->vz());
        gtInfo->matched_track_pt.push_back(tk->pt());
        gtInfo->matched_track_pt_err.push_back(tk->ptError());
        gtInfo->matched_track_eta.push_back(tk->eta());
        gtInfo->matched_track_phi.push_back(tk->phi());
        gtInfo->matched_track_dxybs.push_back(tk->dxy(*beamspot));
        gtInfo->matched_track_dxypv.push_back(tk->dxy(primary_vertex->position()));
        gtInfo->matched_track_dxy_err.push_back(tk->dxyError());
        gtInfo->matched_track_dzbs.push_back(tk->dz((*beamspot).position()));
        gtInfo->matched_track_dzpv.push_back(tk->dz(primary_vertex->position()));
        gtInfo->matched_track_dz_err.push_back(tk->dzError());
        gtInfo->matched_track_dr.push_back(matchres.second.second[0]);
        gtInfo->matched_track_chi2.push_back(matchres.second.first);
        gtInfo->matched_track_nhits.push_back(tk->hitPattern().numberOfValidHits());
        gtInfo->matched_track_normchi2.push_back(tk->normalizedChi2());

        matched_tks.push_back(*tk);
        if (histos) {
          tracks_pt->Fill(tk->pt());
          tracks_eta->Fill(tk->eta());
          tracks_phi->Fill(tk->phi());
          tracks_dxy->Fill(tk->dxy(*beamspot));
          tracks_dxy_err->Fill(tk->dxyError());
          tracks_dxy_sig->Fill(tk->dxy(*beamspot)/tk->dxyError());
          tracks_dz->Fill(tk->dz((*beamspot).position()));
          tracks_dz_err->Fill(tk->dzError());
          tracks_dz_sig->Fill(tk->dz((*beamspot).position())/tk->dzError());
          tracks_nhits->Fill(tk->hitPattern().numberOfValidHits());
          tracks_normchi2->Fill(tk->normalizedChi2());
          sigmapt_ratio->Fill(tk->ptError()/tk->pt());
        }
      }
      else {
        gtInfo->gen_match.push_back(false);
        gtInfo->matched_track_vx.push_back(-1);
        gtInfo->matched_track_vy.push_back(-1);
        gtInfo->matched_track_vz.push_back(-1);
        gtInfo->matched_track_pt.push_back(-1);
        gtInfo->matched_track_pt_err.push_back(-1);
        gtInfo->matched_track_eta.push_back(-1);
        gtInfo->matched_track_phi.push_back(-1);
        gtInfo->matched_track_dxybs.push_back(-1);
        gtInfo->matched_track_dxypv.push_back(-1);
        gtInfo->matched_track_dxy_err.push_back(-1);
        gtInfo->matched_track_dzbs.push_back(-1);
        gtInfo->matched_track_dzpv.push_back(-1);
        gtInfo->matched_track_dz_err.push_back(-1);
        gtInfo->matched_track_dr.push_back(-1);
        gtInfo->matched_track_chi2.push_back(-1);
        gtInfo->matched_track_nhits.push_back(-1);
        gtInfo->matched_track_normchi2.push_back(-1);
      }
    }
    if (histos)  n_matched_tracks_LLP->Fill(n_matched_tracks);
    matched_tracks->push_back(matched_tks);
  }
  if (histos){
    for(size_t i=0; i<tracks->size(); ++i){
      n_matched_tracks_gentrack->Fill(track_match[i]);
    }
  }
  for(size_t i=0; i<(gtInfo->gen_tk_idx).size(); ++i){
    if (gtInfo->gen_tk_idx[i]==-1)
      gtInfo->matched_track_n_gentk.push_back(0);
    else {
      gtInfo->matched_track_n_gentk.push_back(track_match[gtInfo->gen_tk_idx[i]]);
    }
  }

  gentkTree->Fill();
  event.put(std::move(matched_tracks));
}

GenMatchedTracks::MatchResult GenMatchedTracks::matchtracks(const reco::GenParticle& gtk, const edm::Handle<reco::TrackCollection>& tracks, const SoftDV::Point& refpoint) {
  Match min_match(999,std::vector<double>());
  int tk_idx = -1;
  for (size_t i=0; i<tracks->size(); ++i){
    reco::TrackRef tk(tracks, i);
    Match match = matchchi2(gtk,tk,refpoint);
    if (match.first<min_match.first && match.second[0]<0.2 && match.second[1]<3){
    //if (match.first<min_match.first && match.second[0]<0.2){
      min_match = match;
      tk_idx = i;
    }
  }
  return MatchResult(tk_idx,min_match);
}

GenMatchedTracks::Match GenMatchedTracks::matchchi2(const reco::GenParticle& gtk, const reco::TrackRef& rtk, const SoftDV::Point& refpoint) {

  //double dxy = gen_dxy_reco(gtk,refpoint);
  double dxy = gen_dxy(gtk,refpoint);
  double dz = gen_dz(gtk,refpoint);

  std::vector<double> a;
  a.push_back( ( fabs(rtk->dxy(refpoint)) - fabs(dxy) ) / rtk->dxyError() );
  a.push_back( ( rtk->dz(refpoint)- dz ) / (4*rtk->dzError()) );
  a.push_back( ( rtk->charge()/rtk->pt() - gtk.charge()/gtk.pt()) / (1.0/rtk->ptError()) );
  double dr = reco::deltaR(rtk->eta(), rtk->phi(), gtk.eta(), gtk.phi());
  a.push_back(dr/0.01);
  double asum = 0;
  for (double& xa:a){
    asum += xa*xa;
  }
  std::vector<double> m({dr,fabs( fabs(rtk->dxy(refpoint)) - fabs(dxy) ) / rtk->dxyError()});
  return std::pair<double,std::vector<double>>(0.25*asum,m);
}

void GenMatchedTracks::initStructure()
{
  gtInfo->bs_x = -1;
  gtInfo->bs_y = -1;
  gtInfo->bs_z = -1;
  gtInfo->pv_x = -1;
  gtInfo->pv_y = -1;
  gtInfo->pv_z = -1;
  gtInfo->gen_pt.clear();
  gtInfo->gen_eta.clear();
  gtInfo->gen_phi.clear();
  gtInfo->gen_dxybs.clear();
  gtInfo->gen_dxybs_reco.clear();
  gtInfo->gen_dxypv.clear();
  gtInfo->gen_dxypv_reco.clear();
  gtInfo->gen_dzbs.clear();
  gtInfo->gen_dzpv.clear();
  gtInfo->gen_charge.clear();
  gtInfo->gen_vx.clear();
  gtInfo->gen_vy.clear();
  gtInfo->gen_vz.clear();
  gtInfo->gen_match.clear();
  gtInfo->gen_llp_idx.clear();
  gtInfo->gen_tk_idx.clear();
  gtInfo->matched_track_vx.clear();
  gtInfo->matched_track_vy.clear();
  gtInfo->matched_track_vz.clear();
  gtInfo->matched_track_pt.clear();
  gtInfo->matched_track_pt_err.clear();
  gtInfo->matched_track_eta.clear();
  gtInfo->matched_track_phi.clear();
  gtInfo->matched_track_dxybs.clear();
  gtInfo->matched_track_dxypv.clear();
  gtInfo->matched_track_dxy_err.clear();
  gtInfo->matched_track_dzbs.clear();
  gtInfo->matched_track_dzpv.clear();
  gtInfo->matched_track_dz_err.clear();
  gtInfo->matched_track_dr.clear();
  gtInfo->matched_track_chi2.clear();
  gtInfo->matched_track_nhits.clear();
  gtInfo->matched_track_normchi2.clear();
  gtInfo->matched_track_n_gentk.clear();
}

DEFINE_FWK_MODULE(GenMatchedTracks);
