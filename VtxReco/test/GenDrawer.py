import FWCore.ParameterSet.Config as cms

process = cms.Process("Drawer")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(2) )

import FWCore.Utilities.FileUtils as FileUtils
inputDatafileList = FileUtils.loadListFromFile('/users/ang.li/public/SoftDV/CMSSW_10_6_30/src/SoftDisplacedVertices/VtxReco/test/filelist_stop4b_600_588_200.txt')

process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring(
    #'file:/users/ang.li/public/SoftDV/CMSSW_10_6_30/src/SoftDisplacedVertices/VtxReco/test/splitSUSY_M2000_1950_ctau1p0_AOD_2017.root',
    #'root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL17MiniAODv2/splitSUSY_M2000_1950_ctau1p0_TuneCP2_13TeV-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/80000/03435A66-8AC7-7B4C-9744-0D774D27E48B.root',
    #'root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL17MiniAODv2/splitSUSY_M2000_1950_ctau1p0_TuneCP2_13TeV-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/80000/12B0D985-23FA-1B45-B3F9-51E4F20B630B.root',
    #'root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL17MiniAOD/ZJetsToNuNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/00000/E5DF4692-A6EA-0545-B901-D071F3385AAB.root',
    cms.untracked.vstring( *inputDatafileList)
  )
)
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.printTree = cms.EDAnalyzer("ParticleTreeDrawer",
                                   #src = cms.InputTag("prunedGenParticles"),  
                                   src = cms.InputTag("genParticles"),  
                                   printP4 = cms.untracked.bool(False),
                                   printPtEtaPhi = cms.untracked.bool(False),
                                   printVertex = cms.untracked.bool(False),
                                   printStatus = cms.untracked.bool(False),
                                   printIndex = cms.untracked.bool(False),
                                   #status = cms.untracked.vint32( 3 )
                                   )

process.p = cms.Path(process.printTree)
