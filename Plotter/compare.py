import os
import ROOT
import SoftDisplacedVertices.Samples.Samples as s
ROOT.EnableImplicitMT(4)
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.TH1.SetDefaultSumw2(True)
ROOT.gStyle.SetOptStat(0)

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, nargs='+',
                    help='files to compare')
parser.add_argument('--dirs', type=str, nargs='+',
                    help='directories to compare')
parser.add_argument('--nice', type=str, nargs='+',
                    help='legend names')
parser.add_argument('--scale', action='store_true', default=False,
                    help='Whether to scale the plot')
args = parser.parse_args()


def AddHists(hs,ws):
  assert len(hs)==len(ws)
  for i in range(len(hs)):
    hs[i].Scale(ws[i])
    if i>0:
      hs[0].Add(hs[i])
  return hs[0]

def StackHists(hs,ws):
  assert len(hs)==len(ws)
  h = ROOT.THStack("h","")
  for i in range(len(hs)):
    hs[i].Scale(ws[i])
    hs[i].SetLineColor(i+1)
    hs[i].SetFillColor(i+1)
    h.Add(hs[i])
  return h


def comparehists(name,hs,legend,colors=None,scale=False):
  c = ROOT.TCanvas("c"+name,"c"+name,600,600)
  l = ROOT.TLegend(0.6,0.7,0.9,0.9)
  y_max = 0
  y_min = 1
  for i in range(len(hs)):
    if scale:
      hs[i].Scale(1./hs[i].Integral())
    hs[i].SetLineWidth(2)
    if colors is not None:
      hs[i].SetLineColor(colors[i])
    y_max = max(y_max,hs[i].GetMaximum())
    y_min = min(y_min,hs[i].GetMinimum())

  for i in range(len(hs)):
    if i==0:
      hs[i].SetMaximum(10*y_max)
      #hs[i].SetMinimum(0.5*y_min)
      hs[i].DrawClone("PLC PMC")
    else:
      hs[i].DrawClone("same PLC PMC")
    l.AddEntry(hs[i],legend[i])

  l.Draw()
  c.Update()
  c.SetLogy()
  c.SaveAs("{}.pdf".format(name))

assert((len(args.input)>1) + (len(args.dirs)>1) == 1 )
fs = [ROOT.TFile.Open(fn) for fn in args.input]
plots = [p.GetName() for p in fs[0].GetListOfKeys()]

for plt in plots:
  h_compare = []
  for f in fs:
    try:
      h = f.Get(plt)
    except:
      print("{} not in f.".format(plt))
      continue
    h_compare.append(h.Clone())

  comparehists(plt,h_compare,legend=args.nice,scale=args.scale)

for f in fs:
  f.Close()




#f1 = ROOT.TFile.Open("/users/ang.li/public/SoftDV/CMSSW_13_3_0/src/SoftDisplacedVertices/Plotter/plots_ML_METSlice/bkg_2018_MLNanoAODv0_hist.root")
#f2 = ROOT.TFile.Open("/users/ang.li/public/SoftDV/CMSSW_13_3_0/src/SoftDisplacedVertices/Plotter/plots_ML_METSlice/stop_M600_588_ct200_2018_MLNanoAODv0_hist.root")
#f3 = ROOT.TFile.Open("/users/ang.li/public/SoftDV/CMSSW_13_3_0/src/SoftDisplacedVertices/Plotter/plots_ML_METSlice/stop_M600_585_ct20_2018_MLNanoAODv0_hist.root")
#f8 = ROOT.TFile.Open("/users/ang.li/public/SoftDV/CMSSW_13_3_0/src/SoftDisplacedVertices/Plotter/plots_ML_METSlice/stop_M600_580_ct2_2018_MLNanoAODv0_hist.root")
#f4 = ROOT.TFile.Open("/users/ang.li/public/SoftDV/CMSSW_13_3_0/src/SoftDisplacedVertices/Plotter/plots_ML_METSlice/stop_M600_580_ct2_2018_MLNanoAODv0_hist.root")

