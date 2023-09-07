import FWCore.ParameterSet.Config as cms

from PhysicsTools.PatAlgos.tools.helpers import getPatAlgosToolsTask

def miniAOD_customise_SoftDisplacedVertices(process):

    task = getPatAlgosToolsTask(process)
    process.load('SoftDisplacedVertices.VtxReco.VertexTracks_cfi')
    task.add(process.VertexTracksFilter)

    process.MINIAODEventContent.outputCommands.append('keep *_VertexTracksFilter_*_*')
    process.MINIAODSIMEventContent.outputCommands.append('keep *_VertexTracksFilter_*_*')

def miniAOD_customise_SoftDisplacedVerticesMC(process):

    miniAOD_customise_SoftDisplacedVertices(process)

    # keep stable charged particles
    process.prunedGenParticles.select.append("keep status == 1 && abs(charge) == 1")


