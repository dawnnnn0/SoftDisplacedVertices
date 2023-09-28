import FWCore.ParameterSet.Config as cms

TrackVertexMatchTable = cms.EDProducer("TrackVertexMatchTableProducer",
      branchName = cms.string('vtx'),
      docString = cms.string('Vertex matching to tracks'),
      objName = cms.string('customTracks'),
      src = cms.InputTag("VertexTracksFilter","seed"),
      vtx = cms.InputTag("IVFSecondaryVerticesSoftDV"),
      debug = cms.bool(False),
    )
