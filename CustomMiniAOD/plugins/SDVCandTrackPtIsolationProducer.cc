/*
Adapted from
PhysicsTools/IsolationAlgos/plugins/CandTrackPtIsolationProducer.cc
for CMSSW_10_6_X
*/


#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "PhysicsTools/IsolationAlgos/interface/IsolationProducerNew.h"
#include "PhysicsTools/IsolationAlgos/interface/PtIsolationAlgo.h"
// #include "SoftDisplacedVertices/CustomMiniAOD/plugins/PtIsolationAlgo.cc"

typedef reco::modulesNew::IsolationProducer<reco::TrackCollection, reco::TrackCollection,
                PtIsolationAlgo<reco::Track,reco::TrackCollection> > SDVCandTrackPtIsolationProducer;

DEFINE_FWK_MODULE(SDVCandTrackPtIsolationProducer);