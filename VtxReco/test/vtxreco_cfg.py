import FWCore.ParameterSet.Config as cms

process = cms.Process("VtxReco")

process.load("SoftDisplacedVertices.VtxReco.VertexReco_cff")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring(
    'file:/users/ang.li/public/SoftDV/CMSSW_10_6_30/src/SoftDisplacedVertices/VtxReco/test/splitSUSY_M2000_1950_ctau1p0_AOD_2017.root'
  )
)

process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('vtxreco.root'),
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
process.out.outputCommands.append('keep *_pfMet_*_*')
process.out.outputCommands.append('keep *_ak4PFJets_*_*')
process.out.outputCommands.append('keep *_offlineBeamSpot_*_*')
process.out.outputCommands.append('keep *_VertexTracks_*_*')
process.out.outputCommands.append('keep *_inclusiveVertexFinderSoftDV_*_*')
process.out.outputCommands.append('keep *_inclusiveSecondaryVerticesSoftDV_*_*')

process.TFileService = cms.Service("TFileService", fileName = cms.string("vtxreco_histos.root") )

process.p = cms.Path(process.trig_filter + process.inclusiveVertexingTaskSoftDV)
process.outp = cms.EndPath(process.out)
