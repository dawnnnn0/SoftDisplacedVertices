import FWCore.ParameterSet.Config as cms

from PhysicsTools.PatAlgos.tools.helpers import getPatAlgosToolsTask

def miniAOD_customise_SoftDisplacedVertices(process):

    task = getPatAlgosToolsTask(process)
    process.load('SoftDisplacedVertices.VtxReco.VertexTracks_cfi')
    
    task.add(process.VertexTracksFilter)

    process.MINIAODEventContent.outputCommands.append('keep *_VertexTracks*_*_*')
    process.MINIAODSIMEventContent.outputCommands.append('keep *_VertexTracks*_*_*')

def miniAOD_customise_SoftDisplacedVerticesMC(process):

    miniAOD_customise_SoftDisplacedVertices(process)

    process.prunedGenParticlesWithStableCharged = process.prunedGenParticles.clone()
    process.prunedGenParticlesWithStableCharged.select.append("keep status == 1 && abs(charge) == 1 && pt > 0.5 && abs(eta) < 2.5")
    process.MINIAODSIMEventContent.outputCommands.append('keep recoGenParticles_prunedGenParticlesWithStableCharged_*_*')

    task = getPatAlgosToolsTask(process)
    task.add(process.prunedGenParticlesWithStableCharged)




