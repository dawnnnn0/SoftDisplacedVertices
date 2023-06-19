import FWCore.ParameterSet.Config as cms

VertexTracks = cms.EDFilter("VertexTracks",
    tracks = cms.InputTag('generalTracks'),
    beamspot = cms.InputTag('offlineBeamSpot'),
    min_n_seed_tracks = cms.int32(0),
    min_track_pt = cms.double(1),
    min_track_dxy = cms.double(0),
    min_track_sigmadxy = cms.double(2),
    min_track_nhits = cms.int32(10),
    )
