import FWCore.ParameterSet.Config as cms

from SoftDisplacedVertices.VtxReco.TracksMiniAOD_cfi import TracksMiniAOD
from SoftDisplacedVertices.VtxReco.VertexTracks_cfi import VertexTracks
from SoftDisplacedVertices.VtxReco.TracksMiniAOD_cfi import TracksMiniAOD
from SoftDisplacedVertices.VtxReco.Vertexer_cfi import mfvVerticesAOD, mfvVerticesMINIAOD

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

IVFSecondaryVerticesSoftDV = vertexMerger.clone(
    secondaryVertices = "trackVertexArbitratorSoftDV",
    maxFraction = 0.2,
    minSignificance = 10.,
)

#inclusiveVertexFinderSoftDV.vertexReco.smoothing = cms.bool(False)
inclusiveVertexFinderSoftDV.minPt = cms.double(0.5)
inclusiveVertexFinderSoftDV.minHits = cms.uint32(6)
inclusiveVertexFinderSoftDV.maximumLongitudinalImpactParameter = cms.double(20.)
inclusiveVertexFinderSoftDV.vertexMinAngleCosine = cms.double(0.00001)

trackVertexArbitratorSoftDV.dRCut = cms.double(1.57)
trackVertexArbitratorSoftDV.distCut = cms.double(0.1)
trackVertexArbitratorSoftDV.trackMinPixels = cms.int32(0)


#MFVSecondaryVerticesSoftDV = mfvVerticesAOD.clone()

def VertexRecoSeq(process, name="vtxreco", useMINIAOD=False, useIVF=False):
  if not useIVF:
    #process.MFVSecondaryVerticesSoftDV = process.mfvVerticesAOD.clone()
    process.MFVSecondaryVerticesSoftDV = getattr(process,'mfvVertices'+('MINIAOD' if useMINIAOD else 'AOD')).clone()
    DVSeq = cms.Sequence(
        process.MFVSecondaryVerticesSoftDV
    )
  else:
    DVSeq = cms.Sequence(
        inclusiveVertexFinderSoftDV *
        vertexMergerSoftDV *
        trackVertexArbitratorSoftDV *
        IVFSecondaryVerticesSoftDV
    )
  if useMINIAOD:
    inclusiveVertexFinderSoftDV.primaryVertices = cms.InputTag('offlineSlimmedPrimaryVertices')
    trackVertexArbitratorSoftDV.primaryVertices = cms.InputTag('offlineSlimmedPrimaryVertices')
    VertexTracks.tracks = cms.InputTag('TracksMiniAOD')

    trackSeq = cms.Sequence(
        TracksMiniAOD *      
        VertexTracks
    )

  else:
    trackSeq = cms.Sequence(
        VertexTracks
    )

  VtxReco = cms.Sequence(
      trackSeq *
      DVSeq
  )
  setattr(process,name,VtxReco)
