/*
Defines an alias for the templated class.
*/

#include "PhysicsTools/NanoAOD/interface/SimpleFlatTableProducer.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "FWCore/Framework/interface/MakerMacros.h"


typedef SimpleFlatTableProducer<reco::Track> SimpleTrackFlatTableProducer;


DEFINE_FWK_MODULE(SimpleTrackFlatTableProducer);