"""
Writes reco::Track collections to nanoAOD as flat n-tuples.
"""



import FWCore.ParameterSet.Config as cms


CustomFlatTable = cms.EDProducer("SimpleTrackFlatTableProducer",
    name = cms.string("customTracks"),
    doc = cms.string("Preselected subset of generalTracks"),
    cut = cms.string(''),
    skipNonExistingSrc = cms.bool(True),
    extension = cms.bool(False),
    singleton = cms.bool(False),
    src = cms.InputTag("VertexTracksFilter", "seed"),
    # src = cms.InputTag("finalIsolatedTracks"),
    variables = cms.PSet(
    # This name (charge) is appended to name of the table like mytable_charge
    # This will be the branch name.
    charge = cms.PSet(
        expr = cms.string('charge'),
        doc = cms.string('electric charge'),
        mcOnly = cms.bool(False),
        type = cms.string('int'),
        precision = cms.int32(-1),
        compression = cms.string('none'),
        ),
    pt = cms.PSet(
        expr = cms.string('pt'),
        doc = cms.string('transverse momentum'),
        mcOnly = cms.bool(False),
        type = cms.string('float'),
        precision = cms.int32(-1),
        compression = cms.string('none'),
        ),
    px = cms.PSet(
        expr = cms.string('px'),
        doc = cms.string('x coordinate of momentum vector'),
        mcOnly = cms.bool(False),
        type = cms.string('float'),
        precision = cms.int32(-1),
        compression = cms.string('none'),
        ),
    py = cms.PSet(
        expr = cms.string('py'),
        doc = cms.string('y coordinate of momentum vector'),
        mcOnly = cms.bool(False),
        type = cms.string('float'),
        precision = cms.int32(-1),
        compression = cms.string('none'),
        ),
    pz = cms.PSet(
        expr = cms.string('pz'),
        doc = cms.string('z coordinate of momentum vector'),
        mcOnly = cms.bool(False),
        type = cms.string('float'),
        precision = cms.int32(-1),
        compression = cms.string('none'),
        ),
    vx = cms.PSet(
        expr = cms.string('vx'),
        doc = cms.string('x coordinate of the reference point on track'),
        mcOnly = cms.bool(False),
        type = cms.string('float'),
        precision = cms.int32(-1),
        compression = cms.string('none'),
        ),
    vy = cms.PSet(
        expr = cms.string('vy'),
        doc = cms.string('y coordinate of the reference point on track'),
        mcOnly = cms.bool(False),
        type = cms.string('float'),
        precision = cms.int32(-1),
        compression = cms.string('none'),
        ),
    vz = cms.PSet(
        expr = cms.string('vz'),
        doc = cms.string('z coordinate of the reference point on track'),
        mcOnly = cms.bool(False),
        type = cms.string('float'),
        precision = cms.int32(-1),
        compression = cms.string('none'),
        ),
    )
)
