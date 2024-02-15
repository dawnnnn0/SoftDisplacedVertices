import FWCore.ParameterSet.Config as cms

recoTrackTable = cms.EDProducer("RecoTrackTableProducer",
    src = cms.InputTag("FilterIsolateTracks", "seed"),
    isoDR03 = cms.InputTag("FilterIsolateTracks", "isolationDR03"),
    dr03TkSumPt = cms.InputTag("filteredTrackIsolations"),
    vtx = cms.InputTag("offlineSlimmedPrimaryVertices"),
    recoTrackName = cms.string("SDVTrack"),
    recoTrackDoc = cms.string("Filtered reco Tracks"),
    skipNonExistingSrc = cms.bool(True)
)
