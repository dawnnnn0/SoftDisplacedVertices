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

#include "FWCore/Utilities/interface/Exception.h"
#include "FWCore/Utilities/interface/EDMException.h"

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
    const bool skipNonExistingSrc_;
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
      recoTrackDoc_(pset.getParameter<std::string>("recoTrackDoc")),
      skipNonExistingSrc_(pset.getParameter<bool>("skipNonExistingSrc"))
{
    produces<nanoaod::FlatTable>("");
}

RecoTrackTableProducer::~RecoTrackTableProducer()
{
}

// ------------ method called for each event  ------------
void RecoTrackTableProducer::produce(edm::Event &iEvent, const edm::EventSetup &iSetup)
{
    edm::Handle<reco::TrackCollection> recoTracks;
    edm::Handle<reco::VertexCollection> recoVertices;

    std::vector<float> eta, phi, dxy, dz, pt, dxyError, dzError, ptError, phiError, etaError, validFraction;
    std::vector<int> charge, numberOfValidHits, numberOfLostHits;
    std::vector<int> isHighPurity;
    int nEntries = 0;
    try
    {
        iEvent.getByToken(srcToken_, recoTracks);
        iEvent.getByToken(vtxToken_, recoVertices);

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
            // dxyError.push_back(track->dxyError());
            dxyError.push_back(track->dxyError(pvx->position(), pvx->covariance()));
            // dzError.push_back(track->dzError(pvx->position(), pvx->covariance()));
            dzError.push_back(track->dzError());
            charge.push_back(track->charge());
            isHighPurity.push_back(track->quality(reco::TrackBase::TrackQuality::highPurity));
            numberOfValidHits.push_back(track->numberOfValidHits());
            numberOfLostHits.push_back(track->numberOfLostHits());
            validFraction.push_back(track->validFraction());
        }
        nEntries = recoTracks->size();
    }
    catch (const cms::Exception &e)
    {
        if (skipNonExistingSrc_)
        {
            if (e.category() != "ProductNotFound")
            {
                throw e;
            }
        }
        else
        {
            throw e;
        }

        // if (!(skipNonExistingSrc_ && e.category() != "ProductNotFound")){throw e;}
    }

    auto recoTrackTable = std::make_unique<nanoaod::FlatTable>(nEntries, recoTrackName_, false);
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
    recoTrackTable->addColumn<int>("charge", charge, "Charge", nanoaod::FlatTable::IntColumn, 10);
    recoTrackTable->addColumn<int>("isHighPurity", isHighPurity, "Is High Purity", nanoaod::FlatTable::IntColumn);
    recoTrackTable->addColumn<int>("numberOfValidHits", numberOfValidHits, "Number of valid hits", nanoaod::FlatTable::IntColumn);
    recoTrackTable->addColumn<int>("numberOfLostHits", numberOfLostHits, "Number of cases with layers without hits", nanoaod::FlatTable::IntColumn);
    recoTrackTable->addColumn<float>("validFraction", validFraction, "Fraction of valid hits on track", nanoaod::FlatTable::FloatColumn, 10);
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
    desc.add<std::string>("recoTrackName")->setComment("name of the flat table to be produced");
    desc.add<std::string>("recoTrackDoc")->setComment("a few words about the documentation");
    desc.add<bool>("skipNonExistingSrc", false)
        ->setComment("whether or not to skip producing the table on absent input product");

    descriptions.addWithDefaultLabel(desc);
}

// define this as a plug-in
DEFINE_FWK_MODULE(RecoTrackTableProducer);
