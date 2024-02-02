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

#include "SoftDisplacedVertices/SoftDVDataFormats/interface/PFIsolation.h"

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
    edm::InputTag isoDR03_;
    edm::EDGetTokenT<std::vector<SoftDV::PFIsolation>> isoDR03Token_;
    const std::string recoTrackName_;
    const std::string recoTrackDoc_;
    const bool skipNonExistingSrc_;
    float pfRelIso03_all_;
    float pfRelIso03_chg_;

};

//
// constructors and destructor
//
RecoTrackTableProducer::RecoTrackTableProducer(const edm::ParameterSet &pset)
    : src_(pset.getParameter<edm::InputTag>("src")),
      srcToken_(consumes<reco::TrackCollection>(src_)),
      vtx_(pset.getParameter<edm::InputTag>("vtx")),
      vtxToken_(consumes<reco::VertexCollection>(vtx_)),
      isoDR03_(pset.getParameter<edm::InputTag>("isoDR03")),
      isoDR03Token_(consumes<std::vector<SoftDV::PFIsolation>>(isoDR03_)),
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
    edm::Handle<std::vector<SoftDV::PFIsolation>> recoTracks_isoDR03;
    edm::Handle<reco::VertexCollection> recoVertices;

    std::vector<float> eta, phi, dxy, dz, pt, dxyError, dzError, ptError, phiError, etaError, validFraction;
    std::vector<float> normalizedChi2;
    std::vector<int> charge, numberOfValidHits, numberOfLostHits;
    std::vector<int> isHighPurity;
    std::vector<int> algo;
    std::vector<float> pfRelIso03_all, pfRelIso03_chg;
    int nEntries = 0;
    try
    {
        iEvent.getByToken(srcToken_, recoTracks);
        iEvent.getByToken(isoDR03Token_, recoTracks_isoDR03);
        iEvent.getByToken(vtxToken_, recoVertices);

        auto pvx = recoVertices->begin();
        for (auto track = recoTracks->begin(); track != recoTracks->end(); ++track)
        {   
            // ISOLATION
            int track_id = track - recoTracks->begin();
            SoftDV::PFIsolation isoDR03 = (*recoTracks_isoDR03)[track_id];

            pfRelIso03_all_ = (isoDR03.chargedHadronIso() +
                                  std::max<double>(isoDR03.neutralHadronIso() +
                                                   isoDR03.photonIso() -
                                                   isoDR03.puChargedHadronIso()/2,0.0))
                                / track->pt();
                
            pfRelIso03_chg_  = isoDR03.chargedHadronIso()/track->pt();
            //////////////////////////////////////////////////

            // ISOLATION
            pfRelIso03_all.push_back(pfRelIso03_all_);
            pfRelIso03_chg.push_back(pfRelIso03_chg_);
            ////////////////////

            normalizedChi2.push_back(track->normalizedChi2());
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
            algo.push_back(track->algo());
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

    recoTrackTable->addColumn<float>("pfRelIso03_all", pfRelIso03_all, "PF relative isolation dR=0.3, total (deltaBeta corrections)", nanoaod::FlatTable::FloatColumn, 10);
    recoTrackTable->addColumn<float>("pfRelIso03_chg", pfRelIso03_chg, "PF relative isolation dR=0.3, charged component", nanoaod::FlatTable::FloatColumn, 10);

    recoTrackTable->addColumn<float>("normalizedChi2", normalizedChi2, "normalizedChi2", nanoaod::FlatTable::FloatColumn, 10);
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
    recoTrackTable->addColumn<int>("algo", algo, "Algorithm of track reconstruction", nanoaod::FlatTable::IntColumn);
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
    desc.add<edm::InputTag>("isoDR03")->setComment("PFIsolationDR03 collection");
    desc.add<edm::InputTag>("vtx")->setComment("vertex collection");
    desc.add<std::string>("recoTrackName")->setComment("name of the flat table to be produced");
    desc.add<std::string>("recoTrackDoc")->setComment("a few words about the documentation");
    desc.add<bool>("skipNonExistingSrc", false)
        ->setComment("whether or not to skip producing the table on absent input product");

    descriptions.addWithDefaultLabel(desc);
}

// define this as a plug-in
DEFINE_FWK_MODULE(RecoTrackTableProducer);
