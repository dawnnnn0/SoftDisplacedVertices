import FWCore.ParameterSet.Config as cms

genSecondaryVertexTable = cms.EDProducer("GenSecondaryVertexTableProducer",
    src = cms.InputTag("finalGenParticles"),
    genPartName = cms.string("GenPart"),   
    genSVtxName = cms.string("GenSVX"),
    genSVtxDoc = cms.string("Vertices from generator"),
)
