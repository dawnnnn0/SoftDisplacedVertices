import FWCore.ParameterSet.Config as cms

process = cms.Process("Histos")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring(
    'file:/users/ang.li/public/SoftDV/CMSSW_10_6_30/src/SoftDisplacedVertices/VtxReco/test/TestRun/vtxreco.root'
  )
)

process.TFileService = cms.Service("TFileService", fileName = cms.string("tree.root") )

Histos = cms.EDAnalyzer("EventHistos",
    beamspot_token = cms.InputTag('offlineBeamSpot'),
    jet_token = cms.InputTag('ak4PFJets'),
    met_token = cms.InputTag('pfMet'),
    vtx_token = cms.InputTag('inclusiveSecondaryVerticesSoftDV'),
)

process.p = cms.Path(Histos)
