import click


def get_cuts(ev, sv, tr):
    print("ev_cuts: ", ev)
    print("sv_cuts: ", sv)
    print("tr_cuts: ", tr)

    cuts_ev = ev.split(',')
    cuts_sv = sv.split(',')
    cuts_tr = tr.split(',')
    
    cutdict_ev = {}
    cutdict_ev['1'] = 'ROOT::RVecB  no_cut(RawMET_pt.size(),0); // fill'
    cutdict_ev['MET'] = 'RawMET_pt>200.'
    cutstr_ev = '&&'.join(cutdict_ev[i] if i in cutdict_ev else i for i in cuts_ev)
    print("cutstr_ev: ", cutstr_ev) 
    
    
    cutdict_sv = {}
    cutdict_sv['1'] = ''
    cutdict_sv['DPHIRM'] = 'acos(cos(SDVSecVtx_L_phi-RawMET_phi))<1.5'
    cutdict_sv['RALPHA'] = 'SDVSecVtx_pAngle>0.2'
    cutdict_sv['LXYSIG'] = 'SDVSecVtx_LxySig>20'
    cutdict_sv['NGTR'] = 'SDVSecVtx_newgoodtr>=2'
    cutstr_sv = '&&'.join(cutdict_sv[i] if i in cutdict_sv else i for i in cuts_sv)
    print("cutstr_sv: ", cutstr_sv) 
    
    
    cutdict_tr = {}
    cutdict_tr['1'] = 'SDVTrack_numberOfValidHits>=0'
    cutdict_tr['DXYSIG'] = '(abs(SDVTrack_dxy)/SDVTrack_dxyError)>4'
    cutdict_tr['CHI2'] = 'SDVTrack_normalizedChi2 < 5'
    cutdict_tr['DZ'] = 'abs(SDVTrack_dz)<4.'
    cutdict_tr['NVH'] = 'SDVTrack_numberOfValidHits>13'
    cutdict_tr['RSPT'] = '(SDVTrack_ptError/SDVTrack_pt)<0.015'
    cutstr_tr = '&&'.join(cutdict_tr[i] if i in cutdict_tr else i for i in cuts_tr)
    print("cutstr_tr: ", cutstr_tr)


    
    return 'this is a cut_list'

def calc_histograms(cut_list):
    print("my_histograms: ", 'this is a histogram.')
    return 'this is a histogram.'

def plot_histograms(my_histograms):
    print("plotting histograms...")


@click.command()
@click.option("-ev", default="1")
@click.option("-sv", default="1")
@click.option("-tr", default="1")

def main_cli(ev, sv, tr):
    print("Running main...")
    cut_list = get_cuts(ev, sv, tr)
    my_histograms = calc_histograms(cut_list)
    plot_histograms(my_histograms)


if __name__ == "__main__":
    main_cli()