import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import *

def nanoAOD_customise_SoftDisplacedVertices(process):

    process.load("SoftDisplacedVertices.VtxReco.VertexReco_cff")
  
    process.vtxReco = cms.Sequence(
        process.inclusiveVertexFinderSoftDV *
        process.vertexMergerSoftDV *
        process.trackVertexArbitratorSoftDV *
        process.IVFSecondaryVerticesSoftDV
    )

    process.load("SoftDisplacedVertices.CustomNanoAOD.SVTrackTable_cfi")
    process.load("SoftDisplacedVertices.CustomNanoAOD.RecoTrackTableProducer_cfi")
    
#   have care when running on data
    process.nanoSequenceMC = cms.Sequence(process.nanoSequenceMC + process.recoTrackTable + process.vtxReco + process.SVTrackTable)
    
    return process

def nanoAOD_customise_SoftDisplacedVerticesMC(process):

    process = nanoAOD_customise_SoftDisplacedVertices(process)
    
    process.finalGenParticlesWithStableCharged = process.finalGenParticles.clone(
        src = cms.InputTag("prunedGenParticles")
    )
    process.finalGenParticlesWithStableCharged.select.append('keep status==1 && abs(charge) == 1')

    process.genParticleForSDVTable = process.genParticleTable.clone(
        src = cms.InputTag("finalGenParticlesWithStableCharged"),
        name = cms.string("SDVGenPart")
    )

    process.load('SoftDisplacedVertices.CustomNanoAOD.GenSecondaryVertexTableProducer_cff')

    process.sdvSequence = cms.Sequence(
        process.finalGenParticlesWithStableCharged
        + process.genParticleForSDVTable
        + process.genSecondaryVertexTable
    )
    process.nanoSequenceMC = cms.Sequence(process.nanoSequenceMC + process.sdvSequence)  
    
    return process


