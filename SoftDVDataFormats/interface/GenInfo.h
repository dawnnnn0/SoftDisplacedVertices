#ifndef SoftDVDataFormats_GenInfo_h
#define SoftDVDataFormats_GenInfo_h

#include <vector>
#include <cmath>
#include "DataFormats/Math/interface/Point3D.h"
#include "DataFormats/Math/interface/Vector3D.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/GeometryCommonDetAlgo/interface/Measurement1D.h"

namespace SoftDV {

  typedef math::XYZPoint Point;
  typedef math::XYZVector Vector;
  typedef math::PtEtaPhiMLorentzVector PolarLorentzVector;

  struct Particle {
    int pdgid;
    double charge;
    PolarLorentzVector polarp4;
    Point vertex;

    Particle():
      pdgid(-999), charge(-999), polarp4(PolarLorentzVector()), vertex(Point()) {}
    Particle(int pdgid, double charge, PolarLorentzVector polarp4, Point vertex):
      pdgid(pdgid), charge(charge), polarp4(polarp4), vertex(vertex){}
    bool valid() const {return (pdgid!=-999 || charge!=-999);}
  };

  struct LLP : public Particle {
    std::vector<Particle> decay_products;
    std::vector<reco::GenParticle> gen_tracks;

    LLP():
      Particle(),decay_products(std::vector<Particle>()),gen_tracks(std::vector<reco::GenParticle>()) {}
    LLP(int pdgid, double charge, PolarLorentzVector polarp4, Point vertex, std::vector<Particle> decay_products):
      Particle(pdgid,charge,polarp4,vertex),decay_products(decay_products),gen_tracks(std::vector<reco::GenParticle>()) {}
    bool valid() const {return decay_products.size()>0;}
    Point decay_point(size_t i=0) const {
      if (!(i<decay_products.size()))
        throw std::invalid_argument("parameter i out of range!");
      return decay_products[i].vertex;
    }

    Vector flight(Point pv) const {
      if (!valid())
        throw std::invalid_argument("LLP not valid!");
      Vector gen_vec = Vector(pv);
      Vector decay_vec = Vector(decay_point(0));
      return decay_vec - gen_vec;
    }
    double ct(Point pv) const { return std::sqrt(flight(pv).Mag2())/polarp4.Beta()/polarp4.Gamma();}
    //void addGenTracks(std::vector<reco::GenParticle> gts){ self.gen_tracks = gts;}
    std::vector<reco::GenParticle> getGenTracks() const {return gen_tracks;}
  };

  class GenInfo {
    public:
      GenInfo() {}

      int getNumberOfLLPs() {return llps_.size();}
      std::vector<LLP> getLLPs() {return llps_;}
      LLP getLLP(size_t i) {
        if (!(i<llps_.size()))
          throw std::invalid_argument("parameter i out of range!");
        return llps_[i];
      }

      void addLLP(LLP llp) {
        //maybe would be nice if this method checks whether the llp is already added
        llps_.push_back(llp);
      }

    private:
      std::vector<LLP> llps_;
  };


}
double gen_dxy(const reco::GenParticle& gtk, const edm::Handle<reco::BeamSpot>& beamspot); 
double gen_dz(const reco::GenParticle& gtk, const edm::Handle<reco::BeamSpot>& beamspot);

Measurement1D gen_dist(const reco::Vertex& sv, const SoftDV::Point& gen, const bool use3d);

#endif
