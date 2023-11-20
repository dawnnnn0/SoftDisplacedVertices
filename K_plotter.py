# python K_plotter.py RawMET_pt,20,0,2000 -ev RawMET -sv DPHIRM,RALPHA,LXYSIG,NGTR -tr DXYSIG,DZ,NVH,RSPT
# python K_plotter.py SDVSecVtx_Lxy,40,0,120 -ev RawMET -sv DPHIRM,RALPHA,LXYSIG,NGTR -tr DXYSIG,DZ,NVH,RSPT

import ROOT

import click
import varcutlib
import os
import pickle

# ROOT.TH1.SetDefaultSumw2(False)
ROOT.gInterpreter.Declare('#include "RDF_helper.h"')
# ROOT.EnableImplicitMT()    # Tells ROOT to go parallel

# Empty class for the dot notation.
class DotDict:
    pass


def data_load_step(directory):
    """
    Gets the files in type agnostic way.
    Prepare the RDataFrame.

    Parameters
    ----------
    files: Should be a directory.
    """

    # Check out https://root-forum.cern.ch/t/how-to-open-multiple-root-files-with-rdataframe-in-pyroot/31497
    # ROOT_str_filenames = ROOT.std.vector('string')()
    # if isinstance(files, list):
    #     for filename in files:
    #         ROOT_str_filenames.push_back(filename)
    # elif isinstance(files, str):
    #     if os.path.isdir(files):
    #         ROOT_str_filenames = os.path.join(files, "*.root")
    #     else:
    #         ROOT_str_filenames.push_back(files)

    
    if os.path.isdir(directory):
        filenames = os.path.join(directory, "*.root")
    else:
        raise ValueError('You should provide a directory.')

    df = ROOT.RDataFrame("Events", filenames)
    
    # df = ROOT.RDataFrame("Events", "/users/alikaan.gueven/AOD_to_nanoAOD/data/dataFromFelix-NanoAODv9.root")


    lumi = 300.  # integrated luminosity
    xs   = 205.  # cross-section
    k_f  = 1.23 # LO -> NLO correction

    with open(os.path.join(directory.replace('NANO', 'MINI'), 'metadata.pkl'), 'rb') as f:
        pickle_dict = pickle.load(f)
    SumgenWeight = pickle_dict['totalSumWeights']
    # SumgenWeight = df.Sum('genWeight').GetValue()
    
    df = df.Define('scaling_factor', f'{lumi*xs*k_f/SumgenWeight}/genWeight')
    print(f"Scaling factor: {df.Take['double']('scaling_factor').GetValue()[0]}")
    # df = df.Define('scaling_factor', '1')
    
    return df


def filtering_step(df, cutstring, debug=False):
    """
    Filter RDataFrames.
    """
    
    df_ev = df.Filter(cutstring.ev)
    
    df_sv = df_ev.Define('SDVTrack_mask_wo_ngoodTr', cutstring.tr) \
                 .Define('SDVSecVtx_newgoodtr','nGoodTrk(SDVTrack_mask_wo_ngoodTr, SDVIdxLUT_SecVtxIdx, SDVIdxLUT_TrackIdx, nSDVSecVtx)') \
                 .Filter(f'Sum({cutstring.sv})>0')

    print('')
    print('{:<25}'.format('nEvents: '), df.Count().GetValue())
    print('{:<25}'.format('nEvents passing ev cuts: '), df_ev.Count().GetValue())
    print('{:<25}'.format('nEvents passing sv cuts: '), df_sv.Count().GetValue())

    if debug:
        print('-'*40)
        df_ev.Define('ev_mask', f'{cutstr_ev}') \
             .Define('sv_mask', f'Sum({cutstr_sv})>0') \
             .Display(['ev_mask', 'sv_mask', 'nSDVSecVtx'], 10).Print()
        print('-'*40)
    
    return df_ev, df_sv


# def filter_2SDVs(df, var, cutstring):
#     """
#     Filter RDataFrames.
#     """
    
