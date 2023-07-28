import FWCore.ParameterSet.Config as cms

VertexTracks = cms.EDFilter("VertexTracks",
    tracks = cms.InputTag('generalTracks'),
    beamspot = cms.InputTag('offlineBeamSpot'),
    min_n_seed_tracks = cms.int32(0),
    min_track_pt = cms.double(0.5),
    #min_track_pt = cms.double(1.),
    min_track_dxy = cms.double(0),
    min_track_nsigmadxy = cms.double(4),
    min_track_nhits = cms.int32(6),
    max_track_normchi2 = cms.double(5),
    #max_track_dz = cms.double(4),
    max_track_dz = cms.double(999),
    max_track_sigmapt_ratio = cms.double(0.015),
    histos = cms.bool(True),
    )
