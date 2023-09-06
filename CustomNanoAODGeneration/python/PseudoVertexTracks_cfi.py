from FWCore.MessageService.MessageLogger_cfi import *


import FWCore.ParameterSet.Config as cms


PseudoVertexTracks = cms.EDProducer("PseudoVertexTracksProducer",
                                            tracks = cms.InputTag("VertexTracksFilter")
)