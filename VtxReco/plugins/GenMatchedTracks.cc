#include "TTree.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
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
  std::vector<double> gen_pt;
  std::vector<double> gen_eta;
  std::vector<double> gen_phi;
  std::vector<double> gen_dxy;
  std::vector<double> gen_dz;
  std::vector<double> gen_charge;
  std::vector<bool> gen_match;
  std::vector<int> gen_llp_idx;
  std::vector<int> gen_tk_idx;
  std::vector<double> matched_track_pt;
  std::vector<double> matched_track_eta;
  std::vector<double> matched_track_phi;
  std::vector<double> matched_track_dxy;
  std::vector<double> matched_track_dxy_err;
  std::vector<double> matched_track_dz;
  std::vector<double> matched_track_dz_err;
  std::vector<int> matched_track_n_gentk;
};


class GenMatchedTracks : public edm::EDProducer {
  typedef std::pair<double,double> Match; //the first element is chi2 and the second element is dr
  typedef std::pair<int, Match> MatchResult; //the first element is the index of matched track and the second element is Match

  public:
    explicit GenMatchedTracks(const edm::ParameterSet&);

  private:
    void produce(edm::Event&, const edm::EventSetup&) override;
    void initStructure();
    const edm::EDGetTokenT<std::vector<SoftDV::LLP>> llp_gen_token;
    const edm::EDGetTokenT<reco::TrackCollection> tracks_token;
    const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
    const bool histos;

    MatchResult matchtracks(const reco::GenParticle&, const edm::Handle<reco::TrackCollection>&, const edm::Handle<reco::BeamSpot>& );
    Match matchchi2(const reco::GenParticle&, const reco::TrackRef&, const edm::Handle<reco::BeamSpot>& );

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
    histos(cfg.getParameter<bool>("histos"))
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
    gentkTree->Branch("gen_pt",   &gtInfo->gen_pt);
    gentkTree->Branch("gen_eta",  &gtInfo->gen_eta);
    gentkTree->Branch("gen_phi",  &gtInfo->gen_phi);
    gentkTree->Branch("gen_dxy",  &gtInfo->gen_dxy);
    gentkTree->Branch("gen_dz",   &gtInfo->gen_dz);
    gentkTree->Branch("gen_charge",&gtInfo->gen_charge);
    gentkTree->Branch("gen_match", &gtInfo->gen_match);
    gentkTree->Branch("gen_llp_idx",&gtInfo->gen_llp_idx);
    gentkTree->Branch("gen_tk_idx",&gtInfo->gen_tk_idx);
    gentkTree->Branch("matched_track_pt",   &gtInfo->matched_track_pt);
    gentkTree->Branch("matched_track_eta",  &gtInfo->matched_track_eta);
    gentkTree->Branch("matched_track_phi",  &gtInfo->matched_track_phi);
    gentkTree->Branch("matched_track_dxy",  &gtInfo->matched_track_dxy);
    gentkTree->Branch("matched_track_dxy_err",  &gtInfo->matched_track_dxy_err);
    gentkTree->Branch("matched_track_dz",       &gtInfo->matched_track_dz);
    gentkTree->Branch("matched_track_dz_err",   &gtInfo->matched_track_dz_err);
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

  std::vector<int> track_match(tracks->size(),0);

