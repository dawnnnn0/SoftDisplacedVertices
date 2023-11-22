# varcutlib
from types import SimpleNamespace
# import argparse

# parser = argparse.ArgumentParser()

# parser.add_argument("-ev", default='1')
# parser.add_argument("-sv", default='1')
# parser.add_argument("-tr", default='1')

# cuts = parser.parse_args()

# ev = cuts.ev
# sv = cuts.sv
# tr = cuts.tr

def get_cuts(ev,sv,tr):
    """
    Gets abbreviations of the  cuts and returns them in a ROOT compatible form.
    The user can provide cuts that are not listed as well, but then s/he,
    in that case it is the user's responsibilty to check if those in the form as ROOT expects.

    
    Parameters
    ----------

    ev: str
        Event cuts delimited by comma (,).
    sv: str
        Secondary vertex cuts delimited by comma (,).
    tr: str
        Track cuts delimited by comma (,).

    Returns
    -------

    cuts_dotdict: SimpleNamespace
        Cut strings are accessible via dot notation, e.g. cuts.ev

    """
    print("ev_cuts: ", ev)
    print("sv_cuts: ", sv)
    print("tr_cuts: ", tr)
    print('')

    cuts_ev = ev.split(',')
    cuts_sv = sv.split(',')
    cuts_tr = tr.split(',')

    cutdict_ev = {}
    cutdict_ev['1'] = 'true'
    cutdict_ev['RawMET'] = 'RawMET_pt>200.'
    cutdict_ev['GenMET'] = 'GenMET_pt>200.'
    cutdict_ev['GenJet'] = 'GenJet_pt[0]>100.'
    
    cutstr_ev = '&&'.join(cutdict_ev[i] if i in cutdict_ev else i for i in cuts_ev)
    print("cutstr_ev: ", cutstr_ev) 
    
    
    cutdict_sv = {}
    # cutdict_sv['1'] = 'ROOT::RVecB(nSDVSecVtx, 1)' # When nSDVSecVtx is 0, RVec is ambiguous, thus set to false. Avoid this with the following line.
    cutdict_sv['1'] = '(nSDVSecVtx>0) ? ROOT::RVecB(nSDVSecVtx, 1) : ROOT::RVecB(1, 1)'
    cutdict_sv['DPHIRM'] = 'acos(cos(SDVSecVtx_L_phi-GenMET_phi))<1.5'
    cutdict_sv['RALPHA'] = 'SDVSecVtx_pAngle>0.2'
    cutdict_sv['LXYSIG'] = 'SDVSecVtx_LxySig>20'
    cutdict_sv['NGTR'] = 'SDVSecVtx_newgoodtr>=2'
    cutdict_sv["DPHIJ"] = 'acos(cos(SDVSecVtx_L_phi-GenJet_phi[0]))>1'
    cutdict_sv["NDOF"] = 'SDVSecVtx_ndof>1'
    
    cutstr_sv = '&&'.join(cutdict_sv[i] if i in cutdict_sv else i for i in cuts_sv)
    print("cutstr_sv: ", cutstr_sv) 
    
    
    cutdict_tr = {}
    # cutdict_tr['1'] = 'ROOT::RVecI(nSDVTrack, 1)' # When nSDVTrack is 0, RVec is ambiguous, thus set to false. Avoid this with the following line.
    cutdict_tr['1'] = '(nSDVTrack>0) ? ROOT::RVecI(nSDVTrack, 1) : ROOT::RVecI(1, 1)'
    cutdict_tr['DXYSIG'] = '(abs(SDVTrack_dxy)/SDVTrack_dxyError)>4'
    cutdict_tr['CHI2'] = 'SDVTrack_normalizedChi2 < 5'
    cutdict_tr['DZ'] = 'abs(SDVTrack_dz)<4.'
    cutdict_tr['NVH'] = 'SDVTrack_numberOfValidHits>13'
    cutdict_tr['RSPT'] = '(SDVTrack_ptError/SDVTrack_pt)<0.015'
    cutdict_tr["DPHIJ"] = 'acos(cos(SDVTrack_phi-GenJet_phi[0]))>1'
    cutdict_tr["DPHIM"] = 'acos(cos(SDVTrack_phi-GenMET_phi))<1.5'
    
    cutstr_tr = '&&'.join(cutdict_tr[i] if i in cutdict_tr else i for i in cuts_tr)
    print("cutstr_tr: ", cutstr_tr)
    print('')

    
    cuts_dict = {'ev': cutstr_ev, 'sv': cutstr_sv, 'tr': cutstr_tr}
    cuts_dotdict = SimpleNamespace(**cuts_dict)
    
    return cuts_dotdict





