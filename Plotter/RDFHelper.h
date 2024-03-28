#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "TCanvas.h"
#include "TH1D.h"
#include "TLatex.h"
#include "Math/Vector4D.h"
#include "TStyle.h"
#include <algorithm> 

void printVec(ROOT::RVecI v) {

    for (size_t i=0; i<v.size(); ++i) {
        std::cout << v[i] << ", ";
    }
    std::cout << std::endl;
    return;
}

//This functino removes duplicated elements in a vector
template<typename T>
T removeDuplicate(T v) {
    //printVec(v);
    v = ROOT::VecOps::Sort(v);
    v.erase( std::unique( v.begin(), v.end() ), v.end() );
    //printVec(v);
    
    return v;
}

// This function returns a list with the length of nTracks, each element labels whether the track is included in a SV or not
ROOT::VecOps::RVec<int> Track_isInSV(ROOT::RVecI SDVIdxLUT_TrackIdx, int nTracks){
  ROOT::RVecI isInSV(nTracks,0);
  for (auto& idx : SDVIdxLUT_TrackIdx){
    isInSV[idx] = 1;
  }
  return isInSV;
}

// This function returns a list with the length of nTracks, each element shows the weight of the track in the SV fit
ROOT::VecOps::RVec<float> Track_WeightInSV(ROOT::RVecI SDVIdxLUT_TrackIdx, ROOT::RVecF SDVIdxLUT_TrackWeight, int nTracks){
  ROOT::RVecF tkweight(nTracks,-1);
  for (int i=0; i<SDVIdxLUT_TrackIdx.size(); ++i){
    tkweight[SDVIdxLUT_TrackIdx[i]] = SDVIdxLUT_TrackWeight[i];
  }
  return tkweight;
}

//This function helps to get the list of track indices that are included in the SDV (using LUT)
ROOT::VecOps::RVec<int> TracksinSDV(ROOT::RVecI SDVIdxLUT_SecVtxIdx, ROOT::RVecI SDVIdxLUT_TrackIdx, int iSDV)
{
    return SDVIdxLUT_TrackIdx[SDVIdxLUT_SecVtxIdx==iSDV];
}

ROOT::VecOps::RVec<int> GetTracksinSDVs(ROOT::RVecI SDVIdxLUT_SecVtxIdx, ROOT::RVecI SDVIdxLUT_TrackIdx, ROOT::RVecB SDVSecVtx_selected)
{
    ROOT::RVecI alltks;
    for (int i=0; i<SDVSecVtx_selected.size(); ++i){
        if (SDVSecVtx_selected[i]) {
            ROOT::RVecI tks = TracksinSDV(SDVIdxLUT_SecVtxIdx,SDVIdxLUT_TrackIdx,i);
            alltks = ROOT::VecOps::Concatenate(alltks,tks);
        }
    }
    return alltks;
}

//This function returns the number of good tracks in SDV
//It requires the input of SDVTrack_isGoodTrack, which is an array of 0 or 1 that indicates whether a track is good or not
ROOT::VecOps::RVec<int> SDVSecVtx_nGoodTrack(ROOT::RVecI SDVIdxLUT_SecVtxIdx, ROOT::RVecI SDVIdxLUT_TrackIdx, ROOT::RVecI SDVTrack_isGoodTrack, int nSDV)
{
    ROOT::VecOps::RVec<int> nGoodTracks;
    for (int i=0; i<nSDV; ++i){
        auto tkIdx = SDVIdxLUT_TrackIdx[SDVIdxLUT_SecVtxIdx==i];
        auto SDVTrack_isGoodTrack_filtered = ROOT::VecOps::Take(SDVTrack_isGoodTrack,tkIdx);
        auto SDVTrack_isGoodTrack_GoodTrack = SDVTrack_isGoodTrack_filtered[SDVTrack_isGoodTrack_filtered==1];
        nGoodTracks.push_back(SDVTrack_isGoodTrack_GoodTrack.size());
    }
    return nGoodTracks;
}

ROOT::VecOps::RVec<int> SDVSecVtx_nGoodRefitTrack(ROOT::RVecI SDVRefitTrack_svIdx, ROOT::RVecI SDVRefitTrack_isGoodTrack, int nSDV)
{
    ROOT::VecOps::RVec<int> nGoodTracks;
    for (int i=0; i<nSDV; ++i){
        auto ntk = ROOT::VecOps::Sum(SDVRefitTrack_isGoodTrack[SDVRefitTrack_svIdx==i]);
        nGoodTracks.push_back(ntk);
    }
    return nGoodTracks;
}

