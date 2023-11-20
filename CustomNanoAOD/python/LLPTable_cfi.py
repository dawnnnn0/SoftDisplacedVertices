import FWCore.ParameterSet.Config as cms

LLPTable = cms.EDProducer("LLPTableProducer",
    src = cms.InputTag("genParticles"),
    #src = cms.InputTag("finalGenParticlesWithStableCharged"),
    LLPName = cms.string("LLP"),
    LLPDoc = cms.string("Table of LLPs"),
    LLPid_ = cms.vint32(1000006),
    LSPid_ = cms.int32(1000022),
    pvToken = cms.InputTag("offlineSlimmedPrimaryVertices"),
    tkToken = cms.InputTag("VertexTracksFilter","seed"),
    svToken = cms.InputTag("IVFSecondaryVerticesSoftDV"),
    debug = cms.bool(False),
    )
