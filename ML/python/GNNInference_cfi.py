import FWCore.ParameterSet.Config as cms

GNNInference = cms.EDProducer('GNNInference',
    input_names_emb = cms.vstring("input_tk"),
    input_names_gnn = cms.vstring("input_tk","input_edges"),
    primary_vertex_token = cms.InputTag("offlineSlimmedPrimaryVertices"),
    tracks = cms.InputTag("TrackFilter", "seed"),
    isoDR03 = cms.InputTag("TrackFilter", "isolationDR03"),
    EMB_model_path = cms.FileInPath("SoftDisplacedVertices/ML/EMB_1.onnx"),
    GNN_model_path = cms.FileInPath("SoftDisplacedVertices/ML/GNN_dist0p15_0509.onnx"),
    edge_dist_cut = cms.double(0.02),
    edge_gnn_cut = cms.double(0.9),
    )
