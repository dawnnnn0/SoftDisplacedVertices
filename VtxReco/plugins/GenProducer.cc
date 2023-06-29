#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "SoftDisplacedVertices/SoftDVDataFormats/interface/GenInfo.h"

class GenProducer : public edm::EDProducer {
  public:
    explicit GenProducer(const edm::ParameterSet&);
  private:
    void produce(edm::Event&, const edm::EventSetup&) override;
    const edm::EDGetTokenT<reco::GenParticleCollection> gen_particles_token;
    const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
    int llp_id;
    bool debug;

    std::vector<SoftDV::LLP> findPattern(const edm::Handle<reco::GenParticleCollection>& gen_particles) const;
};

GenProducer::GenProducer(const edm::ParameterSet& cfg)
  : gen_particles_token(consumes<reco::GenParticleCollection>(cfg.getParameter<edm::InputTag>("gen_particles_token"))),
    beamspot_token(consumes<reco::BeamSpot>(cfg.getParameter<edm::InputTag>("beamspot_token"))),
    llp_id(cfg.getParameter<int>("llp_id")),
    debug(cfg.getParameter<bool>("debug"))
{
  produces<std::vector<SoftDV::LLP>>();
}

std::vector<SoftDV::LLP>
GenProducer::findPattern(const edm::Handle<reco::GenParticleCollection>& gen_particles) const
{
  if (debug)
    std::cout << "GenProducer: start looking for LLP pattern." << std::endl;
  
  bool found = false;
  std::vector<SoftDV::LLP> llps;
  for (size_t i=0; i<gen_particles->size(); ++i) {
    const reco::GenParticle& gen = gen_particles->at(i);
    std::vector<SoftDV::Particle> daus;
    if (gen.pdgId() == llp_id && gen.numberOfDaughters() == 3) {
      found = true;
      if (!gen.isLastCopy()) continue;
      if (debug)
        std::cout << "llp id: " << gen.pdgId() << " vertex " << gen.vertex().x() << " " << gen.vertex().y() << " " << gen.vertex().z() << " x " << gen.vx() << " y " << gen.vy() << " z "  << gen.vz() << std::endl;
      for (size_t j=0; j<gen.numberOfDaughters(); ++j) {
        SoftDV::Particle dau = SoftDV::Particle(gen.daughter(j)->pdgId(), gen.daughter(j)->charge(), gen.daughter(j)->polarP4(), gen.daughter(j)->vertex());
        daus.push_back(dau);
        if (debug)
          std::cout << "  daughter id: " << gen.daughter(j)->pdgId() << " vertex " << gen.daughter(j)->vertex().x() << " " << gen.daughter(j)->vertex().y() << " " << gen.daughter(j)->vertex().z() << " x " << gen.daughter(j)->vx() << " y " << gen.daughter(j)->vy() << " z "  << gen.daughter(j)->vz() << std::endl;
      }
    }
    SoftDV::LLP llp = SoftDV::LLP(gen.pdgId(),gen.charge(),gen.polarP4(),gen.vertex(),daus);
    if (found){
      llps.push_back(llp);
      found = false;
    }
  }
  return llps;
}

void GenProducer::produce(edm::Event& event, const edm::EventSetup&) {
  std::unique_ptr<std::vector<SoftDV::LLP>> llps(new std::vector<SoftDV::LLP>);
  
  if (!(event.isRealData())){
    edm::Handle<reco::GenParticleCollection> gen_particles;
    event.getByToken(gen_particles_token, gen_particles);

    std::vector<SoftDV::LLP> genllps = findPattern(gen_particles);
    for (auto& p: genllps){
      llps->push_back(p);
    }
  }
  event.put(std::move(llps));
}

DEFINE_FWK_MODULE(GenProducer);
