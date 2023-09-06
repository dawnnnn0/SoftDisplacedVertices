import FWCore.ParameterSet.Config as cms

GenMatchedTracks = cms.EDProducer("GenMatchedTracks",
    llp_gen_token = cms.InputTag('GenInfo'),
    tracks = cms.InputTag('generalTracks'),
    beamspot = cms.InputTag('offlineBeamSpot'),
    primary_vertices = cms.InputTag('offlinePrimaryVertices'),
    histos = cms.bool(True),
    debug = cms.bool(False),
    )
