#include "FWCore/Framework/interface/global/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "DataFormats/NanoAOD/interface/FlatTable.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include <vector>
#include <iostream>

class TrackVertexMatchTableProducer : public edm::global::EDProducer<> {
  public:
    TrackVertexMatchTableProducer(edm::ParameterSet const& params)
      : objName_(params.getParameter<std::string>("objName")),
        branchName_(params.getParameter<std::string>("branchName")),
        doc_(params.getParameter<std::string>("docString")),
        src_(consumes<reco::TrackCollection>(params.getParameter<edm::InputTag>("src"))),
        vtx_(consumes<reco::VertexCollection>(params.getParameter<edm::InputTag>("vtx"))),
        debug(params.getParameter<bool>("debug"))
    {
        produces<nanoaod::FlatTable>();
    }

    ~TrackVertexMatchTableProducer() override {}

    void produce(edm::StreamID id, edm::Event& iEvent, const edm::EventSetup& iSetup) const override {
      const auto& tracks = iEvent.get(src_);
      auto ntrack = tracks.size();
      auto tab = std::make_unique<nanoaod::FlatTable>(ntrack, objName_, false, true);
      
      const auto& vertices = iEvent.get(vtx_);

      std::vector<int> key(ntrack, -1);

      if (debug) {
        std::cout << "SVs " << vertices.size() << std::endl;
        for (size_t ivtx=0; ivtx<vertices.size(); ++ivtx) {
            const reco::Vertex& vtx = vertices.at(ivtx);
            std::cout << "reco vertex " << ivtx << " x: " << vtx.x() << " y: " << vtx.y() << " z: " << vtx.z()  << " tracks " << std::endl;
            for (auto v_tk = vtx.tracks_begin(), vtke = vtx.tracks_end(); v_tk != vtke; ++v_tk){
              std::cout << "  pt: " << (*v_tk)->pt() << " eta: " << (*v_tk)->eta() << " phi: " << (*v_tk)->phi() << std::endl;
            }
        }

      }

      for (size_t i = 0; i < ntrack; ++i) {
        const auto& tk = tracks.at(i);
        if (debug){
          std::cout << "reco track " << i << " pt " << tk.pt() << " eta " << tk.eta() << " phi " << tk.phi() << std::endl;
        }
        // match vertices by matching tracks
        // FIXME: This algorithm assumes tracks are not reused for different vertices, so it might be a problem when it is not the case
        int matched_vtx_idx = -1;
        for (size_t ivtx=0; ivtx<vertices.size(); ++ivtx) {
          const reco::Vertex& vtx = vertices.at(ivtx);
          double match_threshold = 1.1;
          // for each LLP, compare the matched tracks with tracks in the reco vertex 
          
          if (debug){
            std::cout << "reco vertex " << ivtx << " x: " << vtx.x() << " y: " << vtx.y() << " z: " << vtx.z()  << " tracks " << std::endl;
            for (auto v_tk = vtx.tracks_begin(), vtke = vtx.tracks_end(); v_tk != vtke; ++v_tk){
              std::cout << "  pt: " << (*v_tk)->pt() << " eta: " << (*v_tk)->eta() << " phi: " << (*v_tk)->phi() << std::endl;
            }
          }

          for (auto v_tk = vtx.tracks_begin(), vtke = vtx.tracks_end(); v_tk != vtke; ++v_tk){
            double dpt = fabs(tk.pt() - (*v_tk)->pt()) + 1;
            double deta = fabs(tk.eta() - (*v_tk)->eta()) + 1;
            double dphi = fabs(tk.phi() - (*v_tk)->phi()) + 1;
            if (dpt * deta * dphi < match_threshold){
              matched_vtx_idx = (int) ivtx;
              if (debug) {
                std::cout << "  track matched: " << std::endl;
                std::cout << "  |->  gen pt " << tk.pt() << " eta " << tk.eta() << " phi " << tk.phi() << std::endl;
                std::cout << "  --> reco pt " << (*v_tk)->pt() << " eta " << (*v_tk)->eta() << " phi " << (*v_tk)->phi() << std::endl;
              }
              break;
            }
          }
          if (matched_vtx_idx!=-1)
            break;
        }
        if (debug)
          std::cout << "track matched with vertex " << matched_vtx_idx << std::endl;
        key[i] = matched_vtx_idx;
      }
      tab->addColumn<int>(branchName_ + "Idx", key, "Index into secondary vertices list for " + doc_, nanoaod::FlatTable::IntColumn);
      iEvent.put(std::move(tab));
    }

  protected:
      const std::string objName_, branchName_, doc_;
      const edm::EDGetTokenT<reco::TrackCollection> src_;
      const edm::EDGetTokenT<reco::VertexCollection> vtx_;
      bool debug;
};
#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(TrackVertexMatchTableProducer);
