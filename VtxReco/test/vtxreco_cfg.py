import FWCore.ParameterSet.Config as cms
from SoftDisplacedVertices.VtxReco.VertexReco_cff import VertexRecoSeq

useMINIAOD = True

process = cms.Process("VtxReco")

if useMINIAOD:
  process.load("SoftDisplacedVertices.VtxReco.TracksMiniAOD_cfi")
process.load("SoftDisplacedVertices.VtxReco.VertexReco_cff")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring(
    #'file:/users/ang.li/public/SoftDV/CMSSW_10_6_30/src/SoftDisplacedVertices/VtxReco/test/splitSUSY_M2000_1950_ctau1p0_AOD_2017.root',
    'root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL17MiniAODv2/splitSUSY_M2000_1950_ctau1p0_TuneCP2_13TeV-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/80000/03435A66-8AC7-7B4C-9744-0D774D27E48B.root',
  )
)

process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('vtxreco.root'),
    SelectEvents = cms.untracked.PSet(
      SelectEvents = cms.vstring('p'),
      ),
    outputCommands = cms.untracked.vstring(
      'drop *',
      )
)

# HLT trigger requirement
import HLTrigger.HLTfilters.hltHighLevel_cfi as hlt
process.trig_filter = hlt.hltHighLevel.clone(
    HLTPaths = ['HLT_PFMET120_PFMHT120_IDTight_v*'],
    throw = False
    )

process.load("TrackingTools/TransientTrack/TransientTrackBuilder_cfi")
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
#process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = '106X_mc2017_realistic_v10'

process.out.outputCommands.append('drop *')
if useMINIAOD:
  process.out.outputCommands.append('keep *_slimmedMETs_*_*')
  process.out.outputCommands.append('keep *_slimmedJets_*_*')
else:
  process.out.outputCommands.append('keep *_pfMet_*_*')
  process.out.outputCommands.append('keep *_ak4PFJets_*_*')
process.out.outputCommands.append('keep *_offlineBeamSpot_*_*')
process.out.outputCommands.append('keep *_VertexTracks_*_*')
process.out.outputCommands.append('keep *_inclusiveVertexFinderSoftDV_*_*')
process.out.outputCommands.append('keep *_inclusiveSecondaryVerticesSoftDV_*_*')

process.TFileService = cms.Service("TFileService", fileName = cms.string("vtxreco_histos.root") )

VertexRecoSeq(process, useMINIAOD=useMINIAOD)
process.p = cms.Path(process.trig_filter + process.vtxreco)
process.outp = cms.EndPath(process.out)
