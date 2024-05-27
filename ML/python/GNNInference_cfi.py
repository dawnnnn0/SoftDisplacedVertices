import FWCore.ParameterSet.Config as cms

GNNInference = cms.EDProducer('GNNInference',
    input_names_emb = cms.vstring("input_tk"),
    input_names_gnn = cms.vstring("input_tk","input_edges_dist"),
    EMB_model_path = cms.FileInPath("SoftDisplacedVertices/ML/EMB_1.onnx"),
    GNN_model_path = cms.FileInPath("SoftDisplacedVertices/ML/GNN_test.onnx"),
    )
