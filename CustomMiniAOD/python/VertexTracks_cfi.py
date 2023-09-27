from PhysicsTools.PatAlgos.slimming.isolatedTracks_cfi import isolatedTracks
import FWCore.ParameterSet.Config as cms

VertexTracks = isolatedTracks.clone(
    pT_cut = cms.double(0.50),         # save tracks above this pt
    pT_cut_noIso = cms.double(0.50),  # for tracks with at least this pT, don't apply any iso cut
    miniRelIso_cut = cms.double(1.0),
)