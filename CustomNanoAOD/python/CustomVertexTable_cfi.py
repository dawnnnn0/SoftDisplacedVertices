"""
This produces flat table of displaced vertices
"""

import FWCore.ParameterSet.Config as cms


CustomVertexTable = cms.EDProducer("SVTableProducer",
    pvSrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
    goodPvCut = cms.string(""),
    svSrc = cms.InputTag("IVFSecondaryVerticesSoftDV"),
    svCut = cms.string(""), #DON'T APPLY CUT HERE, OTHERWISE THE LINK BETWEEN TRACK AND VERTICES WILL BE BROKEN!
    dlenMin = cms.double(0),
    dlenSigMin = cms.double(0),
    pvName = cms.string("primaryVtx"),
    svName = cms.string("softDV"),
    svDoc = cms.string("Table of displaced vertices"),
    storeCharge = cms.bool(True)
)