#     # df_ev = df.Filter(cutstring.ev)
#     df_ev = df.Define('SDVTrack_mask_wo_ngoodTr', cutstring.tr) \
#               .Define('SDVSecVtx_newgoodtr','nGoodTrk(SDVTrack_mask_wo_ngoodTr, SDVIdxLUT_SecVtxIdx, SDVIdxLUT_TrackIdx, nSDVSecVtx)') \
#               .Filter(f'{cutstring.ev} && Sum({cutstring.sv})>1')
    
#     df_sv = df_ev.Define('masked_var', f'{var}[{cutstring.ev} && {cutstring.sv}]')

#     # DEBUG
#     print('-'*40)
#     df_sv.Define('ev_mask', f'{cutstring.ev}') \
#          .Define('sv_mask', f'{cutstring.sv}') \
#          .Display(['ev_mask', 'sv_mask', 'nSDVSecVtx', 'masked_var'], 30).Print()
#     print('-'*40)
#     return df_ev, df_sv


def masking_step(df, var, cutstring, debug=False):
    """
    Mask RDataFrames.
    """
    
    df_ev = df.Filter(cutstring.ev)
    
    df_sv = df_ev.Define('SDVTrack_mask_wo_ngoodTr', cutstring.tr) \
                 .Define('SDVSecVtx_newgoodtr','nGoodTrk(SDVTrack_mask_wo_ngoodTr, SDVIdxLUT_SecVtxIdx, SDVIdxLUT_TrackIdx, nSDVSecVtx)') \
                 .Define(f'masked_{var}', f'{var}[{cutstring.ev} && {cutstring.sv}]')

    print('')
    print('{:<25}'.format('nEvents: '), df.Count().GetValue())
    print('{:<25}'.format('nEvents passing ev cuts: '), df_ev.Count().GetValue())

    if debug:
        df_debug = df_sv.Filter(f'Sum(masked_{var}>15)>0')
        print('event', df_debug.Take['unsigned long long']('event').GetValue())
        print('GenMET_pt', df_debug.Take['ROOT::VecOps::RVec<float>']('GenMET_pt').GetValue())
        print('SDVSecVtx_Lxy', df_debug.Take['ROOT::VecOps::RVec<float>'](f'masked_{var}').GetValue())
        
        print('-'*40)
        df_sv.Define('ev_mask', f'{cutstring.ev}') \
             .Define('sv_mask', f'{cutstring.sv}') \
             .Display(['ev_mask', 'sv_mask', 'nSDVSecVtx', 'masked_var'], 20).Print()
        print('-'*40)
    
    return df_ev, df_sv


# HISTOGRAMS
# -----------

def histogram_step(df_ev, df_sv, pargs, is_masked=False, debug=False):
    """
    Calculate histograms.
    """
     
    hh_ev = df_ev.Histo1D(('ev', pargs.title, pargs.nb, pargs.xlow, pargs.xup), pargs.var, 'scaling_factor')

    if is_masked:
        pargs.masked_var = f'masked_{pargs.var}'
        hh_sv = df_sv.Histo1D(('sv', pargs.title, pargs.nb, pargs.xlow, pargs.xup), pargs.masked_var, 'scaling_factor')
    else:
        hh_sv = df_sv.Histo1D(('sv', pargs.title, pargs.nb, pargs.xlow, pargs.xup), pargs.var, 'scaling_factor')
    
    # hh_ev.Sumw2()
    # hh_sv.Sumw2()
        
    # hh_cut_efficacy = ROOT.TH1D('hh_cut_efficacy', 'Cut Efficacy', pargs.nb, pargs.xlow, pargs.xup)
    # hh_cut_efficacy.Divide(hh_sv.GetPtr(),hh_ev.GetPtr())

    if debug:
        # for i in range(1, hh_ev.GetNbinsX()):
        print('')
        for i in range(1, 5):
            bin_content_ev = hh_ev.GetBinContent(i)
            bin_content_sv = hh_sv.GetBinContent(i)

            bin_err_ev = hh_ev.GetBinError(i)
            bin_err_sv = hh_sv.GetBinError(i)
        
            print(bin_content_ev)
            print(bin_content_sv)
            print(bin_err_ev)
            print(bin_err_sv)
            # print('cut efficacy: ', f'{(0 if bin_content_ev==0 else bin_content_sv/bin_content_ev):.2f}')
            # print('cut efficacy with hist divide: ', f'{hh_cut_efficacy.GetBinContent(i):.2f} +/- {hh_cut_efficacy.GetBinError(i):.2f}')
            print('-'*40)

    
    return hh_ev, hh_sv



