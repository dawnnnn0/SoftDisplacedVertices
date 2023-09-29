import FWCore.ParameterSet.Config as cms

recoTrackTable = cms.EDProducer("RecoTrackTableProducer",
    src = cms.InputTag("VertexTracksFilter", "seed"),
    vtx = cms.InputTag("offlineSlimmedPrimaryVertices"),
    recoTrackName = cms.string("SDVTracks"),
    recoTrackDoc = cms.string("Filtered reco Tracks"),
    skipNonExistingSrc = cms.bool(True)
)
