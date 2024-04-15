// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"

#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"

#include "DataFormats/NanoAOD/interface/FlatTable.h"
#include "RecoVertex/VertexTools/interface/VertexDistance3D.h"
#include "RecoVertex/VertexTools/interface/VertexDistanceXY.h"
#include "RecoVertex/VertexPrimitives/interface/ConvertToFromReco.h"
#include "RecoVertex/VertexPrimitives/interface/VertexState.h"
#include "DataFormats/Common/interface/ValueMap.h"

#include "DataFormats/GeometryVector/interface/GlobalVector.h"

class RefitTrackCopyProducer : public edm::stream::EDProducer<> {
public:
  explicit RefitTrackCopyProducer(const edm::ParameterSet&);
  ~RefitTrackCopyProducer() override;

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  void beginStream(edm::StreamID) override;
  void produce(edm::Event&, const edm::EventSetup&) override;
  void endStream() override;

  //virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
  //virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
  //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
  //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

  // ----------member data ---------------------------

  const edm::EDGetTokenT<std::vector<reco::Vertex>> pvs_;
  const edm::EDGetTokenT<std::vector<reco::Vertex>> svs_;
  const std::string tkName_;
};

RefitTrackCopyProducer::RefitTrackCopyProducer(const edm::ParameterSet& params)
    : pvs_(consumes<std::vector<reco::Vertex>>(params.getParameter<edm::InputTag>("pvSrc"))),
      svs_(consumes<std::vector<reco::Vertex>>(params.getParameter<edm::InputTag>("svSrc"))),
      tkName_(params.getParameter<std::string>("tkName"))

{
  produces<nanoaod::FlatTable>("tksrefitcopy");
}

RefitTrackCopyProducer::~RefitTrackCopyProducer() {
}


void RefitTrackCopyProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  using namespace edm;
  edm::Handle<std::vector<reco::Vertex>> pvsIn;
  iEvent.getByToken(pvs_, pvsIn);

  edm::Handle<std::vector<reco::Vertex>> svsIn;
  iEvent.getByToken(svs_, svsIn);
  size_t i = 0;
  const auto& PV0 = pvsIn->front();
  std::vector<float> track_vx;
  for (const auto& sv : *svsIn) {
    auto rtks = sv.refittedTracks();
    for (auto& rtk:rtks){
      track_vx.push_back(rtk.vx());
    }
  }

  // Refitted track table
  //
  auto refittkTable = std::make_unique<nanoaod::FlatTable>(track_vx.size(), tkName_, false);
  refittkTable->addColumn<float>("vx", track_vx, "track vx", nanoaod::FlatTable::FloatColumn, 10);

  iEvent.put(std::move(refittkTable), "tksrefitcopy");
}

// ------------ method called once each stream before processing any runs, lumis or events  ------------
void RefitTrackCopyProducer::beginStream(edm::StreamID) {}

// ------------ method called once each stream after processing all runs, lumis and events  ------------
void RefitTrackCopyProducer::endStream() {}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void RefitTrackCopyProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

DEFINE_FWK_MODULE(RefitTrackCopyProducer);