# PLOTS
# -------

def simple_plotting_step(hh_ev, hh_sv, pargs):
    
    c1 = ROOT.TCanvas("c1","myCanvas1",800,800)
    hh_ev.SetMarkerSize(0)
    hh_ev.SetFillStyle(3001) # hatched fill
    hh_ev.SetFillColorAlpha(1, 0.80)
    hh_ev.Draw('e2')
    
    hh_ev_no_err = hh_ev.Clone("ev_no_err")
    hh_ev_no_err.SetFillStyle(1001) # solid fill
    hh_ev_no_err.SetFillColorAlpha(1, 0.10)
    hh_ev_no_err.SetLineColor(1)
    hh_ev_no_err.SetLineWidth(2)
    hh_ev_no_err.Draw('hist same')
    
    hh_sv.SetMarkerSize(0)
    hh_sv.SetFillStyle(3001)
    hh_sv.SetFillColorAlpha(4, 0.80)
    hh_sv.Draw('e2 same')
    
    hh_sv_no_err = hh_sv.Clone("sv_no_err")
    hh_sv_no_err.SetFillStyle(1001)
    hh_sv_no_err.SetFillColorAlpha(4, 0.20)
    hh_sv_no_err.SetLineColor(4)
    hh_sv_no_err.SetLineWidth(2)
    hh_sv_no_err.Draw('hist same')
    
    c1.SetLogy(True)
    c1.SaveAs(pargs.savename)

    print('-'*100)
    print('\n')
    
    
def plotting_step(hh_ev, hh_sv, pargs):

    c1 = ROOT.TCanvas("c1","myCanvas1",800,800)
    c1.Divide(1,2,0,0)
    
    yswidth = 700
    ylwidth = 1000
    scaleFacBottomPad = yswidth/float((ylwidth-yswidth))
    yBorder = (ylwidth-yswidth)/float(ylwidth)    
    p1 = c1.cd(1)
    p1.SetBottomMargin(0.005)
    p1.SetTopMargin(0.05)
    p1.SetRightMargin(0.1)
    p1.SetPad(p1.GetX1(), yBorder, p1.GetX2(), p1.GetY2())
    p2 = c1.cd(2)
    p2.SetTopMargin(0)
    p2.SetRightMargin(0.1)
    p2.SetBottomMargin(scaleFacBottomPad*0.13)
    p2.SetPad(p2.GetX1(), p2.GetY1(),p2.GetX2(), yBorder-0.003)
    
    
    p1.cd()
    p1.SetLogy(True)
    hh_ev.SetFillColorAlpha(1, 0.2)
    hh_ev.SetLineColor(1)
    hh_ev.SetLineWidth(1)
    hh_ev.SetYTitle('events/bin')
    hh_ev.Draw('HIST SAME')
    
    hh_sv.SetFillColorAlpha(4, 0.2)
    hh_sv.SetLineColor(4)
    hh_sv.SetLineWidth(1)
    hh_sv.Draw('HIST SAME')
    
    p2.cd()
    hh_eff = ROOT.TEfficiency(hh_sv.GetValue(), hh_ev.GetValue())
    hh_eff.SetTitle(f';{pargs.var};sv/ev')
    hh_eff.SetMarkerSize(1)
    hh_eff.SetFillStyle(3001)
    hh_eff.SetFillColorAlpha(4, 0.80)
    
    hh_eff.Draw('e2')
    hh_eff.Draw('p0 same')
    c1.Update()

    
    hh_eff.GetPaintedGraph().GetXaxis().SetLimits(hh_ev.GetValue().GetXaxis().GetXmin(),hh_ev.GetValue().GetXaxis().GetXmax())
    hh_eff.GetPaintedGraph().GetXaxis().SetTitleSize(scaleFacBottomPad*hh_eff.GetPaintedGraph().GetXaxis().GetTitleSize())
    hh_eff.GetPaintedGraph().GetXaxis().SetLabelSize(scaleFacBottomPad*hh_eff.GetPaintedGraph().GetXaxis().GetLabelSize())
    hh_eff.GetPaintedGraph().GetXaxis().SetTickLength(scaleFacBottomPad*hh_eff.GetPaintedGraph().GetXaxis().GetTickLength())

    hh_eff.GetPaintedGraph().SetMinimum(0.)
    hh_eff.GetPaintedGraph().SetMaximum(1.05)
    hh_eff.GetPaintedGraph().GetYaxis().SetTitleSize(scaleFacBottomPad*hh_eff.GetPaintedGraph().GetYaxis().GetTitleSize())
    hh_eff.GetPaintedGraph().GetYaxis().SetLabelSize(scaleFacBottomPad*hh_eff.GetPaintedGraph().GetYaxis().GetLabelSize())
    hh_eff.GetPaintedGraph().GetYaxis().SetNdivisions(505)
    hh_eff.GetPaintedGraph().GetYaxis().SetTitleOffset(1.00 / scaleFacBottomPad)
    c1.Update()
    
    c1.SetLogy(True)
    c1.SaveAs(pargs.savename)

    print('-'*100)
    print('\n')
    
    
    
    
    
    
