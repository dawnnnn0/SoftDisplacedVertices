// -*- C++ -*-
//
// Package:    Demo/DemoAnalyzer
// Class:      GenSecondaryVertexTableProducer
//
/**\class GenSecondaryVertexTableProducer GenSecondaryVertexTableProducer.cc Demo/DemoAnalyzer/plugins/GenSecondaryVertexTableProducer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Dietrich Liko
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

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/NanoAOD/interface/FlatTable.h"

//
// class declaration
//
class GenSecondaryVertexTableProducer : public edm::stream::EDProducer<>
{
public:
   explicit GenSecondaryVertexTableProducer(const edm::ParameterSet &);
   ~GenSecondaryVertexTableProducer() override;

   static void fillDescriptions(edm::ConfigurationDescriptions &descriptions);

private:
   void beginStream(edm::StreamID) override;
   void produce(edm::Event &, const edm::EventSetup &) override;
   void endStream() override;

private:
   // ----------member data ---------------------------
   edm::InputTag src_;
   edm::EDGetTokenT<std::vector<reco::GenParticle>> srcToken_;
   const std::string genVtxName_;
   const std::string genVtxDoc_;
   const std::string genPartName_;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
GenSecondaryVertexTableProducer::GenSecondaryVertexTableProducer(const edm::ParameterSet &pset)
    : src_(pset.getParameter<edm::InputTag>("src")),
      srcToken_(consumes<reco::GenParticleCollection>(src_)),
      genVtxName_(pset.getParameter<std::string>("genVtxName")),
      genVtxDoc_(pset.getParameter<std::string>("genVtxDoc")),
      genPartName_(pset.getParameter<std::string>("genPartName"))
{
   produces<nanoaod::FlatTable>("GenVtx");
   produces<nanoaod::FlatTable>("GenPart");
}

GenSecondaryVertexTableProducer::~GenSecondaryVertexTableProducer()
{
}

// ------------ method called for each event  ------------
void GenSecondaryVertexTableProducer::produce(edm::Event &iEvent, const edm::EventSetup &iSetup)
{
   // qstd::cout << "GenSecondaryVertexTableProducer" << std::endl;
   edm::Handle<reco::GenParticleCollection> genParticles;
   iEvent.getByToken(srcToken_, genParticles);

   std::vector<math::XYZPoint> vertices;
   std::vector<std::vector<long>> vtx_gp_idx;
   for (auto gp = genParticles->begin(); gp != genParticles->end(); ++gp)
   {
      if (gp->status() != 1 || abs(gp->charge()) != 1)
         continue;

      math::XYZPoint vtx = gp->vertex();
      float min_dist2 = 0.005 * 0.005;
      int min_idx = -1;
      for (auto vtx1 = vertices.begin(); vtx1 != vertices.end(); ++vtx1)
      {
         float dist2 = (vtx - (*vtx1)).mag2();
         if (dist2 < min_dist2)
         {
            min_dist2 = dist2;
            min_idx = vtx1 - vertices.begin();
         }
      }
      if (min_idx >= 0)
      {
         vtx_gp_idx[min_idx].push_back(gp - genParticles->begin());
      }
      else
      {
         vertices.push_back(vtx);
         vtx_gp_idx.push_back({gp - genParticles->begin()});
      };
   };
   for (std::size_t ivx = 0; ivx < vertices.size();)
   {
      if (vtx_gp_idx[ivx].size() == 1)
      {
         vertices.erase(vertices.begin() + ivx);
         vtx_gp_idx.erase(vtx_gp_idx.begin() + ivx);
      }
      else
      {
         ++ivx;
      };
   }

   std::vector<float> vtx_x, vtx_y, vtx_z;
   std::vector<int> vtx_nr_tracks;
   for (std::size_t ivx = 0; ivx < vertices.size(); ++ivx)
   {
      vtx_x.push_back(vertices[ivx].x());
      vtx_y.push_back(vertices[ivx].y());
      vtx_z.push_back(vertices[ivx].z());
      vtx_nr_tracks.push_back(vtx_gp_idx[ivx].size());
   }
   auto vtxTable = std::make_unique<nanoaod::FlatTable>(vertices.size(), genVtxName_, false);
   vtxTable->setDoc(genVtxDoc_);
   vtxTable->addColumn<float>("x", vtx_x, "vertex x", 10);
   vtxTable->addColumn<float>("y", vtx_y, "vertex y", 10);
   vtxTable->addColumn<float>("z", vtx_z, "vertex z", 10);
   vtxTable->addColumn<int16_t>("nrTracks", vtx_nr_tracks, "number of charged tracks", 10);

   std::vector<int> gp_vtx_idx(genParticles->size(), -1);
   for (std::size_t ivx = 0; ivx < vertices.size(); ++ivx)
   {
      for (std::size_t i = 0; i < vtx_gp_idx[ivx].size(); ++i)
      {
         gp_vtx_idx[vtx_gp_idx[ivx][i]] = ivx;
      };
   };

   auto partTable = std::make_unique<nanoaod::FlatTable>(genParticles->size(), genPartName_, false, true);
   partTable->addColumn<int16_t>("svxIdx", gp_vtx_idx, "secondary vertex index", 10);

   iEvent.put(std::move(vtxTable), "GenVtx");
   iEvent.put(std::move(partTable), "GenPart");
}

// ------------ method called once each stream before processing any runs, lumis or events  ------------
void GenSecondaryVertexTableProducer::beginStream(edm::StreamID) {}

// ------------ method called once each stream after processing all runs, lumis and events  ------------
void GenSecondaryVertexTableProducer::endStream() {}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void GenSecondaryVertexTableProducer::fillDescriptions(edm::ConfigurationDescriptions &descriptions)
{
   edm::ParameterSetDescription desc;

   desc.add<edm::InputTag>("src")->setComment("std::vector<GenParticle> gen particle input collections");
   desc.add<std::string>("genVtxName")->setComment("name of the flat table ouput for vertices");
   desc.add<std::string>("genVtxDoc")->setComment("a few words of documentation");
   desc.add<std::string>("genPartName")->setComment("name of the existing flat table ouput for particles");

   descriptions.addWithDefaultLabel(desc);
}

// define this as a plug-in
DEFINE_FWK_MODULE(GenSecondaryVertexTableProducer);
