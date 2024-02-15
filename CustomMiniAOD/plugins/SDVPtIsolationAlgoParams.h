#ifndef SDVPtIsolationAlgoParams_h
#define SDVPtIsolationAlgoParams_h
// Partial spacialization of parameter set adapeter helper
//  *
//
#include "SoftDisplacedVertices/CustomMiniAOD/plugins/SDVPtIsolationAlgo.cc"
#include "CommonTools/UtilAlgos/interface/ParameterAdapter.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

namespace reco {
  namespace modules {
    
    template<typename T, typename C> 
    struct ParameterAdapter<SDVPtIsolationAlgo<T, C> > { 
      static SDVPtIsolationAlgo<T, C> make( const edm::ParameterSet & cfg ) {
	  return SDVPtIsolationAlgo<T, C>( cfg.template getParameter<double>( "dRMin" ), 
					cfg.template getParameter<double>( "dRMax" ),
					cfg.template getParameter<double>( "dzMax" ),
					cfg.template getParameter<double>( "d0Max" ),
					cfg.template getParameter<double>( "ptMin" ) );
      }
    };
  }
}

#endif