import FWCore.ParameterSet.Config as cms

TracksMiniAOD = cms.EDProducer('TracksMiniAOD',
    packed_candidates = cms.InputTag('packedPFCandidates'),
    )
