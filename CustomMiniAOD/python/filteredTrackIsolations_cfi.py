import FWCore.ParameterSet.Config as cms

filteredTrackIsolations = cms.EDProducer("SDVCandTrackPtIsolationProducer",
    src = cms.InputTag("FilterIsolateTracks", "seed"),
    d0Max = cms.double(1000000.0),
    dRMin = cms.double(0.015),
    dRMax = cms.double(0.3),
    elements = cms.InputTag("generalTracks"),
    ptMin = cms.double(0.5), # was 1.5 before 
    dzMax = cms.double(1000000.0)
)

