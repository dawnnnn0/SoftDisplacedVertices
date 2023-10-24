#include <queue>
#include "SoftDisplacedVertices/SoftDVDataFormats/interface/GenInfo.h"

reco::GenParticleRef SoftDV::get_gen(const reco::Candidate* c, const edm::Handle<reco::GenParticleCollection>& gens) {
  if (c != 0) {
    for (int i = 0, ie = int(gens->size()); i < ie; ++i) {
      const reco::GenParticle& gen = gens->at(i);
      if (&gen == c)
        return reco::GenParticleRef(gens, i);
    }
  }
  return reco::GenParticleRef();
}


std::vector<int> SoftDV::FindLLP(const edm::Handle<reco::GenParticleCollection>& gen_particles, int LLP_id, int LSP_id, bool debug){
  if (debug)
    std::cout << "Start looking for LLP." << std::endl;

  bool found = false;
  std::vector<int> llps;
  for (size_t i=0; i<gen_particles->size(); ++i) {
    const reco::GenParticle& gen = gen_particles->at(i);
    if (abs(gen.pdgId()) == LLP_id) {
      if (!gen.isLastCopy()) continue;
      if (debug)
        std::cout << "llp id: " << gen.pdgId() << " vertex " << gen.vertex().x() << " " << gen.vertex().y() << " " << gen.vertex().z() << std::endl;
      for (size_t j=0; j<gen.numberOfDaughters(); ++j) {
        if (abs(gen.daughter(j)->pdgId())==LSP_id){
          found = true;
        }
        if (gen.daughter(j)->pdgId()==LLP_id){
          if (debug){
            std::cout << "!!! Found LLP daughter still the LLP, so discard the previous LLP." << std::endl;
          }
          found = false;
          break;
        }
      }
    }
    if (found){
      if (debug)
        std::cout << "LLP found." << std::endl;
      llps.push_back(i);
      found = false;
    }
  }

  if (debug){
    std::cout << "Total LLPs: " << llps.size() << std::endl;
  }
  return llps;
  
}

std::vector<int> SoftDV::GetDaughters(const size_t igen, const edm::Handle<reco::GenParticleCollection>& gen_particles, bool debug) {
  const reco::GenParticle gen = gen_particles->at(igen);
  std::queue<reco::GenParticleRef> gen_daughter_queue;
  std::vector<int> processed_gen_key;
  std::vector<int> llp_daus;
  //reco::GenParticleCollection llp_daus;
  std::vector<reco::GenParticle> gtks;

  // Use GenParticleRef to check duplication
  //const auto& llp_ref = reco::GenParticleRef(gen_particles, i);
  if (debug)
    std::cout << "Start looking for daughters." << std::endl;
  //const auto& llp_ref = SoftDV::get_gen(&gen, gen_particles);
  const auto& llp_ref = reco::GenParticleRef(gen_particles, igen);
  if (debug)
    std::cout << "Get LLP reference." << std::endl;
  if (!llp_ref)
    std::cout << "CANNOT FIND LLP REFERENCE!" << std::endl;
  gen_daughter_queue.push(llp_ref);
  processed_gen_key.push_back(llp_ref.key());
  while (!gen_daughter_queue.empty()) {
    reco::GenParticleRef dau = gen_daughter_queue.front();
    if (debug) {
      std::cout << "  Daughter " << dau->pdgId() << " status " << dau->status() << " charge " << dau->charge() << std::endl;
    }
    gen_daughter_queue.pop();
    if ( (dau->status()==1) && (dau->charge()!=0)){
      if (dau.isNonnull()){
        llp_daus.push_back(dau.key());
        //llp_daus.push_back(*(dau.get()));
      }
      if (debug){
        std::cout << "  Final status gen daughter added. ID " << dau->pdgId() << " pt " << dau->pt() << " eta " << dau->eta() << " phi " << dau->phi() << std::endl;
      }
      if (dau->numberOfDaughters()>0){
        std::cout << "GenProducer: Gen daughter with status 1 has daughters!" << std::endl;
      }
      continue;
    }
    for (size_t idau=0; idau<dau->numberOfDaughters(); ++idau){
      const auto& gendau = SoftDV::get_gen(dau->daughter(idau), gen_particles);
      if (!gendau)
        continue;
      int gendau_key = gendau.key();
      if (debug){
        std::cout << "    daughter " << gendau->pdgId() << " status " << gendau->status() << " key " << gendau_key << std::endl;
      }
      if(std::find(processed_gen_key.begin(), processed_gen_key.end(), gendau_key) != processed_gen_key.end()) {
        if (debug)
          std::cout << "     Is was processed before so skipping..." << std::endl;
        continue;
      }
      gen_daughter_queue.push(gendau);
      processed_gen_key.push_back(gendau.key());
    }
  
  }
  return llp_daus;

}

double gen_dxy(const reco::GenParticle& gtk, const SoftDV::Point& refpoint){
  // calculate dxy for gen track
  double r = 88.*gtk.pt();
  double cx = gtk.vx() + gtk.charge() * r * sin(gtk.phi());
  double cy = gtk.vy() - gtk.charge() * r * cos(gtk.phi());
  double dxy = fabs(r-sqrt(pow((cx-( refpoint.x() )), 2) + pow((cy-( refpoint.y() )), 2)));

  return dxy;
}

double gen_dz(const reco::GenParticle& gtk, const SoftDV::Point& refpoint) {
  double rz = sqrt(pow((gtk.vx()-( refpoint.x() )), 2) + pow((gtk.vy()-( refpoint.y() )), 2));
  double z = gtk.vz() - refpoint.z();
  double dz = z-rz*(gtk.pz()/gtk.pt());

  return dz;
}

double gen_dxy_reco(const reco::GenParticle& gtk, const SoftDV::Point& refpoint) {
  return (-(gtk.vx() - refpoint.x()) * gtk.py() + (gtk.vy() - refpoint.y()) * gtk.px()) / gtk.pt();
}

Measurement1D gen_dist(const reco::Vertex& sv, const SoftDV::Point& gen, const bool use3d) {
  math::XYZPoint sv_pos = sv.position();
  math::XYZVector l_sv_gen = sv_pos - gen;
  double d = sqrt(l_sv_gen.Mag2());
  AlgebraicVector3 v(sv.x(), sv.y(), use3d ? sv.z() : 0);
  const double dist2 = ROOT::Math::Mag2(v);
  const double sim  = ROOT::Math::Similarity(v, sv.covariance());
  const double ed = dist2 != 0 ? sqrt(sim/dist2) : 0;
  return Measurement1D(d, ed);
}
