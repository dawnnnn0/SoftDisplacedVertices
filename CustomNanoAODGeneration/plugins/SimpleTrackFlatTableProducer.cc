#include "PhysicsTools/NanoAOD/interface/SimpleFlatTableProducer.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "FWCore/Framework/interface/MakerMacros.h"


// typedef SimpleFlatTableProducer<pat::ElectronCollection> SimpleTrackFlatTableProducer;
typedef SimpleFlatTableProducer<reco::Track> SimpleTrackFlatTableProducer;


DEFINE_FWK_MODULE(SimpleTrackFlatTableProducer);