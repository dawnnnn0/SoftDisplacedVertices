"""
This produces flat table of displaced vertices
"""

import FWCore.ParameterSet.Config as cms


RefitTrackCopyTable = cms.EDProducer("RefitTrackCopyProducer",
    pvSrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
    svSrc = cms.InputTag("IVFSecondaryVerticesSoftDV"),
    tkName = cms.string('SDVRefitTrackCopy'),
)
