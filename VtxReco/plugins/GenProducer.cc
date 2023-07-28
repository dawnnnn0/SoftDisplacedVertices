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
#include "RecoVertex/VertexTools/interface/VertexDistance3D.h"
#include "RecoVertex/VertexTools/interface/VertexDistanceXY.h"
#include "SoftDisplacedVertices/SoftDVDataFormats/interface/GenInfo.h"


class GenProducer : public edm::EDProducer {
  public:
    explicit GenProducer(const edm::ParameterSet&);
  private:
    void produce(edm::Event&, const edm::EventSetup&) override;
    const edm::EDGetTokenT<reco::GenParticleCollection> gen_particles_token;
    const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
    int llp_id;
    int lsp_id;
    bool debug;

    std::vector<SoftDV::LLP> findPattern(const edm::Handle<reco::GenParticleCollection>& gen_particles, const edm::Handle<reco::BeamSpot>& beamspot) const;

    VertexDistanceXY distcalc_2d;
    VertexDistance3D distcalc_3d;
};

GenProducer::GenProducer(const edm::ParameterSet& cfg)
  : gen_particles_token(consumes<reco::GenParticleCollection>(cfg.getParameter<edm::InputTag>("gen_particles_token"))),
    beamspot_token(consumes<reco::BeamSpot>(cfg.getParameter<edm::InputTag>("beamspot_token"))),
    llp_id(cfg.getParameter<int>("llp_id")),
    lsp_id(cfg.getParameter<int>("lsp_id")),
    debug(cfg.getParameter<bool>("debug"))
{
  produces<std::vector<SoftDV::LLP>>();
}

std::vector<SoftDV::LLP>
GenProducer::findPattern(const edm::Handle<reco::GenParticleCollection>& gen_particles, const edm::Handle<reco::BeamSpot>& beamspot) const
{
  if (debug)
    std::cout << "GenProducer: start looking for LLP pattern." << std::endl;
  
  bool found = false;
  std::vector<SoftDV::LLP> llps;
  for (size_t i=0; i<gen_particles->size(); ++i) {
    const reco::GenParticle& gen = gen_particles->at(i);
    std::vector<SoftDV::Particle> daus;
    if (abs(gen.pdgId()) == llp_id && gen.numberOfDaughters() == 3) {
      if (!gen.isLastCopy()) continue;
      if (debug)
        std::cout << "llp id: " << gen.pdgId() << " vertex " << gen.vertex().x() << " " << gen.vertex().y() << " " << gen.vertex().z() << std::endl;
      for (size_t j=0; j<gen.numberOfDaughters(); ++j) {
        if (abs(gen.daughter(j)->pdgId())==lsp_id){
          found = true;
        }
        if (gen.daughter(j)->pdgId()==llp_id){
          if (debug){
            std::cout << "!!! Found LLP daughter still the LLP, so discard the previous LLP." << std::endl;
          }
          found = false;
          break;
        }
        SoftDV::Particle dau = SoftDV::Particle(gen.daughter(j)->pdgId(), gen.daughter(j)->charge(), gen.daughter(j)->polarP4(), gen.daughter(j)->vertex());
        daus.push_back(dau);
        if (debug)
          std::cout << "|->  daughter id: " << gen.daughter(j)->pdgId() << " vertex " << gen.daughter(j)->vertex().x() << " " << gen.daughter(j)->vertex().y() << " " << gen.daughter(j)->vertex().z() << std::endl;
      }
    }
    SoftDV::LLP llp = SoftDV::LLP(gen.pdgId(),gen.charge(),gen.polarP4(),gen.vertex(),daus);
    if (!llp.valid()) continue;

    // Look for charged gen particles that originate in the LLP decay
    std::vector<reco::GenParticle> gtks;
    for (size_t i=0; i<gen_particles->size(); ++i) {
      const reco::GenParticle& gtk = gen_particles->at(i);
      if (gtk.status()!=1) continue;
      if ( (gtk.charge()==0) || (fabs(gtk.charge())<1) ) continue;
      if (gtk.pt()<0.5 || fabs(gtk.eta()) > 2.5 ) continue;
      double r = 88.*gtk.pt();
      double cx = gtk.vx() + gtk.charge() * r * sin(gtk.phi());
      double cy = gtk.vy() - gtk.charge() * r * cos(gtk.phi());
      double dxy_gen = fabs(r-sqrt(pow((cx-( beamspot->x0() )), 2) + pow((cy-( beamspot->y0() )), 2)));
      if (dxy_gen<0.005) continue;
      math::XYZVector dl = gtk.vertex() - llp.decay_point();
      double d3d = std::sqrt(dl.Mag2());
      if (d3d < 0.005){
        gtks.push_back(gtk);
        if (debug){
          std::cout << "  " << gtk.vertex().x() << " " << gtk.vertex().y() << " " << gtk.vertex().z() << std::endl;
        }
      }
    }
    llp.gen_tracks = gtks;

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

    edm::Handle<reco::BeamSpot> beamspot;
    event.getByToken(beamspot_token, beamspot);

    std::vector<SoftDV::LLP> genllps = findPattern(gen_particles, beamspot);
    for (auto& p: genllps){
      llps->push_back(p);
    }
  }
  event.put(std::move(llps));
}

DEFINE_FWK_MODULE(GenProducer);
