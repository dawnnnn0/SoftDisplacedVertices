// -*- C++ -*-
//
// Package:    SoftDisplacedVertices/CustomMiniAOD
// Class:      METFilter
//
/**\class METFilter METFilter.cc SoftDisplacedVertices/CustomMiniAOD/plugins/METFilter.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  dietrich.liko
//         Created:  Tue, 07 Nov 2023 13:35:45 GMT
//
//

// system include files
#include <algorithm>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"

#include "DataFormats/METReco/interface/PFMET.h"

//
// class declaration
//

class METFilter : public edm::stream::EDFilter<>
{
public:
   explicit METFilter(const edm::ParameterSet &);
   ~METFilter();

   static void fillDescriptions(edm::ConfigurationDescriptions &descriptions);

private:
   virtual void beginStream(edm::StreamID) override;
   virtual bool filter(edm::Event &, const edm::EventSetup &) override;
   virtual void endStream() override;

   // virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
   // virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
   // virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
   // virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

   // ----------member data ---------------------------
   edm::InputTag src_;
   edm::EDGetTokenT<std::vector<reco::PFMET>> srcToken_;
   float minMET_;
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
METFilter::METFilter(const edm::ParameterSet &pset)
    : src_(pset.getParameter<edm::InputTag>("src")),
      srcToken_(consumes<std::vector<reco::PFMET>>(src_)),
      minMET_(pset.getParameter<float>("minMET"))
{
   // now do what ever initialization is needed
}

METFilter::~METFilter()
{

   // do anything here that needs to be done at destruction time
   // (e.g. close files, deallocate resources etc.)
}

//
// member functions
//

// ------------ method called on each new Event  ------------
bool METFilter::filter(edm::Event &iEvent, const edm::EventSetup &iSetup)
{
   edm::Handle<std::vector<reco::PFMET>> pfMET;
   iEvent.getByToken(srcToken_, pfMET);

   return std::any_of(
       pfMET->begin(),
       pfMET->end(),
       [this](const reco::PFMET &met)
       { return met.pt() > minMET_; });
}

// ------------ method called once each stream before processing any runs, lumis or events  ------------
void METFilter::beginStream(edm::StreamID)
{
}

// ------------ method called once each stream after processing all runs, lumis and events  ------------
void METFilter::endStream()
{
}

// ------------ method called when starting to processes a run  ------------
/*
void
METFilter::beginRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a run  ------------
/*
void
METFilter::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when starting to processes a luminosity block  ------------
/*
void
METFilter::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a luminosity block  ------------
/*
void
METFilter::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void METFilter::fillDescriptions(edm::ConfigurationDescriptions &descriptions)
{
   // The following says we do not know what parameters are allowed so do no validation
   //  Please change this to state exactly what you do use, even if it is no parameters
   edm::ParameterSetDescription desc;
   desc.setUnknown();
   descriptions.addDefault(desc);
}
// define this as a plug-in
DEFINE_FWK_MODULE(METFilter);
