import FWCore.ParameterSet.Config as cms

DisplayProducer = cms.EDProducer("DisplayProducer",
    src = cms.InputTag("genParticles"),
    #src = cms.InputTag("finalGenParticlesWithStableCharged"),
    LLPid_ = cms.vint32(1000006),
    LSPid_ = cms.int32(1000022),
    pvToken = cms.InputTag("offlineSlimmedPrimaryVertices"),
    tkToken = cms.InputTag("TrackFilter","seed"),
    svIVFToken = cms.InputTag("IVFSecondaryVerticesSoftDV"),
    svMFVToken = cms.InputTag("MFVSecondaryVerticesSoftDV"),
    debug = cms.bool(False),
    )
