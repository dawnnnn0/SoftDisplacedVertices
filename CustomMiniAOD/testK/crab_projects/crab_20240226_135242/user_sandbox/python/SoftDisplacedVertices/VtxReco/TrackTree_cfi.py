import FWCore.ParameterSet.Config as cms

TrackTree = cms.EDAnalyzer("TrackTree",
    beamspot_token = cms.InputTag('offlineBeamSpot'),
    primary_vertex_token = cms.InputTag('offlinePrimaryVertices'),
    tracks = cms.InputTag('generalTracks'),
    jet_token = cms.InputTag('ak4PFJets'),
    met_token = cms.InputTag('pfMet'),
    )
