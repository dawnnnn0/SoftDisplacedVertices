#include "SoftDisplacedVertices/SoftDVDataFormats/interface/GenInfo.h"

double gen_dxy(const reco::GenParticle& gtk, const edm::Handle<reco::BeamSpot>& beamspot){
  // calculate dxy for gen track
  double r = 88.*gtk.pt();
  double cx = gtk.vx() + gtk.charge() * r * sin(gtk.phi());
  double cy = gtk.vy() - gtk.charge() * r * cos(gtk.phi());
  double dxy = fabs(r-sqrt(pow((cx-( beamspot->x0() )), 2) + pow((cy-( beamspot->y0() )), 2)));

  return dxy;
}

double gen_dz(const reco::GenParticle& gtk, const edm::Handle<reco::BeamSpot>& beamspot) {
  double rz = sqrt(pow((gtk.vx()-( beamspot->x0() )), 2) + pow((gtk.vy()-( beamspot->y0() )), 2));
  double z = gtk.vz() - beamspot->z0();
  double dz = z-rz*(gtk.pz()/gtk.pt());

  return dz;
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