//This function returns a vector if the number of reco tracks in SDV that match with gen particles from the LLP decay (using LUT)
ROOT::VecOps::RVec<int> NMatchedTracksinSDV(ROOT::RVecI SDVTrack_LLPIdx, int nSDV, ROOT::RVecI SDVIdxLUT_SecVtxIdx, ROOT::RVecI SDVIdxLUT_TrackIdx)
{
    ROOT::VecOps::RVec<int> ntracks;
    for (int i=0; i<nSDV; ++i){
        //Get a list of track indices included in the SDV
        //std::cout << "1" << std::endl;
        auto tkIdx = SDVIdxLUT_TrackIdx[SDVIdxLUT_SecVtxIdx==i];
        //std::cout << "2" << std::endl;
        auto SDVTrack_LLPIdx_filtered = ROOT::VecOps::Take(SDVTrack_LLPIdx,tkIdx);
        //std::cout << "3" << std::endl;
        auto selectedTracks = SDVTrack_LLPIdx_filtered[SDVTrack_LLPIdx_filtered!=-1];
        //std::cout << "4" << std::endl;
        ntracks.push_back(selectedTracks.size());
    }
    return ntracks;
}

//This function returns a vector if the number of reco tracks in SDV that match with gen particles from the LLP decay (not using LUT)
ROOT::VecOps::RVec<int> NMatchedTracksinSDVnoLUT(ROOT::RVecI SDVTrack_LLPIdx, int nSDV, ROOT::RVecI SDVTrack_SecVtxIdx)
{
    ROOT::VecOps::RVec<int> ntracks;
    for (int i=0; i<nSDV; ++i){
        //Get a list of track indices included in the SDV
        //auto tkIdx = SDVIdxLUT_TrackIdx[SDVIdxLUT_SecVtxIdx==i];
        //auto SDVTrack_LLPIdx_filtered = ROOT::VecOps::Take(SDVTrack_LLPIdx,tkIdx);
        auto SDVTrack_LLPIdx_filtered = SDVTrack_LLPIdx[SDVTrack_SecVtxIdx==i];
        auto selectedTracks = SDVTrack_LLPIdx_filtered[SDVTrack_LLPIdx_filtered!=-1];
        ntracks.push_back(selectedTracks.size());
    }
    return ntracks;
}


//This function returns 
ROOT::VecOps::RVec<int> NMatchedTracksinLLP(ROOT::RVecI SDVTrack_LLPIdx, int nLLP)
{
    ROOT::VecOps::RVec<int> ntracks;
    for (int i=0; i<nLLP; ++i){
        auto selectedTracks = SDVTrack_LLPIdx[SDVTrack_LLPIdx==i];
        ntracks.push_back(selectedTracks.size());
    }
    return ntracks;
}

ROOT::VecOps::RVec<int> SDVIdxinLLP(ROOT::RVecI SDVTrack_LLPIdx, ROOT::RVecI SDVIdxLUT_SecVtxIdx, ROOT::RVecI SDVIdxLUT_TrackIdx, int nLLP, int nSDV, ROOT::RVecF SDVTrack_pt, ROOT::RVecF SDVTrack_eta, ROOT::RVecF SDVTrack_phi)
{
    ROOT::VecOps::RVec<int> SDVIdx(nLLP,-1);
    for (int illp=0; illp<nLLP; ++illp) {
        int Matched_SDV = -1;
        for (int isdv=0; isdv<nSDV; ++isdv){
            //Get a list of track indices included in the SDV
            auto tkIdx = SDVIdxLUT_TrackIdx[SDVIdxLUT_SecVtxIdx==isdv];
            auto SDVTrack_LLPIdx_filtered = ROOT::VecOps::Take(SDVTrack_LLPIdx,tkIdx);
            auto selectedTracks = SDVTrack_LLPIdx_filtered[SDVTrack_LLPIdx_filtered==illp];
            // DEBUG check
            //auto SDVTrack_pt_filtered = ROOT::VecOps::Take(SDVTrack_pt,tkIdx);
            //auto selected_pt = SDVTrack_pt_filtered[SDVTrack_LLPIdx_filtered==illp];
            //auto SDVTrack_eta_filtered = ROOT::VecOps::Take(SDVTrack_eta,tkIdx);
            //auto selected_eta = SDVTrack_eta_filtered[SDVTrack_LLPIdx_filtered==illp];
            //auto SDVTrack_phi_filtered = ROOT::VecOps::Take(SDVTrack_phi,tkIdx);
            //auto selected_phi = SDVTrack_phi_filtered[SDVTrack_LLPIdx_filtered==illp];
            //std::cout << "LLP " << illp << " vtx " << isdv << std::endl;
            //for (size_t i=0; i<selected_pt.size(); ++i){
            //    std::cout << "    pt " << selected_pt[i] << " eta " << selected_eta[i] << " phi " << selected_phi[i] << std::endl;
            //}
            if (selectedTracks.size()>0){
                Matched_SDV = isdv;
            }
        }
        SDVIdx[illp] = Matched_SDV;
    }
    return SDVIdx;
}


