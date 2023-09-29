#include "SoftDisplacedVertices/VtxReco/plugins/IterativeVtxReco.h"

typedef MFVVertexer<reco::PFJet> MFVVertexerAOD;
typedef MFVVertexer<pat::Jet> MFVVertexerMINIAOD;

DEFINE_FWK_MODULE(MFVVertexerAOD);
DEFINE_FWK_MODULE(MFVVertexerMINIAOD);
