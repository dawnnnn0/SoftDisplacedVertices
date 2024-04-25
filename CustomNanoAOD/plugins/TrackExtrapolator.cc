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
#include <cmath>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"

#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/Math/interface/Vector3D.h"
#include "MagneticField/Engine/interface/MagneticField.h"
#include "TrackingTools/GeomPropagators/interface/Propagator.h"
#include "TrackingTools/TrajectoryParametrization/interface/GlobalTrajectoryParameters.h"
#include "TrackingTools/TrajectoryState/interface/FreeTrajectoryState.h"
#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h"
#include "TrackingTools/Records/interface/TrackingComponentsRecord.h"

#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "DataFormats/NanoAOD/interface/FlatTable.h"

#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/IPTools/interface/IPTools.h"
#include "DataFormats/GeometryCommonDetAlgo/interface/Measurement1D.h"

#include <Math/GenVector/PxPyPzM4D.h>


//
// class declaration
//
class TrackExtrapolator : public edm::stream::EDProducer<> {
public:
  explicit TrackExtrapolator(const edm::ParameterSet&);
  ~TrackExtrapolator() override;

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  void beginStream(edm::StreamID) override;
  void produce(edm::Event&, const edm::EventSetup&) override;
  void endStream() override;

  // ----------member data ---------------------------

