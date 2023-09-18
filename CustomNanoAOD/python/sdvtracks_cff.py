import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import *

SDVTrackTable = cms.EDProducer("SimpleTrackFlatTableProducer",
    src = cms.InputTag("VertexTracksFilter", "seed"),
    cut = cms.string(""),
    name = cms.string("SDVTrack"),
    doc  = cms.string("charged tracks after basic selection"),
    singleton = cms.bool(False),
    extension = cms.bool(False),
    variables = cms.PSet(P3Vars,
        dz = Var("dz",float,doc="dz (with sign) wrt first PV, in cm",precision=10),
        dxy = Var("dxy",float,doc="dxy (with sign) wrt first PV, in cm",precision=10),
        charge = Var("charge", int, doc="electric charge"),
    ),
)
