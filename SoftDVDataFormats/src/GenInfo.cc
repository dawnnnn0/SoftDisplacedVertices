#include "SoftDisplacedVertices/SoftDVDataFormats/interface/GenInfo.h"

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