  const edm::EDGetTokenT<std::vector<reco::Vertex>> svSrc_;  /// Input
  const edm::EDGetTokenT<std::vector<reco::Vertex>> pvSrc_;  /// Input
  const edm::EDGetTokenT<std::vector<reco::Track>>  tkSrc_;  /// Input
  const std::string extrapTkOut_;   /// New parameters will be added to this table.
  const std::string extrapSvOut_;   /// New parameters will be added to this table.

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
    : svSrc_(consumes<std::vector<reco::Vertex>>(iConfig.getParameter<edm::InputTag>("svSrc"))),
      pvSrc_(consumes<std::vector<reco::Vertex>>(iConfig.getParameter<edm::InputTag>("pvSrc"))),
      tkSrc_(consumes<std::vector<reco::Track>>(iConfig.getParameter<edm::InputTag>("tkSrc"))),
      extrapTkOut_(iConfig.getParameter<std::string>("extrapTkOut")),
      extrapSvOut_(iConfig.getParameter<std::string>("extrapSvOut"))
      {
        std::cout << "Propagator constructor is called" << std::endl;
        produces<nanoaod::FlatTable>(extrapTkOut_);
        produces<nanoaod::FlatTable>(extrapSvOut_);
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
  edm::ESHandle<TransientTrackBuilder> trackBuilder;
  iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder", trackBuilder);
  

  // get stuff from Event
  edm::Handle<std::vector<reco::Vertex>> svsIn;
  iEvent.getByToken(svSrc_, svsIn);

  edm::Handle<std::vector<reco::Vertex>> pvsIn;
  iEvent.getByToken(pvSrc_, pvsIn);
  const auto& PV0 = pvsIn->front();

  edm::Handle<std::vector<reco::Track>> tksIn;
  iEvent.getByToken(tkSrc_, tksIn);

  // auto temporaryOutput = std::make_unique<std::vector<float>>();
  std::vector<float> oTk_dxy, oTk_dxyErr, oTk_dxyByHand, oTk_extPV0_dxyByHand, oTk_absolutedxy, oTk_absolutedxyErr, oTk_extSV_mass, oTk_extSV_pAngle;
  std::vector<float>                                     rTk_extPV0_dxyByHand, rTk_absolutedxy, rTk_absolutedxyErr, rTk_mass, rTk_pAngle;
  std::vector<int> svIdx, tkIdx;
  std::vector<float> charge;
  std::vector<float> oTk_vx, oTk_vy, oTk_vz;
  std::vector<float> oTk_px, oTk_py, oTk_pz;
  std::vector<float> oTk_extPV0_vx, oTk_extPV0_vy, oTk_extPV0_vz;
  std::vector<float> oTk_extPV0_px, oTk_extPV0_py, oTk_extPV0_pz;
  std::vector<float> oTk_extSV_vx, oTk_extSV_vy, oTk_extSV_vz;
  std::vector<float> oTk_extSV_px, oTk_extSV_py, oTk_extSV_pz;

  std::vector<float> rTk_vx, rTk_vy, rTk_vz;
  std::vector<float> rTk_px, rTk_py, rTk_pz;
  std::vector<float> rTk_extPV0_vx, rTk_extPV0_vy, rTk_extPV0_vz;
  std::vector<float> rTk_extPV0_px, rTk_extPV0_py, rTk_extPV0_pz;
  std::vector<reco::TrackBase::Vector> oTk_extSV_vec;

  for (const auto& sv : *svsIn) {
    math::XYZTLorentzVectorD vecSum, vecSum2;
    
    for(auto trkBegin = sv.tracks_begin(), trkEnd = sv.tracks_end(), itrk = trkBegin;
       itrk != trkEnd;
       ++itrk){

        reco::TrackBase::Point oTk_extSV_Pos, oTk_extPV0_Pos, rTk_extPV0_Pos;
        reco::TrackBase::Vector oTk_extSV_Mom, oTk_extPV0_Mom, rTk_extPV0_Mom;
        propagateTrackToPCA(sv, **itrk, *field_h, *propagator_h, oTk_extSV_Pos, oTk_extSV_Mom);
        oTk_extSV_vec.push_back(oTk_extSV_Mom);

        // oTk_extSV_pAngle computation
        ROOT::Math::LorentzVector<ROOT::Math::PxPyPzM4D<double> > vec;
        if(sv.trackWeight(*itrk)>=0.5){
          vec.SetPx(oTk_extSV_Mom.X());
          vec.SetPy(oTk_extSV_Mom.Y());
          vec.SetPz(oTk_extSV_Mom.Z());
          vec.SetM(0.13957018);
          vecSum += vec;
        }

        // rTk_pAngle computation
        ROOT::Math::LorentzVector<ROOT::Math::PxPyPzM4D<double> > vec2;
        if(sv.trackWeight(*itrk)>=0.5){
          vec2.SetPx(sv.refittedTrack(*itrk).px());
          vec2.SetPy(sv.refittedTrack(*itrk).py());
          vec2.SetPz(sv.refittedTrack(*itrk).pz());
          vec2.SetM(0.13957018);
          vecSum2 += vec2;
        }

        propagateTrackToPCA(PV0, **itrk, *field_h, *propagator_h, oTk_extPV0_Pos, oTk_extPV0_Mom);

        reco::TransientTrack transient_itrk = trackBuilder->build(**itrk);
        std::pair<bool, Measurement1D> absolutedxy = IPTools::absoluteTransverseImpactParameter(transient_itrk, PV0);

        oTk_dxy.push_back((**itrk).dxy(PV0.position()));
        oTk_dxyErr.push_back((**itrk).dxyError(PV0.position(), PV0.covariance()));
        oTk_dxyByHand.push_back(sqrt(pow((**itrk).vx() - PV0.x(), 2) +
                                     pow((**itrk).vy() - PV0.y(), 2)));
        oTk_extPV0_dxyByHand.push_back(sqrt(pow(oTk_extPV0_Pos.X() - PV0.x(), 2) +
                                            pow(oTk_extPV0_Pos.Y() - PV0.y(), 2)));
        oTk_absolutedxy.push_back(absolutedxy.second.value());
        oTk_absolutedxyErr.push_back(absolutedxy.second.error());


        svIdx.push_back(&sv - &((*svsIn)[0]));
        for (const auto& tk : *tksIn) {
          if (&tk == &(**itrk)){
            tkIdx.push_back(&tk - &((*tksIn)[0]));
          }
        }
        charge.push_back((**itrk).charge());

        oTk_vx.push_back((**itrk).vx());
        oTk_vy.push_back((**itrk).vy());
        oTk_vz.push_back((**itrk).vz());

        oTk_px.push_back((**itrk).px());
        oTk_py.push_back((**itrk).py());
        oTk_pz.push_back((**itrk).pz());

        oTk_extPV0_vx.push_back(oTk_extPV0_Pos.X());
        oTk_extPV0_vy.push_back(oTk_extPV0_Pos.Y());
        oTk_extPV0_vz.push_back(oTk_extPV0_Pos.Z());
        
        oTk_extPV0_px.push_back(oTk_extPV0_Mom.X());
        oTk_extPV0_py.push_back(oTk_extPV0_Mom.Y());
        oTk_extPV0_pz.push_back(oTk_extPV0_Mom.Z());

        oTk_extSV_vx.push_back(oTk_extSV_Pos.X());
        oTk_extSV_vy.push_back(oTk_extSV_Pos.Y());
        oTk_extSV_vz.push_back(oTk_extSV_Pos.Z());
        
        oTk_extSV_px.push_back(oTk_extSV_Mom.X());
        oTk_extSV_py.push_back(oTk_extSV_Mom.Y());
        oTk_extSV_pz.push_back(oTk_extSV_Mom.Z());


        // backwards propagate

        reco::TrackBase::Point extTkPos_r;
        reco::TrackBase::Vector extTkMom_r;
        propagateTrackToPCA(PV0, sv.refittedTrack(*itrk), *field_h, *propagator_h, rTk_extPV0_Pos, rTk_extPV0_Mom);

        reco::TransientTrack r_transient_itrk = trackBuilder->build(sv.refittedTrack(*itrk));
        std::pair<bool, Measurement1D> r_absolutedxy = IPTools::absoluteTransverseImpactParameter(r_transient_itrk, PV0);

        // rTk_dxy.push_back(sv.refittedTrack(*itrk).dxy(PV0.position()));
        rTk_extPV0_dxyByHand.push_back(sqrt(pow(rTk_extPV0_Pos.X() - PV0.x(), 2) + 
                                            pow(rTk_extPV0_Pos.Y() - PV0.y(), 2)));
        rTk_absolutedxy.push_back(r_absolutedxy.second.value());
        rTk_absolutedxyErr.push_back(r_absolutedxy.second.error());

        rTk_vx.push_back(sv.refittedTrack(*itrk).vx());
        rTk_vy.push_back(sv.refittedTrack(*itrk).vy());
        rTk_vz.push_back(sv.refittedTrack(*itrk).vz());

        rTk_px.push_back(sv.refittedTrack(*itrk).px());
        rTk_py.push_back(sv.refittedTrack(*itrk).py());
        rTk_pz.push_back(sv.refittedTrack(*itrk).pz());

        rTk_extPV0_vx.push_back(rTk_extPV0_Pos.X());
        rTk_extPV0_vy.push_back(rTk_extPV0_Pos.Y());
        rTk_extPV0_vz.push_back(rTk_extPV0_Pos.Z());

        rTk_extPV0_px.push_back(rTk_extPV0_Mom.X());
        rTk_extPV0_py.push_back(rTk_extPV0_Mom.Y());
        rTk_extPV0_pz.push_back(rTk_extPV0_Mom.Z());
        


    }
    
    double dx = (sv.x() - PV0.x());
    double dy = (sv.y() - PV0.y());
    double dz = (sv.z() - PV0.z());

    double oTk_extSV_m = vecSum.mass();
    double oTk_extSV_pdotv = (dx * vecSum.Px() + dy * vecSum.Py() + dz * vecSum.Pz()) /
                                                                    sqrt(vecSum.P2()) / 
                                                                    sqrt(dx*dx + dy*dy + dz*dz);
    double rTk_m = vecSum2.mass();
    double rTk_pdotv = (dx * vecSum2.Px() + dy * vecSum2.Py() + dz * vecSum2.Pz()) /
                                                                sqrt(vecSum2.P2()) / 
                                                                sqrt(dx*dx + dy*dy + dz*dz);
    

    oTk_extSV_mass.push_back(oTk_extSV_m);
    oTk_extSV_pAngle.push_back(std::acos(oTk_extSV_pdotv));

    rTk_mass.push_back(rTk_m);
    rTk_pAngle.push_back(std::acos(rTk_pdotv));
  }

  int nEntriesTk = oTk_dxy.size();
  int nEntriesSv = oTk_extSV_pAngle.size();
  auto extrapTkTable = std::make_unique<nanoaod::FlatTable>(nEntriesTk, extrapTkOut_, false);
  auto extrapSvTable = std::make_unique<nanoaod::FlatTable>(nEntriesSv, extrapSvOut_, false);


  extrapTkTable->addColumn<int>("svIdx", svIdx, "svIdx", nanoaod::FlatTable::IntColumn);
  extrapTkTable->addColumn<int>("tkIdx", tkIdx, "tkIdx", nanoaod::FlatTable::IntColumn);
  extrapTkTable->addColumn<float>("charge", charge, "charge", nanoaod::FlatTable::FloatColumn, 10);

  extrapTkTable->addColumn<float>("oTk_dxy", oTk_dxy, "oTk_dxy", nanoaod::FlatTable::FloatColumn, 10);
  extrapTkTable->addColumn<float>("oTk_dxyErr", oTk_dxyErr, "oTk_dxyErr", nanoaod::FlatTable::FloatColumn, 10);
  extrapTkTable->addColumn<float>("oTk_dxyByHand", oTk_dxyByHand, "oTk_dxyByHand", nanoaod::FlatTable::FloatColumn, 10);
  extrapTkTable->addColumn<float>("oTk_extPV0_dxyByHand", oTk_extPV0_dxyByHand, "oTk_extPV0_dxyByHand", nanoaod::FlatTable::FloatColumn, 10);
  extrapTkTable->addColumn<float>("oTk_absolutedxy", oTk_absolutedxy, "oTk_absolutedxy", nanoaod::FlatTable::FloatColumn, 10);
  extrapTkTable->addColumn<float>("oTk_absolutedxyErr", oTk_absolutedxyErr, "oTk_absolutedxyErr", nanoaod::FlatTable::FloatColumn, 10);

  extrapTkTable->addColumn<float>("oTk_vx", oTk_vx, "oTk_vx", nanoaod::FlatTable::FloatColumn, 10);
  extrapTkTable->addColumn<float>("oTk_vy", oTk_vy, "oTk_vy", nanoaod::FlatTable::FloatColumn, 10);
  extrapTkTable->addColumn<float>("oTk_vz", oTk_vz, "oTk_vz", nanoaod::FlatTable::FloatColumn, 10);
  extrapTkTable->addColumn<float>("oTk_px", oTk_px, "oTk_px", nanoaod::FlatTable::FloatColumn, 10);
  extrapTkTable->addColumn<float>("oTk_py", oTk_py, "oTk_py", nanoaod::FlatTable::FloatColumn, 10);
  extrapTkTable->addColumn<float>("oTk_pz", oTk_pz, "oTk_pz", nanoaod::FlatTable::FloatColumn, 10);

  extrapTkTable->addColumn<float>("oTk_extPV0_vx", oTk_extPV0_vx, "oTk_extPV0_vx", nanoaod::FlatTable::FloatColumn, 10);
  extrapTkTable->addColumn<float>("oTk_extPV0_vy", oTk_extPV0_vy, "oTk_extPV0_vy", nanoaod::FlatTable::FloatColumn, 10);
  extrapTkTable->addColumn<float>("oTk_extPV0_vz", oTk_extPV0_vz, "oTk_extPV0_vz", nanoaod::FlatTable::FloatColumn, 10);
  extrapTkTable->addColumn<float>("oTk_extPV0_px", oTk_extPV0_px, "oTk_extPV0_px", nanoaod::FlatTable::FloatColumn, 10);
  extrapTkTable->addColumn<float>("oTk_extPV0_py", oTk_extPV0_py, "oTk_extPV0_py", nanoaod::FlatTable::FloatColumn, 10);
  extrapTkTable->addColumn<float>("oTk_extPV0_pz", oTk_extPV0_pz, "oTk_extPV0_pz", nanoaod::FlatTable::FloatColumn, 10);

  extrapTkTable->addColumn<float>("oTk_extSV_vx", oTk_extSV_vx, "oTk_extSV_vx", nanoaod::FlatTable::FloatColumn, 10);
  extrapTkTable->addColumn<float>("oTk_extSV_vy", oTk_extSV_vy, "oTk_extSV_vy", nanoaod::FlatTable::FloatColumn, 10);
  extrapTkTable->addColumn<float>("oTk_extSV_vz", oTk_extSV_vz, "oTk_extSV_vz", nanoaod::FlatTable::FloatColumn, 10);
  extrapTkTable->addColumn<float>("oTk_extSV_px", oTk_extSV_px, "oTk_extSV_px", nanoaod::FlatTable::FloatColumn, 10);
  extrapTkTable->addColumn<float>("oTk_extSV_py", oTk_extSV_py, "oTk_extSV_py", nanoaod::FlatTable::FloatColumn, 10);
  extrapTkTable->addColumn<float>("oTk_extSV_pz", oTk_extSV_pz, "oTk_extSV_pz", nanoaod::FlatTable::FloatColumn, 10);


  // extrapTkTable->addColumn<float>("rTk_dxy", rTk_dxy, "rTk_dxy", nanoaod::FlatTable::FloatColumn, 10);
  extrapTkTable->addColumn<float>("rTk_absolutedxy", rTk_absolutedxy, "rTk_absolutedxy", nanoaod::FlatTable::FloatColumn, 10);
  extrapTkTable->addColumn<float>("rTk_absolutedxyErr", rTk_absolutedxyErr, "rTk_absolutedxyErr", nanoaod::FlatTable::FloatColumn, 10);
  extrapTkTable->addColumn<float>("rTk_extPV0_dxyByHand", rTk_extPV0_dxyByHand, "rTk_extPV0_dxyByHand", nanoaod::FlatTable::FloatColumn, 10);

  extrapTkTable->addColumn<float>("rTk_vx", rTk_vx, "rTk_vx", nanoaod::FlatTable::FloatColumn, 10);
  extrapTkTable->addColumn<float>("rTk_vy", rTk_vy, "rTk_vy", nanoaod::FlatTable::FloatColumn, 10);
  extrapTkTable->addColumn<float>("rTk_vz", rTk_vz, "rTk_vz", nanoaod::FlatTable::FloatColumn, 10);
  extrapTkTable->addColumn<float>("rTk_px", rTk_px, "rTk_px", nanoaod::FlatTable::FloatColumn, 10);
  extrapTkTable->addColumn<float>("rTk_py", rTk_py, "rTk_py", nanoaod::FlatTable::FloatColumn, 10);
  extrapTkTable->addColumn<float>("rTk_pz", rTk_pz, "rTk_pz", nanoaod::FlatTable::FloatColumn, 10);
  
  extrapTkTable->addColumn<float>("rTk_extPV0_vx", rTk_extPV0_vx, "rTk_extPV0_vx", nanoaod::FlatTable::FloatColumn, 10);
  extrapTkTable->addColumn<float>("rTk_extPV0_vy", rTk_extPV0_vy, "rTk_extPV0_vy", nanoaod::FlatTable::FloatColumn, 10);
  extrapTkTable->addColumn<float>("rTk_extPV0_vz", rTk_extPV0_vz, "rTk_extPV0_vz", nanoaod::FlatTable::FloatColumn, 10);
  extrapTkTable->addColumn<float>("rTk_extPV0_px", rTk_extPV0_px, "rTk_extPV0_px", nanoaod::FlatTable::FloatColumn, 10);
  extrapTkTable->addColumn<float>("rTk_extPV0_py", rTk_extPV0_py, "rTk_extPV0_py", nanoaod::FlatTable::FloatColumn, 10);
  extrapTkTable->addColumn<float>("rTk_extPV0_pz", rTk_extPV0_pz, "rTk_extPV0_pz", nanoaod::FlatTable::FloatColumn, 10);


  extrapSvTable->addColumn<float>("oTk_extSV_mass", oTk_extSV_mass, "oTk_extSV_mass", nanoaod::FlatTable::FloatColumn, 10);
  extrapSvTable->addColumn<float>("oTk_extSV_pAngle", oTk_extSV_pAngle, "oTk_extSV_pAngle", nanoaod::FlatTable::FloatColumn, 10);

  extrapSvTable->addColumn<float>("rTk_mass", rTk_mass, "rTk_mass", nanoaod::FlatTable::FloatColumn, 10);
  extrapSvTable->addColumn<float>("rTk_pAngle", rTk_pAngle, "rTk_pAngle", nanoaod::FlatTable::FloatColumn, 10);
  
  
  

  iEvent.put(std::move(extrapTkTable), extrapTkOut_);
  iEvent.put(std::move(extrapSvTable), extrapSvOut_);


}

// ------------ method called once each stream before processing any runs, lumis or events  ------------
void TrackExtrapolator::beginStream(edm::StreamID) {}

// ------------ method called once each stream after processing all runs, lumis and events  ------------
void TrackExtrapolator::endStream() {}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void TrackExtrapolator::fillDescriptions(edm::ConfigurationDescriptions &descriptions)
{
    edm::ParameterSetDescription desc;

    desc.add<edm::InputTag>("pvSrc")->setComment("Primary vertices");
    desc.add<edm::InputTag>("svSrc")->setComment("Secondary vertices");
    desc.add<edm::InputTag>("tkSrc")->setComment("Tracks");
    desc.add<std::string>("extrapTkOut")->setComment("New table name");
    desc.add<std::string>("extrapSvOut")->setComment("New table name");
    descriptions.addWithDefaultLabel(desc);
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
}

//define this as a plug-in
DEFINE_FWK_MODULE(TrackExtrapolator);