import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import *

def nanoAOD_customise_SoftDisplacedVerticesMC(process):

    process.finalGenParticles.select.append('keep status==1 && abs(charge) == 1')
      
    process.load('SoftDisplacedVertices.CustomNanoAODGeneration.GenSecondaryVertexTableProducer_cff')
    process.nanoSequenceMC = cms.Sequence(process.nanoSequenceMC + process.genSecondaryVertexTable)

