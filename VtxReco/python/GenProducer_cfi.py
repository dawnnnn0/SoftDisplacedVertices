import FWCore.ParameterSet.Config as cms

GenInfo = cms.EDProducer('GenProducer',
                                 #gen_particles_token = cms.InputTag('prunedGenParticles'),
                                 gen_particles_token = cms.InputTag('genParticles'),
                                 beamspot_token = cms.InputTag('offlineBeamSpot'),
                                 #last_flag_check = cms.bool(False), # needs to be false now that we're using MiniAOD
                                 debug = cms.bool(False),
                                 llp_id = cms.int32(-1),
                                 lsp_id = cms.int32(-1)
                                 )
