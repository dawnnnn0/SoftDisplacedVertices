#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ServiceRegistry/interface/Service.h"


class VertexTracks : public edm::EDFilter {
public:
  VertexTracks(const edm::ParameterSet&);
  virtual bool filter(edm::Event&, const edm::EventSetup&);
private:
  const edm::EDGetTokenT<reco::TrackCollection> tracks_token;
  const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
  const int min_n_seed_tracks;
  const double min_track_pt;
  const double min_track_dxy;
  const double min_track_sigmadxy;
  const int min_track_nhits;
};

VertexTracks::VertexTracks(const edm::ParameterSet& cfg)
  : tracks_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("tracks"))),
    beamspot_token(consumes<reco::BeamSpot>(cfg.getParameter<edm::InputTag>("beamspot"))),
    min_n_seed_tracks(cfg.getParameter<int>("min_n_seed_tracks")),
    min_track_pt(cfg.getParameter<double>("min_track_pt")),
    min_track_dxy(cfg.getParameter<double>("min_track_dxy")),
    min_track_sigmadxy(cfg.getParameter<double>("min_track_sigmadxy")),
    min_track_nhits(cfg.getParameter<int>("min_track_nhits"))
{
  produces<std::vector<reco::TrackRef>>("all");
  produces<std::vector<reco::TrackRef>>("seed");
  produces<reco::TrackCollection>("seed");
}

bool VertexTracks::filter(edm::Event& event, const edm::EventSetup& setup) {

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
    const double sigmadxybs = dxybs / dxyerr;
    const int nhits = tk->hitPattern().numberOfValidHits();

    bool use_track =
      pt > min_track_pt &&
      fabs(dxybs) > min_track_dxy &&
      fabs(sigmadxybs) > min_track_sigmadxy &&
      nhits >= min_track_nhits;

    if (use_track) {
      seed_tracks->push_back(tk);
      seed_tracks_copy->push_back(*tk);
    }
  }

  const bool pass_min_n_seed_tracks = int(seed_tracks->size()) >= min_n_seed_tracks;

  event.put(std::move(all_tracks), "all");
  event.put(std::move(seed_tracks), "seed");
  event.put(std::move(seed_tracks_copy), "seed");

  return pass_min_n_seed_tracks;
}

DEFINE_FWK_MODULE(VertexTracks);
