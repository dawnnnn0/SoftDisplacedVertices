import FWCore.ParameterSet.Config as cms

from SoftDisplacedVertices.VtxReco.VertexTracks_cfi import VertexTracks

from RecoVertex.AdaptiveVertexFinder.inclusiveVertexFinder_cfi import *
from RecoVertex.AdaptiveVertexFinder.vertexMerger_cfi import *
from RecoVertex.AdaptiveVertexFinder.trackVertexArbitrator_cfi import *

inclusiveVertexFinderSoftDV = inclusiveVertexFinder.clone(
    tracks = cms.InputTag("VertexTracks","seed"),
    minPt = 1.0,
    )

vertexMergerSoftDV = vertexMerger.clone(
    secondaryVertices = cms.InputTag("inclusiveVertexFinderSoftDV"),
    )

trackVertexArbitratorSoftDV = trackVertexArbitrator.clone(
    secondaryVertices = cms.InputTag("vertexMergerSoftDV"),
    tracks = cms.InputTag("VertexTracks","seed"),
    )

inclusiveSecondaryVerticesSoftDV = vertexMerger.clone(
    secondaryVertices = "trackVertexArbitratorSoftDV",
    maxFraction = 0.2,
    minSignificance = 10.,
)

#inclusiveVertexFinderSoftDV.vertexReco.smoothing = cms.bool(False)

inclusiveVertexingTaskSoftDV = cms.Sequence(
    VertexTracks *
    inclusiveVertexFinderSoftDV *
    vertexMergerSoftDV *
    trackVertexArbitratorSoftDV *
    inclusiveSecondaryVerticesSoftDV
)
