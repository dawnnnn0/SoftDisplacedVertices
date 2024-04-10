// Implementation date: 4/4/2024
// Implemented from RecoTracker/TrackExtrapolator/src/TrackExtrapolator.cc
//
// Currently there is no need to extrapolate the tracks.
// If needed, this code can be used as a reference.
// N.B. Change SteppingHelixPropagatorAlong to SteppingHelixPropagatorAny as the
//      momentum at ref_point might be pointing opposite to the SV if the stops are not boosted.

// system include files
#include <memory>
#include <vector>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/Math/interface/Vector3D.h"
#include "MagneticField/Engine/interface/MagneticField.h"
#include "TrackingTools/GeomPropagators/interface/Propagator.h"
#include "TrackingTools/TrajectoryParametrization/interface/GlobalTrajectoryParameters.h"
#include "TrackingTools/TrajectoryState/interface/FreeTrajectoryState.h"
#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h"
#include "TrackingTools/Records/interface/TrackingComponentsRecord.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"


//
// class declaration
//
class TrackExtrapolator : public edm::stream::EDProducer<> {
public:
  explicit TrackExtrapolator(const edm::ParameterSet&);
  ~TrackExtrapolator() override;

private:
  void produce(edm::Event&, const edm::EventSetup&) override;

  // ----------member data ---------------------------

  const edm::EDGetTokenT<std::vector<reco::Vertex>> svSrc_;  /// Input

  // ----------internal functions ---------------------------

  /// Propagate a track to a given radius, given the magnetic
  /// field and the propagator. Store the resulting
  /// position, momentum, and direction.
  void propagateTrackToPCA(const reco::Vertex& fSV,
                           const reco::Track& fTrack,
                           const MagneticField& fField,
                           const Propagator& fPropagator,
                           reco::TrackBase::Point& resultPos,
                           reco::TrackBase::Vector& resultMom);
};


//
// constructors and destructor
//
TrackExtrapolator::TrackExtrapolator(const edm::ParameterSet& iConfig)
    : svSrc_(consumes<std::vector<reco::Vertex>>(iConfig.getParameter<edm::InputTag>("svSrc")))
      {
        std::cout << "Propagator constructor is called" << std::endl;
        produces<std::vector<float>>("tkExpo");
      }

TrackExtrapolator::~TrackExtrapolator() {}

//
// member functions
//

// ------------ method called on each new Event  ------------
void TrackExtrapolator::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  
  // get stuff from Event Setup
  edm::ESHandle<MagneticField> field_h;
  iSetup.get<IdealMagneticFieldRecord>().get(field_h);
  edm::ESHandle<Propagator> propagator_h;
  iSetup.get<TrackingComponentsRecord>().get("SteppingHelixPropagatorAny", propagator_h);
  

  // get stuff from Event
  edm::Handle<std::vector<reco::Vertex>> svsIn;
  iEvent.getByToken(svSrc_, svsIn);

  auto temporaryOutput = std::make_unique<std::vector<float>>();

  for (const auto& sv : *svsIn) {
    for(auto trkBegin = sv.tracks_begin(), trkEnd = sv.tracks_end(), itrk = trkBegin;
       itrk != trkEnd;
       ++itrk){

        reco::TrackBase::Point extTkPos;
        reco::TrackBase::Vector extTkMom;
        propagateTrackToPCA(sv, **itrk, *field_h, *propagator_h, extTkPos, extTkMom);
        temporaryOutput->push_back(extTkPos.X());
        std::cout << std::left << std::setw(8) << " " << std::setw(20) << "SV_pos" << std::setw(20) << "orig_refPoint" << std::setw(20) << "extrap_refPoint" << std::endl;
        std::cout << std::left << std::setw(8) << "x" << std::setw(20) << sv.x() << std::setw(20) << (**itrk).vx() << std::setw(20) << extTkPos.X() << std::endl;
        std::cout << std::left << std::setw(8) << "y" << std::setw(20) << sv.y() << std::setw(20) << (**itrk).vy() << std::setw(20) << extTkPos.Y() << std::endl;
        std::cout << std::left << std::setw(8) << "z" << std::setw(20) << sv.z() << std::setw(20) << (**itrk).vz() << std::setw(20) << extTkPos.Z() << std::endl;
        std::cout << " " << std::endl;
        std::cout << std::left << std::setw(8) << " " << std::setw(20) << "orig_mom" << std::setw(20) << "extrap_mom" << std::endl;
        std::cout << std::left << std::setw(8) << "x" << std::setw(20) << (**itrk).px() << std::setw(20) << extTkMom.X() << std::endl;
        std::cout << std::left << std::setw(8) << "y" << std::setw(20) << (**itrk).py() << std::setw(20) << extTkMom.Y() << std::endl;
        std::cout << std::left << std::setw(8) << "z" << std::setw(20) << (**itrk).pz() << std::setw(20) << extTkMom.Z() << std::endl;
        std::cout << "--------------------------------------------------------------------------------" << std::endl;

    }
  }

  iEvent.put(std::move(temporaryOutput), "tkExpo");
}

// -----------------------------------------------------------------------------
//
void TrackExtrapolator::propagateTrackToPCA(const reco::Vertex& fSV,
                                            const reco::Track& fTrack,
                                            const MagneticField& fField,
                                            const Propagator& fPropagator,
                                            reco::TrackBase::Point& resultPos,
                                            reco::TrackBase::Vector& resultMom) {
  GlobalPoint SVPosition(fSV.x(),fSV.y(),fSV.z());   // reference point
  GlobalPoint trackPosition(fTrack.vx(), fTrack.vy(), fTrack.vz());   // reference point
  GlobalVector trackMomentum(fTrack.px(), fTrack.py(), fTrack.pz());  // reference momentum
  

  GlobalTrajectoryParameters trackParams(trackPosition, trackMomentum, fTrack.charge(), &fField);
  FreeTrajectoryState trackState(trackParams);

  FreeTrajectoryState propagatedInfo = fPropagator.propagate(
      trackState, SVPosition);

  resultPos = propagatedInfo.position();
  resultMom = propagatedInfo.momentum();


/*   if (propagatedInfo.isValid()) {
    resultPos = propagatedInfo.globalPosition();
    resultMom = propagatedInfo.globalMomentum();
    return true;
  } else {
    return false;
  } */
}

//define this as a plug-in
DEFINE_FWK_MODULE(TrackExtrapolator);