"""
Implementation date: 4/4/2024
Implemented from RecoTracker/TrackExtrapolator/src/TrackExtrapolator.cc
"""

import FWCore.ParameterSet.Config as cms


TrackExtrapolator = cms.EDProducer("TrackExtrapolator",
    svSrc = cms.InputTag("IVFSecondaryVerticesSoftDV")
)
