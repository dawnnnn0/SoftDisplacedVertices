#include "SoftDisplacedVertices/VtxReco/plugins/EventTree.h"

typedef EventTree<reco::PFJetCollection, reco::PFMETCollection> EventTreeAOD;
typedef EventTree<pat::JetCollection, pat::METCollection> EventTreeMINIAOD;

DEFINE_FWK_MODULE(EventTreeAOD);
DEFINE_FWK_MODULE(EventTreeMINIAOD);
