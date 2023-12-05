/*
Comment: Ali Kaan Güven
This is kept just for the sake of demonstrating how one codes a simple producer.
This plugin is NOT used in the main code.
*/


#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/RefToPtr.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/TrackReco/interface/Track.h"



#include <vector>

class PseudoVertexTracksProducer : public edm::stream::EDProducer<> {
public:
  PseudoVertexTracksProducer(edm::ParameterSet const& params) : 
      tracks_(consumes<reco::TrackCollection>(params.getParameter<edm::InputTag>("tracks"))){
          produces<reco::TrackCollection>();
      }

  ~PseudoVertexTracksProducer() override {}

    void produce(edm::Event& iEvent, const edm::EventSetup& iSetup) override {
    auto out = std::make_unique<reco::TrackCollection>();

    edm::Handle<reco::TrackCollection> tracks;
    iEvent.getByToken(tracks_, tracks);
    for (const auto & track : *tracks) {
      out->push_back(track);
    }

    iEvent.put(std::move(out));
  }

protected:
  const edm::EDGetTokenT<reco::TrackCollection> tracks_;
};

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PseudoVertexTracksProducer);
