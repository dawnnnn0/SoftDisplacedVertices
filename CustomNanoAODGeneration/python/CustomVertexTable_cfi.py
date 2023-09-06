import FWCore.ParameterSet.Config as cms


CustomVertexTable = cms.EDProducer("VertexTableProducer",
    pvSrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
    goodPvCut = cms.string(""),
    svSrc = cms.InputTag("IVFSecondaryVerticesSoftDV"),
    svCut = cms.string(""),
    dlenMin = cms.double(0),
    dlenSigMin = cms.double(0),
    pvName = cms.string("offlineSlimmedPrimaryVertices"),
    svName = cms.string("inclusiveVertexFinderSoftDV"),
    svDoc = cms.string("First attempt to create a vertex table"),
    storeCharge = cms.bool(True)
)