ROOT::VecOps::RVec<int> SDVIdxinLLP_dist(ROOT::RVecF LLP_decay_x, ROOT::RVecF LLP_decay_y, ROOT::RVecF LLP_decay_z, ROOT::RVecF SDVSecVtx_x, ROOT::RVecF SDVSecVtx_y, ROOT::RVecF SDVSecVtx_z, int nLLP, int nSDV)
{
    ROOT::VecOps::RVec<int> SDVIdx(nLLP,-1);
    for (int illp=0; illp<nLLP; ++illp) {
        int Matched_SDV = -1;
        for (int isdv=0; isdv<nSDV; ++isdv){
            double dist = sqrt((LLP_decay_x[illp]-SDVSecVtx_x[isdv])*(LLP_decay_x[illp]-SDVSecVtx_x[isdv]) + (LLP_decay_y[illp]-SDVSecVtx_y[isdv])*(LLP_decay_y[illp]-SDVSecVtx_y[isdv]) + (LLP_decay_z[illp]-SDVSecVtx_z[isdv])*(LLP_decay_z[illp]-SDVSecVtx_z[isdv]));
            if (dist<0.01)
                Matched_SDV = isdv;
        }
        SDVIdx[illp] = Matched_SDV;
    }
    return SDVIdx;
}

ROOT::VecOps::RVec<int> GenPartIdx_tkmatched(ROOT::RVecI SDVTrack_GenPartIdx, ROOT::RVecI SDVGenPart_isGentk, ROOT::RVecI SDVGenPart_LLPIdx)
{
    ROOT::RVecI SDVTrack_GenPartIdx_matched = SDVTrack_GenPartIdx[SDVTrack_GenPartIdx>=0];
    ROOT::RVecI SDVTrack_SDVGenPart_isGentk = ROOT::VecOps::Take(SDVGenPart_isGentk,SDVTrack_GenPartIdx_matched);
    ROOT::RVecI SDVTrack_SDVGenPart_LLPIdx = ROOT::VecOps::Take(SDVGenPart_LLPIdx,SDVTrack_GenPartIdx_matched);
    
    ROOT::RVecI idx = SDVTrack_GenPartIdx_matched[SDVTrack_SDVGenPart_isGentk==1 & SDVTrack_SDVGenPart_LLPIdx>=0];
    
    idx.erase( std::unique( idx.begin(), idx.end() ), idx.end() );
    
    return idx;
    
}

ROOT::RVecF LLP_GenTkSumpT(ROOT::RVecI SDVGenPart_isGentk, ROOT::RVecI SDVGenPart_LLPIdx, int nLLP, ROOT::RVecF SDVGenPart_pt, ROOT::RVecF SDVGenPart_eta, ROOT::RVecF SDVGenPart_phi, ROOT::RVecF SDVGenPart_mass)
{
    ROOT::VecOps::RVec<float> LLP_gtkpTsum(nLLP,0);
    for (size_t illp=0; illp<nLLP; ++illp){
        ROOT::Math::PtEtaPhiMVector p4_llp;
        ROOT::RVecF pts = SDVGenPart_pt[SDVGenPart_isGentk==1 & SDVGenPart_LLPIdx==illp];
        ROOT::RVecF etas = SDVGenPart_eta[SDVGenPart_isGentk==1 & SDVGenPart_LLPIdx==illp];
        ROOT::RVecF phis = SDVGenPart_phi[SDVGenPart_isGentk==1 & SDVGenPart_LLPIdx==illp];
        ROOT::RVecF masses = SDVGenPart_mass[SDVGenPart_isGentk==1 & SDVGenPart_LLPIdx==illp];
        for (size_t igtk=0; igtk<pts.size(); ++igtk){
            p4_llp += ROOT::Math::PtEtaPhiMVector(pts[igtk],etas[igtk],phis[igtk],masses[igtk]);
        }
        LLP_gtkpTsum[illp] = p4_llp.pt();
    }
    return LLP_gtkpTsum;
}


