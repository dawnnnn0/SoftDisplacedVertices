import FWCore.ParameterSet.Config as cms

from SoftDisplacedVertices.VtxReco.TracksMiniAOD_cfi import TracksMiniAOD
from SoftDisplacedVertices.VtxReco.VertexTracks_cfi import VertexTracksFilter
from SoftDisplacedVertices.VtxReco.Vertexer_cfi import mfvVerticesAOD, mfvVerticesMINIAOD

from RecoVertex.AdaptiveVertexFinder.inclusiveVertexFinder_cfi import *
from RecoVertex.AdaptiveVertexFinder.vertexMerger_cfi import *
from RecoVertex.AdaptiveVertexFinder.trackVertexArbitrator_cfi import *



VertexTracksFilter.min_track_nsigmadxy = cms.double(2)

inclusiveVertexFinderSoftDV = inclusiveVertexFinder.clone(
    primaryVertices = cms.InputTag('offlineSlimmedPrimaryVertices'),
    tracks = cms.InputTag("VertexTracksFilter","seed"),
    minPt = 0.5,
    )

vertexMergerSoftDV = vertexMerger.clone(
    secondaryVertices = cms.InputTag("inclusiveVertexFinderSoftDV"),
    )

trackVertexArbitratorSoftDV = trackVertexArbitrator.clone(
    primaryVertices = cms.InputTag('offlineSlimmedPrimaryVertices'),
    secondaryVertices = cms.InputTag("vertexMergerSoftDV"),
    tracks = cms.InputTag("VertexTracksFilter","seed"),
    )

IVFSecondaryVerticesSoftDV = vertexMerger.clone(
    secondaryVertices = "trackVertexArbitratorSoftDV",
    maxFraction = 0.2,
    minSignificance = 10.,
)

#inclusiveVertexFinderSoftDV.vertexReco.smoothing = cms.bool(False)
#trackVertexArbitratorSoftDV.dRCut = cms.double(1.57) #old
#vertexMergerSoftDV.maxFraction = cms.double(0.4)
#trackVertexArbitratorSoftDV.trackMinPt = cms.double(0.4)
#trackVertexArbitratorSoftDV.dLenFraction = cms.double(1.0)
#IVFSecondaryVerticesSoftDV.minSignificance = cms.double(5.0)


inclusiveVertexFinderSoftDV.minPt = cms.double(0.5)
inclusiveVertexFinderSoftDV.minHits = cms.uint32(6)
inclusiveVertexFinderSoftDV.maximumLongitudinalImpactParameter = cms.double(20.)
inclusiveVertexFinderSoftDV.vertexMinAngleCosine = cms.double(0.00001)
inclusiveVertexFinderSoftDV.clusterizer.clusterMinAngleCosine = cms.double(0.00001) #new
inclusiveVertexFinderSoftDV.clusterizer.distanceRatio = cms.double(1) #new
trackVertexArbitratorSoftDV.distCut = cms.double(0.1)
trackVertexArbitratorSoftDV.trackMinPixels = cms.int32(0)
trackVertexArbitratorSoftDV.dRCut = cms.double(5.0) #new


def VertexFilterSeq(process, name="vtxfilter", useMINIAOD=False, useIVF=False):
    assert useIVF==True and useMINIAOD==False, "Check the code. Do you intend to use a different setup?"

    trackSeq = cms.Sequence(VertexTracksFilter)
    # DVSeq    = cms.Sequence(inclusiveVertexFinderSoftDV *
    #                         vertexMergerSoftDV *
    #                         trackVertexArbitratorSoftDV *
    #                         IVFSecondaryVerticesSoftDV
    #                         )
    

    VtxFilter = cms.Sequence(trackSeq)

    setattr(process,name,VtxFilter)


def VertexRecoSeq(process, name="vtxreco", useMINIAOD=False, useIVF=False):
    assert useIVF==True and useMINIAOD==False, "Check the code. Do you intend to use a different setup?"


    DVSeq = cms.Sequence(inclusiveVertexFinderSoftDV *
                         vertexMergerSoftDV *
                         trackVertexArbitratorSoftDV *
                         IVFSecondaryVerticesSoftDV
                         )
    

    VtxReco = cms.Sequence(DVSeq)
    
    setattr(process,name,VtxReco)
