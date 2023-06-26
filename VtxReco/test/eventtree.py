import FWCore.ParameterSet.Config as cms

useMINIAOD = False

process = cms.Process("Histos")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring(
    'file:/users/ang.li/public/SoftDV/CMSSW_10_6_30/src/SoftDisplacedVertices/VtxReco/test/TestRun/vtxreco_AOD.root'
  )
)

process.TFileService = cms.Service("TFileService", fileName = cms.string("tree.root") )

process.EventTreeAOD = cms.EDAnalyzer("EventTreeAOD",
    beamspot_token = cms.InputTag('offlineBeamSpot'),
    jet_token = cms.InputTag('ak4PFJets'),
    met_token = cms.InputTag('pfMet'),
    vtx_token = cms.InputTag('inclusiveSecondaryVerticesSoftDV'),
)

process.EventTreeMINIAOD = cms.EDAnalyzer("EventTreeMINIAOD",
    beamspot_token = cms.InputTag('offlineBeamSpot'),
    jet_token = cms.InputTag('slimmedJets'),
    met_token = cms.InputTag('slimmedMETs'),
    vtx_token = cms.InputTag('inclusiveSecondaryVerticesSoftDV'),
)


#process.options = cms.untracked.PSet(
#    SkipEvent= cms.untracked.vstring("ProductNotFound"), # make this exception fatal
#)

process.p = cms.Path()
if useMINIAOD:
  process.p = cms.Path(process.EventTreeMINIAOD)
else:
  process.p = cms.Path(process.EventTreeAOD)
