import FWCore.ParameterSet.Config as cms

genSecondaryVertexTable = cms.EDProducer("GenSecondaryVertexTableProducer",
    src = cms.InputTag("finalGenParticles"),
    genVtxName = cms.string("GenSVX"),
    genVtxDoc = cms.string("Vertices from generator"),
)
