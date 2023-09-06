import FWCore.ParameterSet.Config as cms

from SoftDisplacedVertices.VtxReco.TracksMiniAOD_cfi import TracksMiniAOD
from SoftDisplacedVertices.VtxReco.VertexTracks_cfi import VertexTracks
from SoftDisplacedVertices.VtxReco.TracksMiniAOD_cfi import TracksMiniAOD
from SoftDisplacedVertices.VtxReco.Vertexer_cfi import mfvVerticesAOD, mfvVerticesMINIAOD

from RecoVertex.AdaptiveVertexFinder.inclusiveVertexFinder_cfi import *
from RecoVertex.AdaptiveVertexFinder.vertexMerger_cfi import *
from RecoVertex.AdaptiveVertexFinder.trackVertexArbitrator_cfi import *

VertexTracksLoose = VertexTracks.clone(
    min_track_nsigmadxy = cms.double(2),
    )

inclusiveVertexFinderSoftDV = inclusiveVertexFinder.clone(
    tracks = cms.InputTag("VertexTracks","seed"),
    minPt = 0.5,
    )

vertexMergerSoftDV = vertexMerger.clone(
    secondaryVertices = cms.InputTag("inclusiveVertexFinderSoftDV"),
    )

trackVertexArbitratorSoftDV = trackVertexArbitrator.clone(
    secondaryVertices = cms.InputTag("vertexMergerSoftDV"),
    tracks = cms.InputTag("VertexTracks","seed"),
    #tracks = cms.InputTag("VertexTracksLoose","seed"),
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

inclusiveVertexFinderSoftDV.clusterizer.clusterMinAngleCosine = cms.double(0.00001) #new
inclusiveVertexFinderSoftDV.clusterizer.distanceRatio = cms.double(1) #new

#trackVertexArbitratorSoftDV.dRCut = cms.double(1.57) #old
trackVertexArbitratorSoftDV.distCut = cms.double(0.1)
trackVertexArbitratorSoftDV.trackMinPixels = cms.int32(0)

#vertexMergerSoftDV.maxFraction = cms.double(0.4)

#trackVertexArbitratorSoftDV.trackMinPt = cms.double(0.4)
#trackVertexArbitratorSoftDV.dLenFraction = cms.double(1.0)
trackVertexArbitratorSoftDV.dRCut = cms.double(5.0) #new

#IVFSecondaryVerticesSoftDV.minSignificance = cms.double(5.0)

MFVSecondaryVerticesSoftDV = mfvVerticesAOD.clone()

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
    VertexTracksLoose.tracks = cms.InputTag('TracksMiniAOD')

    trackSeq = cms.Sequence(
        TracksMiniAOD *      
        VertexTracks *
        VertexTracksLoose
    )

  else:
    trackSeq = cms.Sequence(
        VertexTracks *
        VertexTracksLoose
    )

  VtxReco = cms.Sequence(
      trackSeq *
      DVSeq
  )
  setattr(process,name,VtxReco)
