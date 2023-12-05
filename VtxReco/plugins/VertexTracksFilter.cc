#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "FWCore/Framework/interface/one/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ServiceRegistry/interface/Service.h"


class VertexTracksFilter : public edm::one::EDFilter<edm::one::SharedResources>{
public:
  VertexTracksFilter(const edm::ParameterSet&);
  virtual bool filter(edm::Event&, const edm::EventSetup&);
private:
  const edm::EDGetTokenT<reco::TrackCollection> tracks_token;
  const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
  const int min_n_seed_tracks;
  const double min_track_pt;
  const double min_track_dxy;
  const double min_track_nsigmadxy;
  const int min_track_nhits;
  const double max_track_normchi2;
  const double max_track_dz;
  const double max_track_sigmapt_ratio;
  const bool histos;

  static const int N_TRACK_TYPES = 2;
  static const int N_TRACK_VARS = 11;
  TH1D* h_n_track[N_TRACK_TYPES];
  TH1D* h_track_vars[N_TRACK_TYPES][N_TRACK_VARS];
  TH1D* h_track_pt[N_TRACK_TYPES];
  TH1D* h_track_dxy[N_TRACK_TYPES];
  TH1D* h_track_dxyerr[N_TRACK_TYPES];
  TH1D* h_track_nsigmadxy[N_TRACK_TYPES];
  TH1D* h_track_nhits[N_TRACK_TYPES];
  TH1D* h_track_normchi2[N_TRACK_TYPES];
  TH1D* h_track_dz[N_TRACK_TYPES];
  TH1D* h_track_sigmapt_ratio[N_TRACK_TYPES];
};

VertexTracksFilter::VertexTracksFilter(const edm::ParameterSet& cfg)
  : tracks_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("tracks"))),
    beamspot_token(consumes<reco::BeamSpot>(cfg.getParameter<edm::InputTag>("beamspot"))),
    min_n_seed_tracks(cfg.getParameter<int>("min_n_seed_tracks")),
    min_track_pt(cfg.getParameter<double>("min_track_pt")),
    min_track_dxy(cfg.getParameter<double>("min_track_dxy")),
    min_track_nsigmadxy(cfg.getParameter<double>("min_track_nsigmadxy")),
    min_track_nhits(cfg.getParameter<int>("min_track_nhits")),
    max_track_normchi2(cfg.getParameter<double>("max_track_normchi2")),
    max_track_dz(cfg.getParameter<double>("max_track_dz")),
    max_track_sigmapt_ratio(cfg.getParameter<double>("max_track_sigmapt_ratio")),
    histos(cfg.getParameter<bool>("histos"))
{
  usesResource("TFileService");
  produces<std::vector<reco::TrackRef>>("all");
  produces<std::vector<reco::TrackRef>>("seed");
  produces<reco::TrackCollection>("seed");

  if (histos){
    edm::Service<TFileService> fs;
    const char* track_desc[N_TRACK_TYPES] = {"all", "seed"};
    const char* var_names[N_TRACK_VARS] = {"pt", "eta", "phi", "dxy", "dxyerr", "nsigmadxy", "nhits", "normchi2", "dz", "pterr", "pterr_ratio"};
    const int var_nbins[N_TRACK_VARS] = {250, 50, 50, 500, 500, 100, 20, 20, 80, 50, 50};
    const double var_lo[N_TRACK_VARS] = {  0, -2.5, -3.15, -0.2,   0,  0,  0,  0, -20,    0,   0};
    const double var_hi[N_TRACK_VARS] = { 50,  2.5,  3.15,  0.2, 0.2, 10, 20, 10,  20, 0.15, 0.1};
    for (int i=0; i<N_TRACK_TYPES; ++i){
      h_n_track[i] = fs->make<TH1D>(TString::Format("h_n_%s_track", track_desc[i]),TString::Format(";number of %s tracks;A.U.", track_desc[i]),200,0,200);
      for (int ii=0; ii<N_TRACK_VARS; ++ii){
        h_track_vars[i][ii] = fs->make<TH1D>(TString::Format("h_%s_track_%s",track_desc[i],var_names[ii]), TString::Format(";%s;",var_names[ii]),var_nbins[ii],var_lo[ii],var_hi[ii]);
      }
    }
  }
}

bool VertexTracksFilter::filter(edm::Event& event, const edm::EventSetup& setup) {

  std::unique_ptr<std::vector<reco::TrackRef>> all_tracks (new std::vector<reco::TrackRef>);
  std::unique_ptr<std::vector<reco::TrackRef>> seed_tracks(new std::vector<reco::TrackRef>);
  std::unique_ptr<reco::TrackCollection> seed_tracks_copy(new reco::TrackCollection);

  edm::Handle<reco::TrackCollection> tracks;
  event.getByToken(tracks_token, tracks);

  edm::Handle<reco::BeamSpot> beamspot;
  event.getByToken(beamspot_token, beamspot);

  for (size_t i=0; i<tracks->size(); ++i){
    reco::TrackRef tk(tracks, i);
    all_tracks->push_back(tk);
    const double pt = tk->pt();
    const double dxybs = tk->dxy(*beamspot);
    const double dxyerr = tk->dxyError();
    const double nsigmadxybs = dxybs / dxyerr;
    const double nhits = tk->hitPattern().numberOfValidHits();
    const double normchi2 = tk->normalizedChi2();
    const double dz = tk->dz((*beamspot).position());
    const double sigmapt = tk->ptError();
    const double sigmapt_ratio = sigmapt / pt;

    bool use_track =
      pt > min_track_pt &&
      fabs(dxybs) > min_track_dxy &&
      fabs(nsigmadxybs) > min_track_nsigmadxy &&
      nhits >= min_track_nhits &&
      normchi2 < max_track_normchi2 && 
      fabs(dz) < max_track_dz &&
      sigmapt_ratio < max_track_sigmapt_ratio;

    if (histos) {
      const double vars[N_TRACK_VARS] = {pt, tk->eta(), tk->phi(), dxybs, dxyerr, nsigmadxybs, nhits, normchi2, dz, sigmapt, sigmapt_ratio};
      for (int ivar=0; ivar<N_TRACK_VARS; ++ivar){
        h_track_vars[0][ivar]->Fill(vars[ivar]);
      }
    }

    if (use_track) {
      seed_tracks->push_back(tk);
      seed_tracks_copy->push_back(*tk);
      if (histos) {
        const double vars[N_TRACK_VARS] = {pt, tk->eta(), tk->phi(), dxybs, dxyerr, nsigmadxybs, nhits, normchi2, dz, sigmapt, sigmapt_ratio};
        for (int ivar=0; ivar<N_TRACK_VARS; ++ivar){
          h_track_vars[1][ivar]->Fill(vars[ivar]);
        }
      }
    }
  }

  const bool pass_min_n_seed_tracks = int(seed_tracks->size()) >= min_n_seed_tracks;

  event.put(std::move(all_tracks), "all");
  event.put(std::move(seed_tracks), "seed");
  event.put(std::move(seed_tracks_copy), "seed");

  return pass_min_n_seed_tracks;
}

DEFINE_FWK_MODULE(VertexTracksFilter);