ROOT::RVecF LLP_GenTkMinpT(ROOT::RVecI SDVGenPart_isGentk, ROOT::RVecI SDVGenPart_LLPIdx, int nLLP, ROOT::RVecF SDVGenPart_pt, ROOT::RVecF SDVGenPart_eta, ROOT::RVecF SDVGenPart_phi, ROOT::RVecF SDVGenPart_mass)
{
    ROOT::VecOps::RVec<float> LLP_gtkpTmin(nLLP,0);
    for (size_t illp=0; illp<nLLP; ++illp){
        ROOT::RVecF pts = SDVGenPart_pt[SDVGenPart_isGentk==1 & SDVGenPart_LLPIdx==illp];
        LLP_gtkpTmin[illp] = ROOT::VecOps::Min(pts);
    }
    return LLP_gtkpTmin;
}


ROOT::RVecF LLP_GenTkMaxpT(ROOT::RVecI SDVGenPart_isGentk, ROOT::RVecI SDVGenPart_LLPIdx, int nLLP, ROOT::RVecF SDVGenPart_pt, ROOT::RVecF SDVGenPart_eta, ROOT::RVecF SDVGenPart_phi, ROOT::RVecF SDVGenPart_mass)
{
    ROOT::VecOps::RVec<float> LLP_gtkpTmax(nLLP,0);
    for (size_t illp=0; illp<nLLP; ++illp){
        ROOT::RVecF pts = SDVGenPart_pt[SDVGenPart_isGentk==1 & SDVGenPart_LLPIdx==illp];
        LLP_gtkpTmax[illp] = ROOT::VecOps::Max(pts);
    }
    return LLP_gtkpTmax;
}

float dPhi(float phi1, float phi2) {
  float x = phi1-phi2;
  float o2pi = 1. / (2. * M_PI);
  if (std::abs(x) <= float(M_PI))
    return x;
  float n = std::round(x * o2pi);
  return x - n * float(2. * M_PI);
}

float dR(float phi1, float phi2, float eta1, float eta2) {
    float dp = std::abs(dPhi(phi1, phi2));
    return sqrt(dp*dp+(eta1-eta2)*(eta1-eta2));
}

ROOT::RVecF SDV_TkMaxdphi(ROOT::RVecI SDVIdxLUT_TrackIdx, ROOT::RVecI SDVIdxLUT_SecVtxIdx, int nSDV, ROOT::RVecF SDVTrack_phi)
{
    ROOT::RVecF SDVSecVtx_maxdphi(nSDV,-1);
    for (size_t iSDV=0; iSDV<nSDV; ++iSDV){
        auto tkIdx = SDVIdxLUT_TrackIdx[SDVIdxLUT_SecVtxIdx==iSDV];
        ROOT::RVecF dphis;
        for (size_t i=0; i<tkIdx.size(); ++i){
            for (size_t j=i+1; j<tkIdx.size();++j){
                dphis.push_back(abs(dPhi(SDVTrack_phi[tkIdx[i]],SDVTrack_phi[tkIdx[j]])));
            }
        }
        SDVSecVtx_maxdphi[iSDV] = ROOT::VecOps::Max(dphis);
    }
    return SDVSecVtx_maxdphi;
}

ROOT::RVecF SDV_TkMindphi(ROOT::RVecI SDVIdxLUT_TrackIdx, ROOT::RVecI SDVIdxLUT_SecVtxIdx, int nSDV, ROOT::RVecF SDVTrack_phi)
{
    ROOT::RVecF SDVSecVtx_mindphi(nSDV,-1);
    for (size_t iSDV=0; iSDV<nSDV; ++iSDV){
        auto tkIdx = SDVIdxLUT_TrackIdx[SDVIdxLUT_SecVtxIdx==iSDV];
        ROOT::RVecF dphis;
        for (size_t i=0; i<tkIdx.size(); ++i){
            for (size_t j=i+1; j<tkIdx.size();++j){
                dphis.push_back(abs(dPhi(SDVTrack_phi[tkIdx[i]],SDVTrack_phi[tkIdx[j]])));
            }
        }
        SDVSecVtx_mindphi[iSDV] = ROOT::VecOps::Min(dphis);
    }
    return SDVSecVtx_mindphi;
}

