import FWCore.ParameterSet.Config as cms

recoTrackTable = cms.EDProducer("RecoTrackTableProducer",
    src = cms.InputTag("TrackFilter", "seed"),
    isoDR03 = cms.InputTag("TrackFilter", "isolationDR03"),
    dr03TkSumPt = cms.InputTag("TrackPtIsolation"),
    vtx = cms.InputTag("offlineSlimmedPrimaryVertices"),
    recoTrackName = cms.string("SDVTrack"),
    recoTrackDoc = cms.string("Filtered reco Tracks"),
    skipNonExistingSrc = cms.bool(True)
)
