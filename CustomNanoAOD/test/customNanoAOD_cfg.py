"""
WARNING:
You must adapt your the input source and output filename before you run this.
"""

# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: --python_filename NanoAOD_generation_cfg.py --eventcontent NANOAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:/users/alikaan.gueven/AOD_to_nanoAOD/data/SUS-RunIISummer20UL18NanoAOD-00069.root --conditions 106X_upgrade2018_realistic_v16_L1v1 --step NANO --filein file:/users/alikaan.gueven/AOD_to_nanoAOD/data/SUS-RunIISummer20UL18MiniAOD-00069.root --era Run2_2018,run2_nanoAOD_106Xv2 --no_exec --mc -n -1
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run2_2018_cff import Run2_2018
from Configuration.Eras.Modifier_run2_nanoAOD_106Xv2_cff import run2_nanoAOD_106Xv2

import HLTrigger.HLTfilters.hltHighLevel_cfi as hlt
# import Ang's custom CMSSW modules
from SoftDisplacedVertices.VtxReco.VertexReco_cff import VertexRecoSeq


process = cms.Process('customNanoAOD',Run2_2018,run2_nanoAOD_106Xv2)


# from FWCore.MessageService.MessageLogger_cfi import *
# MessageLogger = cms.Service("MessageLogger")
process.load('FWCore.MessageLogger.MessageLogger_cfi')


# import of standard configurations
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('PhysicsTools.NanoAOD.nano_cff')

# Import vertex reconstruction configurations
process.load("SoftDisplacedVertices.VtxReco.VertexReco_cff")
process.load("SoftDisplacedVertices.VtxReco.GenProducer_cfi")
process.load("SoftDisplacedVertices.VtxReco.GenMatchedTracks_cfi")
process.load("TrackingTools/TransientTrack/TransientTrackBuilder_cfi")

# Import custom table configurations




process.maxEvents = cms.untracked.PSet(
    # input = cms.untracked.int32(-1)
)

MessageLogger = cms.Service("MessageLogger")


# Input source
process.source = cms.Source("PoolSource",
    # fileNames = cms.untracked.vstring('file:/users/alikaan.gueven/AOD_to_nanoAOD/data/SUS-RunIISummer20UL18MiniAODv2-00068.root'),
    fileNames = cms.untracked.vstring('file:/users/alikaan.gueven/AOD_to_nanoAOD/data/dataFromFelix-MiniAODv2.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(
    SkipEvent= cms.untracked.vstring("ProductNotFound"),
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('--python_filename nevts:-1'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# HLT trigger requirement
process.trig_filter = hlt.hltHighLevel.clone(
    HLTPaths = ['HLT_PFMET120_PFMHT120_IDTight_v*'],
    throw = False
)

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '106X_upgrade2018_realistic_v16_L1v1', '')


# Output definition
output_mod = cms.OutputModule("NanoAODOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('NANOAODSIM'),
        filterName = cms.untracked.string('')
    ),
    # fileName = cms.untracked.string('file:/users/alikaan.gueven/AOD_to_nanoAOD/data/SUS-RunIISummer20UL18NanoAODv9-00068.root'),
    fileName = cms.untracked.string('file:/users/alikaan.gueven/AOD_to_nanoAOD/data/dataFromFelix-NanoAODv9.root'),
    outputCommands = process.NANOAODSIMEventContent.outputCommands
)


process.NANOAODSIMoutput = output_mod

# Additional output definition

# Defining globally acessible service object that does not affect physics results.
process.TFileService = cms.Service("TFileService", fileName = cms.string("/users/alikaan.gueven/AOD_to_nanoAOD/data/vtxreco_histos.root") )
VertexRecoSeq(process, useMINIAOD=False, useIVF=True)

# EventContentAnalyzer
# process.myEventContent = cms.EDAnalyzer("EventContentAnalyzer")


# Path and EndPath definitions
# process.reco_step = cms.Path(process.trig_filter + process.vtxreco + process.myEventContent)


from SoftDisplacedVertices.CustomNanoAOD.nanoAOD_cff import nanoAOD_customise_SoftDisplacedVerticesMC
nanoAOD_customise_SoftDisplacedVerticesMC(process)


process.nanoAOD_step = cms.Path(process.nanoSequenceMC)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.NANOAODSIMoutput_step = cms.EndPath(process.NANOAODSIMoutput)




# Schedule definition
process.schedule = cms.Schedule(process.nanoAOD_step,
                                process.endjob_step,
                                process.NANOAODSIMoutput_step)


from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.NanoAOD.nano_cff
from PhysicsTools.NanoAOD.nano_cff import nanoAOD_customizeMC 

#call to customisation function nanoAOD_customizeMC imported from PhysicsTools.NanoAOD.nano_cff
process = nanoAOD_customizeMC(process)

# Automatic addition of the customisation function from Configuration.DataProcessing.Utils
from Configuration.DataProcessing.Utils import addMonitoring 

#call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
process = addMonitoring(process)

# End of customisation functions

# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
