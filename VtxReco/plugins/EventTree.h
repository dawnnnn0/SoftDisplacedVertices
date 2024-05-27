#ifndef SoftDV_EventTree_h
#define SoftDV_EventTree_h

#include "TTree.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/METReco/interface/METFwd.h"
#include "DataFormats/METReco/interface/PFMET.h"
#include "DataFormats/METReco/interface/PFMETFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "RecoVertex/VertexTools/interface/VertexDistance3D.h"
#include "RecoVertex/VertexTools/interface/VertexDistanceXY.h"
#include "SoftDisplacedVertices/SoftDVDataFormats/interface/GenInfo.h"

struct eventInfo
{
  int n_vtx;
  int n_gen_vtx;
  int n_matched_vtx;
  std::vector<double> jet_pt;
  std::vector<double> jet_eta;
  std::vector<double> jet_phi;
  double met_pt;
  double met_phi;
  std::vector<double> llp_ctau;
  std::vector<bool> gen_vtx_match;
  std::vector<double> gen_vtx_lxy;
  std::vector<double> gen_vtx_dist;
  std::vector<int> gen_vtx_n_reco_matched_tk;
  std::vector<int> gen_vtx_n_gen_tk;
  std::vector<int> gen_vtx_n_matched_tk;
  std::vector<int> gen_vtx_n_matched_vtx;
  std::vector<bool> gen_vtx_match_by_dist;
  std::vector<int> vtx_match;
  std::vector<double> vtx_x;
  std::vector<double> vtx_y;
  std::vector<double> vtx_z;
  std::vector<double> vtx_ntracks;
  std::vector<double> vtx_ndof;
  std::vector<double> vtx_lxy;
  std::vector<double> vtx_lxy_err;
  std::vector<double> vtx_dphi_jet1;
  std::vector<double> vtx_dphi_met;
  std::vector<double> vtx_acollinearity;
  std::vector<double> matched_track_vx;
  std::vector<double> matched_track_vy;
  std::vector<double> matched_track_vz;
  std::vector<double> matched_track_pt;
  std::vector<double> matched_track_pt_err;
  std::vector<double> matched_track_eta;
  std::vector<double> matched_track_phi;
  std::vector<double> matched_track_dxybs;
  std::vector<double> matched_track_dxypv;
  std::vector<double> matched_track_dxy_err;
  std::vector<double> matched_track_dzbs;
  std::vector<double> matched_track_dzpv;
  std::vector<double> matched_track_dz_err;
  std::vector<double> matched_track_nhits;
  std::vector<double> matched_track_nlayers;
  std::vector<double> matched_track_normchi2;
  std::vector<double> matched_track_dphimet;
  std::vector<double> matched_track_dphijet;
  std::vector<double> matched_track_drjet;
};

template <class Jet, class MET>
class EventTree : public edm::one::EDAnalyzer<edm::one::SharedResources> {
  public:
    explicit EventTree(const edm::ParameterSet&);
    void analyze(const edm::Event&, const edm::EventSetup&);

  private:
    virtual void beginJob() override;
    virtual void endJob() override;
    void initEventStructure();
    
    const edm::EDGetTokenT<reco::BeamSpot> beamspot_token;
    const edm::EDGetTokenT<reco::VertexCollection> primary_vertex_token;
    const edm::EDGetTokenT<Jet> jet_token;
    const edm::EDGetTokenT<MET> met_token;
    const edm::EDGetTokenT<reco::VertexCollection> vtx_token;
    const edm::EDGetTokenT<std::vector<SoftDV::LLP>> llp_gen_token;
    const edm::EDGetTokenT<std::vector<reco::TrackCollection>> gen_matched_track_token;
    
    bool debug;

    TTree *eventTree;
    eventInfo *evInfo;

    VertexDistanceXY distcalc_2d;
    VertexDistance3D distcalc_3d;
};

