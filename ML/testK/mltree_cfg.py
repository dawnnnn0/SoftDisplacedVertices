import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing

import HLTrigger.HLTfilters.hltHighLevel_cfi as hlt
from SoftDisplacedVertices.VtxReco.VertexReco_cff import VertexRecoSeq

process = cms.Process('MLTree')

options = VarParsing ('analysis')
options.parseArguments()

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
process.load("SoftDisplacedVertices.ML.MLTree_cfi")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents)
)

MessageLogger = cms.Service("MessageLogger")


# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles),
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

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '106X_upgrade2018_realistic_v16_L1v1', '')

VertexRecoSeq(process, 'vtxReco', useMINIAOD=False, useIVF=True)

## Output definition
#output_mod = cms.OutputModule("NanoAODOutputModule",
#    compressionAlgorithm = cms.untracked.string('LZMA'),
#    compressionLevel = cms.untracked.int32(9),
#    dataset = cms.untracked.PSet(
#        dataTier = cms.untracked.string('NANOAODSIM'),
#        filterName = cms.untracked.string('')
#    ),
#    fileName = cms.untracked.string('file:/users/ang.li/public/SoftDV/CMSSW_10_6_30/src/SoftDisplacedVertices/ML/test/NanoAOD.root'),
#    outputCommands = process.NANOAODSIMEventContent.outputCommands
#)
#
#process.NANOAODSIMoutput = output_mod

# Defining globally acessible service object that does not affect physics results.
import os
USER = os.environ.get('USER')
process.TFileService = cms.Service("TFileService", fileName = cms.string(options.outputFile))

process.reco_step = cms.Path(process.vtxReco + process.MLTree)
process.endjob_step = cms.EndPath(process.endOfProcess)

# Schedule definition
process.schedule = cms.Schedule(process.reco_step,
                                process.endjob_step
                                )


from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)
