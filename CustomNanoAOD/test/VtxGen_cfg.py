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

import HLTrigger.HLTfilters.hltHighLevel_cfi as hlt
# import Ang's custom CMSSW modules
from SoftDisplacedVertices.VtxReco.VertexReco_cff import VertexRecoSeq


process = cms.Process('vtxgen')


# from FWCore.MessageService.MessageLogger_cfi import *
# MessageLogger = cms.Service("MessageLogger")
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 10000


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
process.load("SoftDisplacedVertices.VtxReco.DisplayProducer_cfi")
process.load("SoftDisplacedVertices.VtxReco.MFVGen_cfi")

# Import custom table configurations




process.maxEvents = cms.untracked.PSet(
    #input = cms.untracked.int32(1000)
)


MessageLogger = cms.Service("MessageLogger")


# Input source
process.source = cms.Source("PoolSource",
    #fileNames = cms.untracked.vstring('file:/users/ang.li/public/SoftDV/CMSSW_10_6_30/src/SoftDisplacedVertices/CustomMiniAOD/test/MiniAOD.root'),
    fileNames = cms.untracked.vstring('file:/scratch-cbe/users/ang.li/SoftDV/MiniAOD_vtxreco/Stop_600_588_200/MINIAODSIMoutput_0.root'),
    #fileNames = cms.untracked.vstring(
    #  'file:/eos/vbc/experiments/cms/store/user/felang/SignalProduction/samples/Stop/600_585_20/CustomMiniAOD/MINIAODSIMoutput_0.root',
    #  'file:/eos/vbc/experiments/cms/store/user/felang/SignalProduction/samples/Stop/600_585_20/CustomMiniAOD/MINIAODSIMoutput_1.root',
    #  'file:/eos/vbc/experiments/cms/store/user/felang/SignalProduction/samples/Stop/600_585_20/CustomMiniAOD/MINIAODSIMoutput_2.root',
    #  'file:/eos/vbc/experiments/cms/store/user/felang/SignalProduction/samples/Stop/600_585_20/CustomMiniAOD/MINIAODSIMoutput_3.root',
    #  ),
    secondaryFileNames = cms.untracked.vstring()
)

#process.source.eventsToProcess = cms.untracked.VEventRange('1:1608-1:1608',"1:2570-1:2570")

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

process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('vtxgen.root'),
    SelectEvents = cms.untracked.PSet(
      ),
    outputCommands = cms.untracked.vstring(
      'keep *',
      )
)

# Additional output definition

# Defining globally acessible service object that does not affect physics results.
process.TFileService = cms.Service("TFileService", fileName = cms.string("vtxreco_histos.root") )

# EventContentAnalyzer
# process.myEventContent = cms.EDAnalyzer("EventContentAnalyzer")


# Path and EndPath definitions
# process.reco_step = cms.Path(process.trig_filter + process.vtxreco + process.myEventContent)

process.load("SoftDisplacedVertices.VtxReco.VertexReco_cff")
process.load("SoftDisplacedVertices.VtxReco.Vertexer_cfi")

process.vtxRecoIVF = cms.Sequence(
    process.inclusiveVertexFinderSoftDV *
    process.vertexMergerSoftDV *
    process.trackVertexArbitratorSoftDV *
    process.IVFSecondaryVerticesSoftDV
)

#process.MFVSecondaryVerticesSoftDV = process.mfvVerticesMINIAOD.clone()
process.MFVSecondaryVerticesSoftDV = process.MFVGenMINIAOD.clone()
process.vtxRecoMFV = cms.Sequence(
    process.MFVSecondaryVerticesSoftDV
)

process.reco_step = cms.Path(process.vtxRecoIVF + process.vtxRecoMFV + process.DisplayProducer)
#process.endjob_step = cms.EndPath(process.endOfProcess)
process.output_step = cms.EndPath(process.out)





# Schedule definition
process.schedule = cms.Schedule(process.reco_step,
                                process.output_step)
#process.schedule = cms.Schedule(process.nanoAOD_step,
#                                process.endjob_step,
#                                process.NANOAODSIMoutput_step)

