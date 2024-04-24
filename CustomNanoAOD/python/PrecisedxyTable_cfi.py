"""
Implementation date: 4/4/2024
Implemented from RecoTracker/TrackExtrapolator/src/TrackExtrapolator.cc
"""
import FWCore.ParameterSet.Config as cms
PrecisedxyTable = cms.EDProducer("PrecisedxyTableProducer",
    pvSrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
    svSrc = cms.InputTag("IVFSecondaryVerticesSoftDV"),
    extraOut = cms.string("SDVExtra")
)
