import FWCore.ParameterSet.Config as cms
from SoftDisplacedVertices.VtxReco.VertexReco_cff import VertexRecoSeq

useMINIAOD = True
useIVF = True

process = cms.Process("VtxReco")

if useMINIAOD:
  process.load("SoftDisplacedVertices.VtxReco.TracksMiniAOD_cfi")
process.load("SoftDisplacedVertices.VtxReco.VertexReco_cff")
process.load("SoftDisplacedVertices.VtxReco.GenProducer_cfi")
#process.load("SoftDisplacedVertices.VtxReco.Vertexer_cfi")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )

process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring(
    #'file:/users/ang.li/public/SoftDV/CMSSW_10_6_30/src/SoftDisplacedVertices/VtxReco/test/splitSUSY_M2000_1950_ctau1p0_AOD_2017.root',
    #'root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL17MiniAODv2/splitSUSY_M2000_1950_ctau1p0_TuneCP2_13TeV-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/80000/03435A66-8AC7-7B4C-9744-0D774D27E48B.root',
    'root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL17MiniAODv2/splitSUSY_M2000_1950_ctau1p0_TuneCP2_13TeV-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/80000/12B0D985-23FA-1B45-B3F9-51E4F20B630B.root'
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
process.out.outputCommands.append('keep *_GenInfo_*_*')
if useIVF:
  process.out.outputCommands.append('keep *_inclusiveVertexFinderSoftDV_*_*')
  process.out.outputCommands.append('keep *_IVFSecondaryVerticesSoftDV_*_*')
else:
  process.out.outputCommands.append('keep *_MFVSecondaryVerticesSoftDV_*_*')

process.TFileService = cms.Service("TFileService", fileName = cms.string("vtxreco_histos.root") )

#gen info
process.GenInfo.llp_id = 1000021
process.GenInfo.gen_particles_token = cms.InputTag('prunedGenParticles')

VertexRecoSeq(process, useMINIAOD=useMINIAOD, useIVF=useIVF)
process.p = cms.Path(process.trig_filter + process.GenInfo + process.vtxreco)
process.outp = cms.EndPath(process.out)