ROOT::RVecF SDV_TkMaxdeta(ROOT::RVecI SDVIdxLUT_TrackIdx, ROOT::RVecI SDVIdxLUT_SecVtxIdx, int nSDV, ROOT::RVecF SDVTrack_eta)
{
    ROOT::RVecF SDVSecVtx_maxdeta(nSDV,-1);
    for (size_t iSDV=0; iSDV<nSDV; ++iSDV){
        auto tkIdx = SDVIdxLUT_TrackIdx[SDVIdxLUT_SecVtxIdx==iSDV];
        ROOT::RVecF dphis;
        for (size_t i=0; i<tkIdx.size(); ++i){
            for (size_t j=i+1; j<tkIdx.size();++j){
                dphis.push_back(abs(SDVTrack_eta[tkIdx[i]]-SDVTrack_eta[tkIdx[j]]));
            }
        }
        SDVSecVtx_maxdeta[iSDV] = ROOT::VecOps::Max(dphis);
    }
    return SDVSecVtx_maxdeta;
}

ROOT::RVecF SDV_TkMindeta(ROOT::RVecI SDVIdxLUT_TrackIdx, ROOT::RVecI SDVIdxLUT_SecVtxIdx, int nSDV, ROOT::RVecF SDVTrack_eta)
{
    ROOT::RVecF SDVSecVtx_mindeta(nSDV,-1);
    for (size_t iSDV=0; iSDV<nSDV; ++iSDV){
        auto tkIdx = SDVIdxLUT_TrackIdx[SDVIdxLUT_SecVtxIdx==iSDV];
        ROOT::RVecF dphis;
        for (size_t i=0; i<tkIdx.size(); ++i){
            for (size_t j=i+1; j<tkIdx.size();++j){
                dphis.push_back(abs(SDVTrack_eta[tkIdx[i]]-SDVTrack_eta[tkIdx[j]]));
            }
        }
        SDVSecVtx_mindeta[iSDV] = ROOT::VecOps::Min(dphis);
    }
    return SDVSecVtx_mindeta;
}

ROOT::RVecF SDV_TkMaxdR(ROOT::RVecI SDVIdxLUT_TrackIdx, ROOT::RVecI SDVIdxLUT_SecVtxIdx, int nSDV, ROOT::RVecF SDVTrack_eta, ROOT::RVecF SDVTrack_phi)
{
    ROOT::RVecF SDVSecVtx_maxdR(nSDV,-1);
    for (size_t iSDV=0; iSDV<nSDV; ++iSDV){
        auto tkIdx = SDVIdxLUT_TrackIdx[SDVIdxLUT_SecVtxIdx==iSDV];
        ROOT::RVecF dphis;
        for (size_t i=0; i<tkIdx.size(); ++i){
            for (size_t j=i+1; j<tkIdx.size();++j){
                dphis.push_back(dR(SDVTrack_phi[tkIdx[i]],SDVTrack_phi[tkIdx[j]],SDVTrack_eta[tkIdx[i]],SDVTrack_eta[tkIdx[j]]));
            }
        }
        SDVSecVtx_maxdR[iSDV] = ROOT::VecOps::Max(dphis);
    }
    return SDVSecVtx_maxdR;
}

ROOT::RVecF SDV_TkMindR(ROOT::RVecI SDVIdxLUT_TrackIdx, ROOT::RVecI SDVIdxLUT_SecVtxIdx, int nSDV, ROOT::RVecF SDVTrack_eta, ROOT::RVecF SDVTrack_phi)
{
    ROOT::RVecF SDVSecVtx_mindR(nSDV,-1);
    for (size_t iSDV=0; iSDV<nSDV; ++iSDV){
        auto tkIdx = SDVIdxLUT_TrackIdx[SDVIdxLUT_SecVtxIdx==iSDV];
        ROOT::RVecF dphis;
        for (size_t i=0; i<tkIdx.size(); ++i){
            for (size_t j=i+1; j<tkIdx.size();++j){
                dphis.push_back(dR(SDVTrack_phi[tkIdx[i]],SDVTrack_phi[tkIdx[j]],SDVTrack_eta[tkIdx[i]],SDVTrack_eta[tkIdx[j]]));
            }
        }
        SDVSecVtx_mindR[iSDV] = ROOT::VecOps::Min(dphis);
    }
    return SDVSecVtx_mindR;
}