template <class Jet, class MET>
EventTree<Jet, MET>::EventTree(const edm::ParameterSet& cfg)
  : beamspot_token(consumes<reco::BeamSpot>(cfg.getParameter<edm::InputTag>("beamspot_token"))),
    primary_vertex_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("primary_vertex_token"))),
    jet_token(consumes<Jet>(cfg.getParameter<edm::InputTag>("jet_token"))),
    met_token(consumes<MET>(cfg.getParameter<edm::InputTag>("met_token"))),
    vtx_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("vtx_token"))),
    llp_gen_token(consumes<std::vector<SoftDV::LLP>>(cfg.getParameter<edm::InputTag>("llp_gen_token"))),
    gen_matched_track_token(consumes<std::vector<std::vector<reco::Track>>>(cfg.getParameter<edm::InputTag>("gen_matched_track_token"))),
    debug(cfg.getParameter<bool>("debug"))
{
  usesResource("TFileService");

  evInfo = new eventInfo;
}

template <class Jet, class MET>
void EventTree<Jet, MET>::analyze(const edm::Event& event, const edm::EventSetup&) {
  initEventStructure();
  edm::Handle<Jet> jets;
  event.getByToken(jet_token, jets);

  edm::Handle<MET> mets;
  event.getByToken(met_token, mets);

  edm::Handle<reco::BeamSpot> beamspot;
  event.getByToken(beamspot_token, beamspot);

  const reco::Vertex fake_bs_vtx(beamspot->position(), beamspot->covariance3D());

  edm::Handle<reco::VertexCollection> primary_vertices;
  event.getByToken(primary_vertex_token, primary_vertices);
  const reco::Vertex* primary_vertex = 0;
  if (primary_vertices->size())
    primary_vertex = &primary_vertices->at(0);

  edm::Handle<reco::VertexCollection> vertices;
  event.getByToken(vtx_token, vertices);

  edm::Handle<std::vector<SoftDV::LLP>> genllps;
  event.getByToken(llp_gen_token, genllps);

  edm::Handle<std::vector<std::vector<reco::Track>>> matched_tracks;
  event.getByToken(gen_matched_track_token, matched_tracks);

  int jet_leading_idx = -1;
  double jet_pt_max = -1;
  for(size_t ijet=0; ijet<jets->size(); ++ijet){
    const auto& jet = jets->at(ijet);
    evInfo->jet_pt.push_back(jet.pt());
    evInfo->jet_eta.push_back(jet.eta());
    evInfo->jet_phi.push_back(jet.phi());
    if (jet.pt()>jet_pt_max) {
      jet_leading_idx = ijet;
      jet_pt_max = jet.pt();
    }
  }

  const auto& met = mets->at(0);
  evInfo->met_pt = met.pt();
  evInfo->met_phi = met.phi();


  //const reco::PFJet& leading_jet = jets->at(jet_leading_idx);
  const auto& leading_jet = jets->at(jet_leading_idx);

  //int n_match = 0;
  int n_gen_vtx = 0;
  //std::vector<int> match_idx;
  std::vector<int> n_matched_vertices(genllps->size(),0);
  std::vector<std::vector<int>> match_index;
  std::vector<int> n_matched_tracks(genllps->size(),0);
  std::vector<double> matched_distance(genllps->size(),999);
  for(size_t illp=0; illp<genllps->size(); ++illp){
    const auto& llp = genllps->at(illp);
    if (!llp.valid()) continue;
    ++n_gen_vtx;

    double ctau = llp.ct(primary_vertex->position());
    evInfo->llp_ctau.push_back(ctau);

    math::XYZPoint llp_decay = llp.decay_point();
    math::XYZPoint bs_pos = fake_bs_vtx.position();
    math::XYZVector l_bs2vtx_gen = llp_decay - bs_pos;
    double gen_vtx_lxy = std::sqrt(l_bs2vtx_gen.Mag2());
    evInfo->gen_vtx_lxy.push_back(gen_vtx_lxy);
    //SoftDV::Point llp_decay = llp.decay_point(0);
    //double min_dist = 999;
    //size_t min_ivtx = 999;
    bool gen_matched = false;
    bool gen_matched_dist = false;
    std::vector<int> match_vtx_idx;
    const auto m_tracks = matched_tracks->at(illp);
    evInfo->gen_vtx_n_reco_matched_tk.push_back(m_tracks.size());
    evInfo->gen_vtx_n_gen_tk.push_back(llp.getGenTracks().size());
    for (const auto& m_tk:m_tracks){
      evInfo->matched_track_vx.push_back(m_tk.vx());
      evInfo->matched_track_vy.push_back(m_tk.vy());
      evInfo->matched_track_vz.push_back(m_tk.vz());
      evInfo->matched_track_pt.push_back(m_tk.pt());
      evInfo->matched_track_pt_err.push_back(m_tk.ptError());
      evInfo->matched_track_eta.push_back(m_tk.eta());
      evInfo->matched_track_phi.push_back(m_tk.phi());
      evInfo->matched_track_dxybs.push_back(m_tk.dxy(*beamspot));
      evInfo->matched_track_dxypv.push_back(m_tk.dxy(primary_vertex->position()));
      evInfo->matched_track_dxy_err.push_back(m_tk.dxyError());
      evInfo->matched_track_dzbs.push_back(m_tk.dz((*beamspot).position()));
      evInfo->matched_track_dzpv.push_back(m_tk.dz(primary_vertex->position()));
      evInfo->matched_track_dz_err.push_back(m_tk.dzError());
      evInfo->matched_track_nhits.push_back(m_tk.hitPattern().numberOfValidHits());
      evInfo->matched_track_nlayers.push_back(m_tk.hitPattern().trackerLayersWithMeasurement());
      evInfo->matched_track_normchi2.push_back(m_tk.normalizedChi2());
      evInfo->matched_track_dphimet.push_back(reco::deltaPhi(m_tk.phi(), met.phi()));
      evInfo->matched_track_dphijet.push_back(reco::deltaPhi(m_tk.phi(), leading_jet.phi()));
      evInfo->matched_track_drjet.push_back(reco::deltaR(m_tk.eta(),m_tk.phi(),leading_jet.eta(),leading_jet.phi()));
    }

    if (debug) {
      std::cout << "LLP " << illp << " matched tracks " << std::endl;
      for (const auto& m_tk:m_tracks){
        std::cout << "  pt: " << m_tk.pt() << " eta: " << m_tk.eta() << " phi: " << m_tk.phi() << std::endl; 
      }
    }

    // match vertices by matching tracks
    for (size_t ivtx=0; ivtx<vertices->size(); ++ivtx) {
      const reco::Vertex& vtx = vertices->at(ivtx);
      double match_threshold = 1.3;
      // for each LLP, compare the matched tracks with tracks in the reco vertex 
      
      if (debug){
        std::cout << "reco vertex " << ivtx << " matched tracks " << std::endl;
        for (auto v_tk = vtx.tracks_begin(), vtke = vtx.tracks_end(); v_tk != vtke; ++v_tk){
          std::cout << "  pt: " << (*v_tk)->pt() << " eta: " << (*v_tk)->eta() << " phi: " << (*v_tk)->phi() << std::endl;
        }
      }

      int n_matched = 0;
      for (const auto& m_tk:m_tracks){
        for (auto v_tk = vtx.tracks_begin(), vtke = vtx.tracks_end(); v_tk != vtke; ++v_tk){
          double dpt = fabs(m_tk.pt() - (*v_tk)->pt()) + 1;
          double deta = fabs(m_tk.eta() - (*v_tk)->eta()) + 1;
          double dphi = fabs(m_tk.phi() - (*v_tk)->phi()) + 1;
          if (dpt * deta * dphi < match_threshold){
            n_matched += 1;
            if (debug) {
              std::cout << "  track matched: " << std::endl;
              std::cout << "  |->  gen pt " << m_tk.pt() << " eta " << m_tk.eta() << " phi " << m_tk.phi() << std::endl;
              std::cout << "  --> reco pt " << (*v_tk)->pt() << " eta " << (*v_tk)->eta() << " phi " << (*v_tk)->phi() << std::endl;
            }
            break;
          }
        }
      }
      if (debug){
        std::cout << "matched tracks " << n_matched << std::endl;
      }
      if (n_matched==0) continue;
      gen_matched = true;
      n_matched_vertices[illp] += 1;
      match_vtx_idx.push_back(ivtx);
      math::XYZPoint vtx_pos = vtx.position();
      math::XYZVector l_vtx_gen = vtx_pos-llp_decay;
      double gen_dist = std::sqrt(l_vtx_gen.Perp2());
      if (n_matched_tracks[illp]<n_matched){
        n_matched_tracks[illp] = n_matched;
        matched_distance[illp] = gen_dist;
      }
      else if ((n_matched_tracks[illp]==n_matched) && (matched_distance[illp]>gen_dist)){
        matched_distance[illp] = gen_dist;
      }
    }
    match_index.push_back(match_vtx_idx);
    evInfo->gen_vtx_match.push_back(gen_matched);


    for(size_t ivtx=0; ivtx<vertices->size(); ++ivtx) {
      //if(std::find(match_idx.begin(), match_idx.end(), ivtx) != match_idx.end())
      //  continue;
      const reco::Vertex& vtx = vertices->at(ivtx);
      const auto d_gen = gen_dist(vtx,llp_decay,true);
      double d_gen_sig = fabs(d_gen.significance());
      if (d_gen_sig<10) {
        gen_matched_dist = true;
        break;
      }
      //math::XYZPoint vtx_pos = vtx.position();
      //math::XYZVector l_vtx_gen = vtx_pos-llp_decay;
      //double gen_dist = std::sqrt(l_vtx_gen.Perp2());
      //if (gen_dist<min_dist){
      //  min_dist = gen_dist;
      //  min_ivtx = ivtx;
      //}
    }
    //if (min_dist<0.01) {
    //  n_match += 1;
    //  match_idx.push_back(min_ivtx);
    //  gen_matched_dist = true;
    //}
    //evInfo->gen_vtx_dist.push_back(min_dist);
    //evInfo->gen_vtx_match.push_back(gen_matched);
    evInfo->gen_vtx_match_by_dist.push_back(gen_matched_dist);
  }
  evInfo->n_gen_vtx = n_gen_vtx;
  evInfo->gen_vtx_dist = matched_distance;
  evInfo->gen_vtx_n_matched_tk = n_matched_tracks;
  evInfo->gen_vtx_n_matched_vtx = n_matched_vertices;
  //evInfo->n_matched_vtx = n_match;

  if (debug){
    std::cout << "matched index:" << std::endl;
    for (const auto& m:match_index) {
      for (const auto& mm:m){
        std::cout << mm << " ";
      }
      std::cout << std::endl;
    }
  }


  evInfo->n_vtx = vertices->size();
  for(size_t ivtx=0; ivtx<vertices->size(); ++ivtx) {
    int matched = -1;
    for (size_t illp=0; illp<genllps->size(); ++illp){
      if(std::find(match_index[illp].begin(), match_index[illp].end(), ivtx) != match_index[illp].end()) {
        if (matched==-1)
          matched = illp;
        else
          matched = 10;
      }
    }
    evInfo->vtx_match.push_back(matched);
    const reco::Vertex& vtx = vertices->at(ivtx);
    math::XYZVector l_vector = vtx.position() - beamspot->position();
    const auto d = distcalc_2d.distance(vtx, fake_bs_vtx);

    evInfo->vtx_x.push_back(vtx.x());
    evInfo->vtx_y.push_back(vtx.y());
    evInfo->vtx_z.push_back(vtx.z());
    evInfo->vtx_ntracks.push_back(vtx.tracksSize());
    evInfo->vtx_ndof.push_back(vtx.normalizedChi2());
    evInfo->vtx_lxy.push_back(d.value());
    evInfo->vtx_lxy_err.push_back(d.error());
    evInfo->vtx_dphi_jet1.push_back(reco::deltaPhi(l_vector, leading_jet));
    evInfo->vtx_dphi_met.push_back(reco::deltaPhi(l_vector, met));
    evInfo->vtx_acollinearity.push_back(reco::deltaPhi(l_vector, vtx.p4()));
  }

  eventTree->Fill();

}

