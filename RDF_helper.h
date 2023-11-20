#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "TCanvas.h"
#include "TH1D.h"
#include "TLatex.h"
#include "Math/Vector4D.h"
#include "TStyle.h"


// //using ROOT::RVecB = typedef ROOT::VecOps::RVec<bool>
// //using ROOT::RVecI = typedef ROOT::VecOps::RVec<int>

// ROOT::RVecB mask_ngoodTrack(ROOT::RVecI & col){
//     return (col>= 2);
// }

ROOT::RVecB mask_ngoodTrack(ROOT::RVecI & ngoodTrack){
    return (ngoodTrack >= 2);
};

ROOT::RVecB mask_pAngle(ROOT::RVecF & pAngle){
    return (pAngle >= 0.20);
};

ROOT::RVecB mask_deltaPhi_MET_Lxy(ROOT::RVecF & SDVSecVtx_L_phi, const Float_t & RawMET_phi){
    ROOT::RVecD double_SDVSecVtx_L_phi = (ROOT::RVecD) SDVSecVtx_L_phi;
    Double_t double_RawMET_phi = (Double_t) RawMET_phi;

    return (acos(cos(SDVSecVtx_L_phi)*cos(RawMET_phi) + sin(SDVSecVtx_L_phi)*sin(RawMET_phi)) < 1.5);
};

ROOT::RVecI cast_to_int(const ROOT::RVecB & mask){
    return (ROOT::RVecI) mask;
};


ROOT::RVecI nGoodTrk(ROOT::RVecI & tr_mask,
                     ROOT::RVecI & lut_sv,
                     ROOT::RVecI & lut_tr,
                     const UInt_t & nsv)
{
    // Add ngoodTracks columns to SDVSecVtx table.
    ROOT::RVecI  sv_ngood_tr(nsv,0); // fill

    // Loop over sv in LUT and get the mask for sv_tracks
    for(auto i = 0; i < lut_sv.size(); i++){
        if(tr_mask[lut_tr[i]]){
            sv_ngood_tr[lut_sv[i]]++;
        }
    }
    return sv_ngood_tr;
}





























