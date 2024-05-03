import FWCore.ParameterSet.Config as cms

VtxMLTableProducer = cms.EDProducer("VtxMLTableProducer",
    primary_vertex_token = cms.InputTag('offlineSlimmedPrimaryVertices'),
    vtx_token = cms.InputTag('IVFSecondaryVerticesSoftDV'),
    tk_token = cms.InputTag('TrackFilter',"seed"),
    model_path = cms.FileInPath("SoftDisplacedVertices/ML/ParTLLP.onnx"),
    )