#legends = ['bkg',"stop_600_588_200"]
#color = [ROOT.kBlue, ROOT.kRed]
#legends = ["background",'stop_600_588_200','stop_600_585_20',"stop_600_580_2"]
#color = [ROOT.kBlack,ROOT.kBlue,ROOT.kRed,ROOT.kGreen+3]
#
#plots = [p.GetName() for p in f1.GetListOfKeys()]
#
#
#for plt in plots:
#  h_compare = []
#  for f in [f1,f2,f3,f8]:
#    try:
#      h = f.Get(plt)
#    except:
#      print("{} not in f.".format(plt))
#      continue
#    if ('SDVSecVtx_dlenSig' in plt) or ('SDVSecVtx_LxySig' in plt):
#      h = h.Rebin(5)
#    if ('MET_pt' in plt):
#      h = h.Rebin(5)
#    print(h.Integral())
#    h_compare.append(h.Clone())
#
#  comparehists(plt,h_compare,legend=legends,colors=color,scale=False)
#  comparehists(plt+'scale',h_compare,legend=legends,colors=color,scale=True)
#
#plots_sf = ['nSDVSecVtx_{0}sel','MET_pt{0}','SDVSecVtx_LxySig_{0}sel_max{0}']
#
#legends_sf = ['CC',"ML"]
#for plt in plots_sf:
#  h1 = f1.Get(plt.format(legends_sf[0]))
#  h2 = f1.Get(plt.format(legends_sf[1]))
#  #if ('MET' in plt):
#  #  h1 = h1.Rebin(5)
#  #  h2 = h2.Rebin(5)
#
#  h_compare = [h1,h2]
#  comparehists(plt.format("compbkg"),h_compare,legend=legends_sf,colors=color,scale=False)
#
#  h1 = f2.Get(plt.format(legends_sf[0]))
#  h2 = f2.Get(plt.format(legends_sf[1]))
#  #if ('MET' in plt):
#  #  h1 = h1.Rebin(5)
#  #  h2 = h2.Rebin(5)
#
#  h_compare = [h1,h2]
#  comparehists(plt.format("compsig"),h_compare,legend=legends_sf,colors=color,scale=False)
#
#legends = ["tag","untag"]
#for plt in plots:
#  if not "untag" in plt:
#    continue
#  plt_untag = plt
#  plt_tag = plt.replace('untag','tag')
#  h_sig_tag = f2.Get(plt_tag)
#  h_sig_untag = f2.Get(plt_untag)
#  h_bkg_tag = f1.Get(plt_tag)
#  h_bkg_untag = f1.Get(plt_untag)
#  h_comp = [h_sig_tag, h_sig_untag]
#  comparehists(plt.replace('untag','')+"tagcompsig",h_comp,legend=legends,colors=color,scale=True)
#  h_comp = [h_bkg_tag, h_bkg_untag]
#  comparehists(plt.replace('untag','')+"tagcompbkg",h_comp,legend=legends,colors=color,scale=True)
#
#plots_ML = ['SDVSecVtx_nGoodTracklowMET','SDVSecVtx_nGoodTrackmidMET','SDVSecVtx_nGoodTrackhighMET']
##plots_ML = ['SDVSecVtx_ParTScore']
#legends = ["background",'stop_600_588_200','stop_600_585_20',"stop_600_580_2"]
#color = [ROOT.kBlack,ROOT.kBlue,ROOT.kRed,ROOT.kGreen+3]
#for plt in plots_ML:
#  h1 = f1.Get(plt)
#  h2 = f2.Get(plt)
#  h3 = f3.Get(plt)
#  h4 = f8.Get(plt)
#  h_comp = [h1,h2,h3,h4]
#  comparehists(plt+"MLcomp",h_comp,legend=legends,colors=color,scale=True)

#plots_ML = ['SDVSecVtx_nGoodTracktaglowMET','SDVSecVtx_nGoodTracktagmidMET','SDVSecVtx_nGoodTracktaghighMET']
##plots_ML = ['SDVSecVtx_ParTScore']
#legends = ["200<MET<400",'400<MET<600','600<MET']
#color = [ROOT.kBlue,ROOT.kRed,ROOT.kGreen+3]
#h_comp = []
#for plt in plots_ML:
#  h = f1.Get(plt)
#  h_comp.append(h.Clone())
#comparehists(plt+"METslice",h_comp,legend=legends,colors=color,scale=True)
#
#
#f1.Close()
#f2.Close()
#f3.Close()
#f4.Close()
#f8.Close()

