import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import *

def nanoAOD_customise_SoftDisplacedVertices(process):

    process.load('SoftDisplacedVertices.CustomNanoAOD.sdvtracks_cff')
    process.nanoSequenceMC = cms.Sequence(process.nanoSequenceMC + process.SDVTrackTable)

def nanoAOD_customise_SoftDisplacedVerticesMC(process):

    nanoAOD_customise_SoftDisplacedVertices(process)
    
    process.finalGenParticlesWithStableCharged = process.finalGenParticles.clone(
        src = cms.InputTag("prunedGenParticlesWithStableCharged")
    )
    process.finalGenParticlesWithStableCharged.select.append('keep status==1 && abs(charge) == 1')

    process.genParticleTableForSDV = process.genParticleTable.clone(
        # src = cms.InputTag("finalGenParticlesWithStableCharged"),
        name = cms.string("SDVGenPart")
    )

    process.load('SoftDisplacedVertices.CustomNanoAOD.GenSecondaryVertexTableProducer_cff')

    process.sdvSequence = cms.Sequence(
        process.finalGenParticlesWithStableCharged
        * process.genParticleTableForSDV
        * process.genSecondaryVertexTable
    )
    process.nanoSequenceMC = cms.Sequence(process.nanoSequenceMC +  process.sdvSequence)