template <class Jet, class MET>
void EventTree<Jet, MET>::beginJob()
{
  edm::Service<TFileService> fs;
  eventTree = fs->make<TTree>( "tree_DV", "tree_DV" );

  eventTree->Branch("n_vtx",      &evInfo->n_vtx);
  eventTree->Branch("n_gen_vtx",  &evInfo->n_gen_vtx);
  eventTree->Branch("n_matched_vtx",      &evInfo->n_matched_vtx);
  eventTree->Branch("jet_pt",     &evInfo->jet_pt);
  eventTree->Branch("jet_eta",    &evInfo->jet_eta);
  eventTree->Branch("jet_phi",    &evInfo->jet_phi);
  eventTree->Branch("met_pt",     &evInfo->met_pt);
  eventTree->Branch("met_phi",    &evInfo->met_phi);
  eventTree->Branch("llp_ctau",   &evInfo->llp_ctau);
  eventTree->Branch("gen_vtx_match",      &evInfo->gen_vtx_match);
  eventTree->Branch("gen_vtx_lxy",      &evInfo->gen_vtx_lxy);
  eventTree->Branch("gen_vtx_dist",      &evInfo->gen_vtx_dist);
  eventTree->Branch("gen_vtx_n_reco_matched_tk", &evInfo->gen_vtx_n_reco_matched_tk);
  eventTree->Branch("gen_vtx_n_gen_tk", &evInfo->gen_vtx_n_gen_tk);
  eventTree->Branch("gen_vtx_n_matched_tk", &evInfo->gen_vtx_n_matched_tk);
  eventTree->Branch("gen_vtx_n_matched_vtx", &evInfo->gen_vtx_n_matched_vtx);
  eventTree->Branch("gen_vtx_match_by_dist", &evInfo->gen_vtx_match_by_dist);
  eventTree->Branch("vtx_match",      &evInfo->vtx_match);
  eventTree->Branch("vtx_x",      &evInfo->vtx_x);
  eventTree->Branch("vtx_y",      &evInfo->vtx_y);
  eventTree->Branch("vtx_z",      &evInfo->vtx_z);
  eventTree->Branch("vtx_ntracks",&evInfo->vtx_ntracks);
  eventTree->Branch("vtx_ndof",   &evInfo->vtx_ndof);
  eventTree->Branch("vtx_lxy",    &evInfo->vtx_lxy);
  eventTree->Branch("vtx_lxy_err",&evInfo->vtx_lxy_err);
  eventTree->Branch("vtx_dphi_jet1", &evInfo->vtx_dphi_jet1);
  eventTree->Branch("vtx_dphi_met",  &evInfo->vtx_dphi_met);
  eventTree->Branch("vtx_acollinearity", &evInfo->vtx_acollinearity);
  eventTree->Branch("matched_track_vx",       &evInfo->matched_track_vx);
  eventTree->Branch("matched_track_vy",       &evInfo->matched_track_vy);
  eventTree->Branch("matched_track_vz",       &evInfo->matched_track_vz);
  eventTree->Branch("matched_track_pt",       &evInfo->matched_track_pt);
  eventTree->Branch("matched_track_pt_err",   &evInfo->matched_track_pt_err);
  eventTree->Branch("matched_track_eta",      &evInfo->matched_track_eta);
  eventTree->Branch("matched_track_phi",      &evInfo->matched_track_phi);
  eventTree->Branch("matched_track_dxybs",    &evInfo->matched_track_dxybs);
  eventTree->Branch("matched_track_dxypv",    &evInfo->matched_track_dxypv);
  eventTree->Branch("matched_track_dxy_err",  &evInfo->matched_track_dxy_err);
  eventTree->Branch("matched_track_dzbs",     &evInfo->matched_track_dzbs);
  eventTree->Branch("matched_track_dzpv",     &evInfo->matched_track_dzpv);
  eventTree->Branch("matched_track_dz_err",   &evInfo->matched_track_dz_err);
  eventTree->Branch("matched_track_nhits",    &evInfo->matched_track_nhits);
  eventTree->Branch("matched_track_nlayers",  &evInfo->matched_track_nlayers);
  eventTree->Branch("matched_track_normchi2", &evInfo->matched_track_normchi2);
  eventTree->Branch("matched_track_dphimet",  &evInfo->matched_track_dphimet);
  eventTree->Branch("matched_track_dphijet",  &evInfo->matched_track_dphijet);
  eventTree->Branch("matched_track_drjet",    &evInfo->matched_track_drjet);

}

