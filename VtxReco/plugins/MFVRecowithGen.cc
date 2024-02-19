#include "SoftDisplacedVertices/VtxReco/plugins/MFVRecowithGen.h"

typedef MFVRecowithGen<reco::PFJet> MFVRecowithGenAOD;
typedef MFVRecowithGen<pat::Jet> MFVRecowithGenMINIAOD;

DEFINE_FWK_MODULE(MFVRecowithGenAOD);
DEFINE_FWK_MODULE(MFVRecowithGenMINIAOD);
