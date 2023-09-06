import FWCore.ParameterSet.Config as cms
process = cms.Process("TESTprint")
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        'file:/users/alikaan.gueven/AOD_to_nanoAOD/data/SUS-RunIISummer20UL18MiniAOD-00069.root'
    )
)
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
)
process.printContent = cms.EDAnalyzer('EventContentAnalyzer',
  indentation = cms.untracked.string('++'),
  verbose = cms.untracked.bool(False),
  verboseIndentation = cms.untracked.string('  '),
  verboseForModuleLabels = cms.untracked.vstring(),
  getData = cms.untracked.bool(False),
  getDataForModuleLabels = cms.untracked.vstring(),
  listContent = cms.untracked.bool(True)
)
process.path = cms.Path(process.printContent)
