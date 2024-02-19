#include "FWCore/Framework/interface/stream/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"

class LumiFilter : public edm::stream::EDFilter<> {
  public:
    LumiFilter(const edm::ParameterSet&);

  private:
    virtual bool filter(edm::Event&, const edm::EventSetup&);
    const unsigned n;
    const unsigned which;
};

LumiFilter::LumiFilter(const edm::ParameterSet& cfg)
  : n(cfg.getParameter<unsigned>("n")),
    which(cfg.getParameter<unsigned>("which"))
{}

bool LumiFilter::filter(edm::Event& event, const edm::EventSetup&) {
  if (!event.isRealData()) {
    return (event.luminosityBlock() % n) == which;
  }
  else{
    return true;
  }
}

DEFINE_FWK_MODULE(LumiFilter);