@click.command()
@click.argument('var_and_bins')
@click.option("-ev", default="1")
@click.option("-sv", default="1")
@click.option("-tr", default="1")
@click.option("-files", default="1")

def main_cli(var_and_bins, ev, sv, tr, files):
    print("Running main...")
    print('')
    print('var:   ', var_and_bins.split(',')[0])
    print('nbins: ', var_and_bins.split(',')[1])
    print('xlow:  ', var_and_bins.split(',')[2])
    print('xup:   ', var_and_bins.split(',')[3])
    print('')


    plot_args = DotDict()
    plot_args.title = 'Simulated Event Distributions After Cuts'
    plot_args.var =        var_and_bins.split(',')[0]
    plot_args.nb =     int(var_and_bins.split(',')[1])
    plot_args.xlow = float(var_and_bins.split(',')[2])
    plot_args.xup =  float(var_and_bins.split(',')[3])
    plot_args.savename = f'{plot_args.var}_w_cuts.png'
    cuts = varcutlib.get_cuts(ev, sv, tr)

    # files = "/users/alikaan.gueven/AOD_to_nanoAOD/data/dataFromFelix-NanoAODv9.root"
    assert files != 1, "Please don't forget to pass a ROOT file. or a list/directory of ROOT files."
    # files = "/users/alikaan.gueven/samplesNewSeedNoDuplicates/customNANOAODSIM/STOP/600_588_200"
    df = data_load_step(files)

    # Check if the var is entry level or subentry level (e.g. RawMET_pt or SDVSecVtx_Lxy)
    if df.GetColumnType(plot_args.var)[:18] == 'ROOT::VecOps::RVec':
        df_ev, df_sv = masking_step(df, plot_args.var, cuts)
        hh_ev, hh_sv = histogram_step(df_ev, df_sv, plot_args, is_masked=True, debug=True)
        plotting_step(hh_ev, hh_sv, plot_args)

    else:
        df_ev, df_sv = filtering_step(df, cuts)
        hh_ev, hh_sv = histogram_step(df_ev, df_sv, plot_args, debug=True)
        plotting_step(hh_ev, hh_sv, plot_args)


if __name__ == "__main__":
    main_cli()
    
    
    
    
