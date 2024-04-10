import FWCore.ParameterSet.Config as cms

LumiFilter = cms.EDFilter('LumiFilter',
                          n = cms.uint32(1),
                          which = cms.uint32(0),
                          )
