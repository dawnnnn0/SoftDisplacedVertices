
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
# from FWCore.MessageService.MessageLogger_cfi import *




process = cms.Process('customNanoAOD',Run2_2018,run2_nanoAOD_106Xv2)

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

# Import Ang's configurations
process.load("SoftDisplacedVertices.VtxReco.VertexReco_cff")
process.load("SoftDisplacedVertices.VtxReco.GenProducer_cfi")
process.load("SoftDisplacedVertices.VtxReco.GenMatchedTracks_cfi")
process.load("TrackingTools/TransientTrack/TransientTrackBuilder_cfi")

# Import Kaan's configurations
process.load("SoftDisplacedVertices.CustomNanoAODGeneration.PseudoVertexTracks_cfi")
process.load("SoftDisplacedVertices.CustomNanoAODGeneration.CustomFlatTable_cfi")
process.load("SoftDisplacedVertices.CustomNanoAODGeneration.CustomVertexTable_cfi")



process.maxEvents = cms.untracked.PSet(
    # input = cms.untracked.int32(-1)
)

MessageLogger = cms.Service("MessageLogger")


# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:/users/alikaan.gueven/AOD_to_nanoAOD/data/SUS-RunIISummer20UL18MiniAODv2-00068.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(
    # SkipEvent= cms.untracked.vstring("ProductNotFound"),
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
    fileName = cms.untracked.string('file:/users/alikaan.gueven/AOD_to_nanoAOD/data/SUS-RunIISummer20UL18NanoAODv9-00068.root'),
    outputCommands = process.NANOAODSIMEventContent.outputCommands
)

# # Preparing Ang's output definitions in the MiniAOD output
# # output_mod.outputCommands.append('drop *') # already included in NanoAODEventContent.outputCommands

# # Keep some RECO objects
# output_mod.outputCommands.append('keep *_pfMet_*_*')
# output_mod.outputCommands.append('keep *_ak4PFJets_*_*')
# output_mod.outputCommands.append('keep *_offlinePrimaryVertices_*_*')
# output_mod.outputCommands.append('keep *_generalTracks_*_*')
# output_mod.outputCommands.append('keep *_offlineBeamSpot_*_*')


# # Keep Ang's objects
# output_mod.outputCommands.append('keep *Table*_*Table*_*_customNanoAOD')
# output_mod.outputCommands.append('keep *_inclusiveVertexFinderSoftDV_*_*')    # DON'T USE THEM!!
# output_mod.outputCommands.append('keep *_vertexMergerSoftDV_*_*')             # DON'T USE THEM!!
# output_mod.outputCommands.append('keep *_trackVertexArbitratorSoftDV_*_*')    # DON'T USE THEM!!
# output_mod.outputCommands.append('keep *_IVFSecondaryVerticesSoftDV_*_*')
# output_mod.outputCommands.append('keep ')

process.NANOAODSIMoutput = output_mod

# process.AODEventContent.outputCommands.append('keep *_VertexTracksFilter_*_*')
# process.AODSIMEventContent.outputCommands.append('keep *_VertexTracksFilter_*_*')
# process.CommonEventContent.outputCommands.append('keep *_VertexTracksFilter_*_*')
# process.NANOAODEventContent.outputCommands.append('keep *_VertexTracksFilter_*_*')
# process.NANOAODSIMEventContent.outputCommands.append('keep *_VertexTracksFilter_*_*')
# process.NanoAODEDMEventContent.outputCommands.append('keep *_VertexTracksFilter_*_*')
# process.MINIAODEventContent.outputCommands.append('keep *_VertexTracksFilter_*_*')
# process.MINIAODSIMEventContent.outputCommands.append('keep *_VertexTracksFilter_*_*')
# process.RAWMINIAODEventContent.outputCommands.append('keep *_VertexTracksFilter_*_*')
# process.RAWMINIAODSIMEventContent.outputCommands.append('keep *_VertexTracksFilter_*_*')
# process.MicroEventContent.outputCommands.append('keep *_VertexTracksFilter_*_*')
# process.MicroEventContentMC.outputCommands.append('keep *_VertexTracksFilter_*_*')




# Additional output definition

# Defining globally acessible service object that does not affect physics results.
process.TFileService = cms.Service("TFileService", fileName = cms.string("/users/alikaan.gueven/AOD_to_nanoAOD/data/vtxreco_histos.root") )
VertexRecoSeq(process, useMINIAOD=False, useIVF=True)

# EventContentAnalyzer
process.myEventContent = cms.EDAnalyzer("EventContentAnalyzer")


# Path and EndPath definitions
process.reco_step = cms.Path(process.trig_filter + process.vtxreco)
process.CustomFlatTables = cms.Sequence( process.CustomFlatTable + process.CustomVertexTable)
process.custom_flattable_step = cms.Path(process.myEventContent + process.CustomFlatTables)
# process.custom_flattable_step = cms.Path(process.CustomFlatTables)


process.nanoAOD_step = cms.Path(process.nanoSequenceMC)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.NANOAODSIMoutput_step = cms.EndPath(process.NANOAODSIMoutput)




# Schedule definition
process.schedule = cms.Schedule(process.reco_step,
                                process.custom_flattable_step,
                                process.nanoAOD_step,
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
