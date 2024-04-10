import FWCore.ParameterSet.Config as cms

recoTrackTableProducer = cms.EDProducer('RecoTrackTableProducer',
  skipNonExistingSrc = cms.bool(False)
)
