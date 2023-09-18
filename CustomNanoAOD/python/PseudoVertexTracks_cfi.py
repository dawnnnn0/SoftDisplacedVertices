"""
Comment: Ali Kaan Guven
This is kept just for the sake of demonstrating how one codes a simple producer.
This plugin is NOT used in the main code.
"""

from FWCore.MessageService.MessageLogger_cfi import *
import FWCore.ParameterSet.Config as cms


PseudoVertexTracks = cms.EDProducer("PseudoVertexTracksProducer",
    tracks = cms.InputTag("VertexTracksFilter")
)