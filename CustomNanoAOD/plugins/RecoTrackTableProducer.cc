// -*- C++ -*-
//
// Package:    SoftDisplacedVertices/CustomMiniAOD
// Class:      RecoTrackTableProducer
//
/**\class RecoTrackTableProducer RecoTrackTableProducer.cc SoftDisplacedVertices/CustomMiniAOD/plugins/RecoTrackTableProducer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Dietrich Liko, Kaan Gueven
//         Created:  Thu, 20 Jul 2023 10:18:55 GMT
//
//

// system include files
#include <memory>
#include <string>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackBase.h"
#include "DataFormats/NanoAOD/interface/FlatTable.h"

class RecoTrackTableProducer : public edm::stream::EDProducer<>
{
public:
    explicit RecoTrackTableProducer(const edm::ParameterSet &);
    ~RecoTrackTableProducer() override;

    static void fillDescriptions(edm::ConfigurationDescriptions &descriptions);

private:
    void beginStream(edm::StreamID) override;
    void produce(edm::Event &, const edm::EventSetup &) override;
    void endStream() override;

private:
    // ----------member data ---------------------------
    edm::InputTag src_;
    edm::EDGetTokenT<std::vector<reco::Track>> srcToken_;
    edm::InputTag vtx_;
    edm::EDGetTokenT<std::vector<reco::Vertex>> vtxToken_;
    const std::string recoTrackName_;
    const std::string recoTrackDoc_;
};

//
// constructors and destructor
//
RecoTrackTableProducer::RecoTrackTableProducer(const edm::ParameterSet &pset)
    : src_(pset.getParameter<edm::InputTag>("src")),
      srcToken_(consumes<reco::TrackCollection>(src_)),
      vtx_(pset.getParameter<edm::InputTag>("vtx")),
      vtxToken_(consumes<reco::VertexCollection>(vtx_)),
      recoTrackName_(pset.getParameter<std::string>("recoTrackName")),
      recoTrackDoc_(pset.getParameter<std::string>("recoTrackDoc"))
{
    produces<nanoaod::FlatTable>("");
}

RecoTrackTableProducer::~RecoTrackTableProducer()
{
}

// ------------ method called for each event  ------------
void RecoTrackTableProducer::produce(edm::Event &iEvent, const edm::EventSetup &iSetup)
{
    std::cout << "RecoTrackTableProducer" << std::endl;
    edm::Handle<reco::TrackCollection> recoTracks;
    iEvent.getByToken(srcToken_, recoTracks);
    edm::Handle<reco::VertexCollection> recoVertices;
    iEvent.getByToken(vtxToken_, recoVertices);

    std::vector<float> eta, phi, dxy, dz, pt, dxyError, dzError, ptError, phiError, etaError;
    std::vector<int> charge;
    std::vector<bool> isHighPurity;

    auto pvx = recoVertices->begin();
    for (auto track = recoTracks->begin(); track != recoTracks->end(); ++track)
    {
        eta.push_back(track->eta());
        phi.push_back(track->phi());
        pt.push_back(track->pt());
        dxy.push_back(track->dxy(pvx->position()));
        dz.push_back(track->dz(pvx->position()));
        etaError.push_back(track->etaError());
        phiError.push_back(track->phiError());
        ptError.push_back(track->ptError());
        dxyError.push_back(track->dxyError(pvx->position(), pvx->covariance()));
        dzError.push_back(track->dzError(pvx->position(), pvx->covariance()));
        // dxyError.push_back(track->dxyError());
        // dzError.push_back(track->dzError());
        charge.push_back(track->charge());
        isHighPurity.push_back(track->quality(reco::TrackBase::TrackQuality::highPurity));
    }

    auto recoTrackTable = std::make_unique<nanoaod::FlatTable>(recoTracks->size(), recoTrackName_, false);
    recoTrackTable->setDoc(recoTrackDoc_);
    recoTrackTable->addColumn<float>("eta", eta, "eta", nanoaod::FlatTable::FloatColumn, 10);
    recoTrackTable->addColumn<float>("phi", phi, "phi", nanoaod::FlatTable::FloatColumn, 10);
    recoTrackTable->addColumn<float>("pt", pt, "pt", nanoaod::FlatTable::FloatColumn, 10);
    recoTrackTable->addColumn<float>("dxy", dxy, "dxy", nanoaod::FlatTable::FloatColumn, 10);
    recoTrackTable->addColumn<float>("dz", dz, "dz", nanoaod::FlatTable::FloatColumn, 10);
    recoTrackTable->addColumn<float>("etaError", etaError, "etaError", nanoaod::FlatTable::FloatColumn, 10);
    recoTrackTable->addColumn<float>("phiError", phiError, "phiError", nanoaod::FlatTable::FloatColumn, 10);
    recoTrackTable->addColumn<float>("ptError", ptError, "ptError", nanoaod::FlatTable::FloatColumn, 10);
    recoTrackTable->addColumn<float>("dxyError", dxyError, "dxyError", nanoaod::FlatTable::FloatColumn, 10);
    recoTrackTable->addColumn<float>("dzError", dzError, "dzError", nanoaod::FlatTable::FloatColumn, 10);
    recoTrackTable->addColumn<int>("charge", charge, "Charge", nanoaod::FlatTable::IntColumn);
    recoTrackTable->addColumn<bool>("isHighPurity", isHighPurity, "Is High Purity", nanoaod::FlatTable::BoolColumn);
    iEvent.put(std::move(recoTrackTable), "");
}

// ------------ method called once each stream before processing any runs, lumis or events  ------------
void RecoTrackTableProducer::beginStream(edm::StreamID) {}

// ------------ method called once each stream after processing all runs, lumis and events  ------------
void RecoTrackTableProducer::endStream() {}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void RecoTrackTableProducer::fillDescriptions(edm::ConfigurationDescriptions &descriptions)
{
    edm::ParameterSetDescription desc;

    desc.add<edm::InputTag>("src")->setComment("track collection");
    desc.add<edm::InputTag>("vtx")->setComment("vertex collection");

    descriptions.addWithDefaultLabel(desc);
}

// define this as a plug-in
DEFINE_FWK_MODULE(RecoTrackTableProducer);
