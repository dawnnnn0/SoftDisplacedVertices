### Example usage:
### 
### Compare histograms for different directories in different files
### python3 compare.py --input /eos/vbc/group/cms/ang.li/MLhists/MLNanoAODv2/stop_M600_588_ct200_2018_hist.root /eos/vbc/group/cms/ang.li/MLhists/MLNanoAODv2/stop_M600_580_ct2_2018_hist.root --dirs histtag histuntag  --nice 588 580 --scale --output /groups/hephy/cms/ang.li/plots/plots_test
###
### Compare histograms for the same directory in different files
### python3 compare.py --input /eos/vbc/group/cms/ang.li/MLhists/MLNanoAODv2/stop_M600_588_ct200_2018_hist.root /eos/vbc/group/cms/ang.li/MLhists/MLNanoAODv2/stop_M600_580_ct2_2018_hist.root --dirs histtag  --nice 588 580 --scale --output /groups/hephy/cms/ang.li/plots/plots_test
###
### Compare histograms for different directories in the same file
### python3 compare.py --input /eos/vbc/group/cms/ang.li/MLhists/MLNanoAODv2/stop_M600_588_ct200_2018_hist.root --dirs histtag histuntag  --nice tag untag --scale --output /groups/hephy/cms/ang.li/plots/plots_test


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
parser.add_argument('--output', type=str,
                    help='output dir')
parser.add_argument('--dirs', type=str, nargs='+',
                    help='directories to compare')
parser.add_argument('--nice', type=str, nargs='+',
                    help='legend names')
parser.add_argument('--scale', action='store_true', default=False,
                    help='Whether to scale the plot')
args = parser.parse_args()

colors_global = [ROOT.kBlue,ROOT.kRed+1,ROOT.kGreen+1,ROOT.kYellow+1,ROOT.kMagenta+1,ROOT.kCyan+1]

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
  if colors is None:
    colors = colors_global[:len(hs)]
  c = ROOT.TCanvas("c"+name,"c"+name,600,600)
  l = ROOT.TLegend(0.6,0.7,0.9,0.9)
  y_max = 0
  y_min = 1
  for i in range(len(hs)):
    if scale:
      hs[i].Scale(1./hs[i].Integral())
    hs[i].SetLineWidth(2)
    hs[i].SetLineColor(colors[i])
    y_max = max(y_max,hs[i].GetMaximum())
    y_min = min(y_min,hs[i].GetMinimum())

  for i in range(len(hs)):
    if i==0:
      hs[i].SetMaximum(10*y_max)
      #hs[i].SetMinimum(0.5*y_min)
      hs[i].DrawClone()
    else:
      hs[i].DrawClone("same")
    l.AddEntry(hs[i],legend[i])

  l.Draw()
  c.Update()
  c.SetLogy()
  c.SaveAs("{}.pdf".format(args.output+'/'+name))
  c.SaveAs("{}.png".format(args.output+'/'+name))

def compareDiffFiles(fns,legend,colors,scale):
  fs = [ROOT.TFile.Open(fn) for fn in fns]
  dirs = []
  if len(args.dirs)==0:
    dirs = ['']*len(fs)
    plots = [p.GetName() for p in fs[0].GetListOfKeys()]
  else:
    dirs = args.dirs
    if len(dirs)==1:
      dirs = [args.dirs[0]]*len(fs)
    fdir = fs[0].Get(args.dirs[0])
    if not fdir:
      print("{} not available in {}!".format(args.dirs[0],fs[0].GetName()))
    plots = [p.GetName() for p in fdir.GetListOfKeys()]
  
  assert(len(dirs)==len(fs))
  for plt in plots:
    h_compare = []
    for f,d in zip(fs,dirs):
      try:
        h = f.Get(d+'/'+plt)
      except:
        print('{} is not available in {}!'.format(d+'/'+plt,f.GetName()))
        continue
      h.SetDirectory(0)
      h_compare.append(h)
  
    comparehists(plt,h_compare,legend=legend,colors=colors,scale=scale)
  
  for f in fs:
    f.Close()

def compareDiffFilesSpecial(fns,legend,colors,scale):
  fs = [ROOT.TFile.Open(fn) for fn in fns]
  plots = [p.GetName() for p in fs[0].GetListOfKeys()]
  
  for plt in plots:
    if not 'untag' in plt:
      continue
    h_compare = []
    for f in fs:
      if 'stop' in f.GetName():
        h = f.Get(plt.replace('untag','genmatchtag'))
      else:
        h = f.Get(plt.replace('untag','tag'))
      h.SetDirectory(0)
      h_compare.append(h)
  
    comparehists(plt,h_compare,legend=legend,colors=colors,scale=scale)
  
  for f in fs:
    f.Close()

def compareSameFile(fn,legend,colors,scale):
  f = ROOT.TFile.Open(fn)

  fdir = f.Get(args.dirs[0])
  if not fdir:
    print("{} not available in {}!".format(args.dirs[0],f.GetName()))
  plots = [p.GetName() for p in fdir.GetListOfKeys()]
  
  for plt in plots:
    h_compare = []
    for d in args.dirs:
      try:
        h = f.Get(d+'/'+plt)
      except:
        print('{} is not available in {}!'.format(d+'/'+plt,f.GetName()))
        continue
      h.SetDirectory(0)
      h_compare.append(h)
  
    comparehists(plt,h_compare,legend=legend,colors=colors,scale=scale)
  
  f.Close()

if __name__ == "__main__":
  if not os.path.exists(args.output):
    os.makedirs(args.output)
  if len(args.input)==1:
    assert(len(args.dirs)>1)
    compareSameFile(args.input[0],args.nice,None,args.scale)
  else:
    compareDiffFiles(args.input,args.nice,None,args.scale)
    #compareDiffFilesSpecial(args.input,args.nice,None,args.scale)