  for (size_t illp=0; illp<genllps->size(); ++illp){
    const auto& llp = genllps->at(illp);
    if (!llp.valid()) continue;
    std::vector<reco::Track> matched_tks;
    const auto gen_tks = llp.getGenTracks();
    if (histos) n_gentracks_LLP->Fill(gen_tks.size());
    int n_matched_tracks = 0;
    for (const auto& gtk:gen_tks){
      const auto matchres = matchtracks(gtk, tracks, beamspot);
      gtInfo->gen_pt.push_back(gtk.pt());
      gtInfo->gen_eta.push_back(gtk.eta());
      gtInfo->gen_phi.push_back(gtk.phi());
      gtInfo->gen_dxy.push_back(gen_dxy(gtk,beamspot));
      gtInfo->gen_dz.push_back(gen_dz(gtk,beamspot));
      gtInfo->gen_charge.push_back(gtk.charge());
      gtInfo->gen_llp_idx.push_back(illp);
      gtInfo->gen_tk_idx.push_back(matchres.first);
      if (matchres.first!=-1){
        gtInfo->gen_match.push_back(true);
        n_matched_tracks += 1;
        track_match[matchres.first] += 1;
        reco::TrackRef tk(tracks, matchres.first);

        gtInfo->matched_track_pt.push_back(tk->pt());
        gtInfo->matched_track_eta.push_back(tk->eta());
        gtInfo->matched_track_phi.push_back(tk->phi());
        gtInfo->matched_track_dxy.push_back(tk->dxy(*beamspot));
        gtInfo->matched_track_dxy_err.push_back(tk->dxyError());
        gtInfo->matched_track_dz.push_back(tk->dz((*beamspot).position()));
        gtInfo->matched_track_dz_err.push_back(tk->dzError());

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
        gtInfo->matched_track_pt.push_back(-1);
        gtInfo->matched_track_eta.push_back(-1);
        gtInfo->matched_track_phi.push_back(-1);
        gtInfo->matched_track_dxy.push_back(-1);
        gtInfo->matched_track_dxy_err.push_back(-1);
        gtInfo->matched_track_dz.push_back(-1);
        gtInfo->matched_track_dz_err.push_back(-1);
      
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
  std::cout << "number of gen particles " << (gtInfo->gen_tk_idx).size() << std::endl;
  for(size_t i=0; i<(gtInfo->gen_tk_idx).size(); ++i){
    std::cout << "  match track idx " << gtInfo->gen_tk_idx[i];
    if (gtInfo->gen_tk_idx[i]==-1)
      gtInfo->matched_track_n_gentk.push_back(0);
    else {
      std::cout << " number of matches " << track_match[gtInfo->gen_tk_idx[i]];
      gtInfo->matched_track_n_gentk.push_back(track_match[gtInfo->gen_tk_idx[i]]);
    }
    std::cout << std::endl;
  }

  gentkTree->Fill();
  event.put(std::move(matched_tracks));
}

GenMatchedTracks::MatchResult GenMatchedTracks::matchtracks(const reco::GenParticle& gtk, const edm::Handle<reco::TrackCollection>& tracks, const edm::Handle<reco::BeamSpot>& beamspot) {
  Match min_match(999,999);
  int tk_idx = -1;
  for (size_t i=0; i<tracks->size(); ++i){
    reco::TrackRef tk(tracks, i);
    Match match = matchchi2(gtk,tk,beamspot);
    if (match.first<min_match.first && match.second<0.2){
      min_match = match;
      tk_idx = i;
    }
  }
  return MatchResult(tk_idx,min_match);
}

GenMatchedTracks::Match GenMatchedTracks::matchchi2(const reco::GenParticle& gtk, const reco::TrackRef& rtk, const edm::Handle<reco::BeamSpot>& beamspot) {

  // calculate dxy for gen track
  //double r = 88.*gtk.pt();
  //double cx = gtk.vx() + gtk.charge() * r * sin(gtk.phi());
  //double cy = gtk.vy() - gtk.charge() * r * cos(gtk.phi());
  //double dxy = fabs(r-sqrt(pow((cx-( beamspot->x0() )), 2) + pow((cy-( beamspot->y0() )), 2)));
  //double rz = sqrt(pow((gtk.vx()-( beamspot->x0() )), 2) + pow((gtk.vy()-( beamspot->y0() )), 2));
  //double z = gtk.vz() - beamspot->z0();
  //double dz = z-rz*(gtk.pz()/gtk.pt());

  double dxy = gen_dxy(gtk,beamspot);
  double dz = gen_dz(gtk,beamspot);

  std::vector<double> a;
  a.push_back( ( fabs(rtk->dxy(*beamspot)) - fabs(dxy) ) / rtk->dxyError() );
  a.push_back( ( rtk->dz((*beamspot).position())- dz ) / 4*rtk->dzError() );
  a.push_back( ( rtk->charge()/rtk->pt() - gtk.charge()/gtk.pt()) / (1.0/rtk->ptError()) );
  double dr = reco::deltaR(rtk->eta(), rtk->phi(), gtk.eta(), gtk.phi());
  a.push_back(dr/0.01);
  double asum = 0;
  for (double& xa:a){
    asum += xa*xa;
  }
  return std::pair<double,double>(0.25*asum,dr);
}

void GenMatchedTracks::initStructure()
{
  gtInfo->gen_pt.clear();
  gtInfo->gen_eta.clear();
  gtInfo->gen_phi.clear();
  gtInfo->gen_dxy.clear();
  gtInfo->gen_dz.clear();
  gtInfo->gen_charge.clear();
  gtInfo->gen_match.clear();
  gtInfo->gen_llp_idx.clear();
  gtInfo->gen_tk_idx.clear();
  gtInfo->matched_track_pt.clear();
  gtInfo->matched_track_eta.clear();
  gtInfo->matched_track_phi.clear();
  gtInfo->matched_track_dxy.clear();
  gtInfo->matched_track_dxy_err.clear();
  gtInfo->matched_track_dz.clear();
  gtInfo->matched_track_dz_err.clear();
  gtInfo->matched_track_n_gentk.clear();
}

DEFINE_FWK_MODULE(GenMatchedTracks);