template <class Jet, class MET>
void EventTree<Jet, MET>::endJob()
{}

template <class Jet, class MET>
void EventTree<Jet, MET>::initEventStructure()
{
  evInfo->n_vtx = -1;
  evInfo->n_gen_vtx = -1;
  evInfo->n_matched_vtx = -1;
  evInfo->jet_pt.clear();
  evInfo->jet_eta.clear();
  evInfo->jet_phi.clear();
  evInfo->met_pt = -1;
  evInfo->met_phi = -1;
  evInfo->llp_ctau.clear();
  evInfo->gen_vtx_match.clear();
  evInfo->gen_vtx_lxy.clear();
  evInfo->gen_vtx_dist.clear();
  evInfo->gen_vtx_n_reco_matched_tk.clear();
  evInfo->gen_vtx_n_gen_tk.clear();
  evInfo->gen_vtx_n_matched_tk.clear();
  evInfo->gen_vtx_n_matched_vtx.clear();
  evInfo->gen_vtx_match_by_dist.clear();
  evInfo->vtx_match.clear();
  evInfo->vtx_x.clear();
  evInfo->vtx_y.clear();
  evInfo->vtx_z.clear();
  evInfo->vtx_ntracks.clear();
  evInfo->vtx_ndof.clear();
  evInfo->vtx_lxy.clear();
  evInfo->vtx_lxy_err.clear();
  evInfo->vtx_dphi_jet1.clear();
  evInfo->vtx_dphi_met.clear();
  evInfo->vtx_acollinearity.clear();
  evInfo->matched_track_vx.clear();
  evInfo->matched_track_vy.clear();
  evInfo->matched_track_vz.clear();
  evInfo->matched_track_pt.clear();
  evInfo->matched_track_pt_err.clear();
  evInfo->matched_track_eta.clear();
  evInfo->matched_track_phi.clear();
  evInfo->matched_track_dxybs.clear();
  evInfo->matched_track_dxypv.clear();
  evInfo->matched_track_dxy_err.clear();
  evInfo->matched_track_dzbs.clear();
  evInfo->matched_track_dzpv.clear();
  evInfo->matched_track_dz_err.clear();
  evInfo->matched_track_nhits.clear();
  evInfo->matched_track_nlayers.clear();
  evInfo->matched_track_normchi2.clear();
  evInfo->matched_track_dphimet.clear();
  evInfo->matched_track_dphijet.clear();
  evInfo->matched_track_drjet.clear();
}

#endif
