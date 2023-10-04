"""
This produces flat table of displaced vertices
"""

import FWCore.ParameterSet.Config as cms


SVTrackTable = cms.EDProducer("SVTrackTableProducer",
    pvSrc = cms.InputTag("offlineSlimmedPrimaryVertices"),

    svSrc = cms.InputTag("IVFSecondaryVerticesSoftDV"),
    svName = cms.string("SDVSecVtx"),
    svDoc = cms.string("Table of displaced vertices"),
    svCut = cms.string(""),

    tkSrc = cms.InputTag("VertexTracksFilter","seed"),
    tkName = cms.string('SDVTrack'),
    tkDoc = cms.string('Vertex matching to tracks'),
    tkbranchName = cms.string('SecVtx'),

    lookupName = cms.string("SDVIdxLUT"),
    lookupDoc = cms.string("Lookup table for secondary vertex and associated track indices"),

    dlenMin = cms.double(0),
    dlenSigMin = cms.double(0),
    storeCharge = cms.bool(True),

    debug = cms.bool(True),
)
