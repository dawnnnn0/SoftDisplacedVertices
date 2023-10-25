import FWCore.ParameterSet.Config as cms

genSecondaryVertexTable = cms.EDProducer("GenSecondaryVertexTableProducer",
    #src = cms.InputTag("finalGenParticlesWithStableCharged"),
    src = cms.InputTag("genParticles"),
    genPartName = cms.string("SDVGenPart"),   
    genVtxName = cms.string("SDVGenVtx"),
    genVtxDoc = cms.string("Vertices from generator"),
)
