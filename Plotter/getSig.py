import os
import uuid
import shutil
import itertools
import ctypes
import subprocess
import math
import ROOT
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib as mpl
import SoftDisplacedVertices.Plotter.plotter as p
import SoftDisplacedVertices.Plotter.plot_setting as ps
import SoftDisplacedVertices.Samples.Samples as s
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str,
                        help='input dir')
parser.add_argument('--SR', type=str, #nargs='+', 
                        help='Signal region')
parser.add_argument('--metcut', type=float, #nargs='+', 
                        help='MET cut')
args = parser.parse_args()

def dict_product(dicts):
    return (dict(zip(dicts, x)) for x in itertools.product(*dicts.values()))

def getbErr(b,uncert,l,syst):
  # Poisson statistical uncertainty
  # Pearson’s chi2 intervals
  b_low = math.sqrt(b*l+l*l/4)-l/2
  b_high = math.sqrt(b*l+l*l/4)+l/2
  b_stat = max(abs(b_high),(b_low))/b
  b_syst2 = syst*syst + (uncert/b)*(uncert/b)
  #return b*math.sqrt(b_stat*b_stat + b_syst*b_syst)
  return b*math.sqrt(b_syst2)

def sig(s,b,b_err):
  return math.sqrt(2*((s+b)*math.log(((s+b)*(b+b_err*b_err))/(b*b+(s+b)*b_err*b_err)) - (b*b/(b_err*b_err))*math.log(1+(b_err*b_err*s)/(b*(b+b_err*b_err)))))

if __name__=="__main__":
  scan_params = {
      '__DPHIMET__': [1.5],
      '__DPHIJET__': [1],
      '__LXYSIG__': [0,10,20],
      '__PANGLE__': [0,0.1,0.2],
      '__NGOODTK__': [0,1,2],
      '__TKDXYSIG__': [2,3,4],
      '__TKDXYDZ__': [0.1,0.15,0.2,0.25,0.3],
      '__ML__': [0.97,0.98,0.99],
      }

  sig_fns = [
      "stop_M600_580_ct2_2018_hist.root",
      "stop_M600_585_ct20_2018_hist.root",
      "stop_M600_588_ct200_2018_hist.root",
      "stop_M1000_980_ct2_2018_hist.root",
      "stop_M1000_985_ct20_2018_hist.root",
      "stop_M1000_988_ct200_2018_hist.root",
      ]

  SRname = "{}/MET_pt".format(args.SR)
  #SRname = "normsel_evt/MET_pt"
  #SRname = "CCSR_evt/MET_pt"
  #SRnames = ["{}/MET_pt".format(sr) for sr in args.SR]

  max_sig = [0] * len(sig_fns)
  max_sig_cuts = [''] * len(sig_fns)

  if False:
    TKDXYSIG = [2,3,4,5,6]
    TKDXYDZ = [0.1,0.15,0.2,0.25,0.3,0.35,0.4]

    for fn in sig_fns:
      sigs = []
      for iy in TKDXYSIG:
        sigss = []
        for ix in TKDXYDZ:
          #d = 'cutscan__DPHIMET__1p5__DPHIJET__1__LXYSIG__20__PANGLE__0p2__NGOODTK__2__TKDXYSIG__{}__TKDXYDZ__{}'.format(iy,ix).replace('.','p')
          d = 'cutscan__DPHIMET__1p5__DPHIJET__1__LXYSIG__0__PANGLE__0__NGOODTK__2__TKDXYSIG__{}__TKDXYDZ__{}'.format(iy,ix).replace('.','p')
          f_bkg = ROOT.TFile.Open(os.path.join(args.input,d,"background_2018_hist.root"))
          fs_sig = ROOT.TFile.Open(os.path.join(args.input,d,fn))
          bkg_uncert = ctypes.c_double(0)
          nevt_bkg = f_bkg.Get(SRname).IntegralAndError(0,1000000,bkg_uncert)
          bkg_uncert = bkg_uncert.value
          nevt_bkg_uncert = getbErr(nevt_bkg,bkg_uncert,l=1,syst=0.2)
          nevt_sigs = fs_sig.Get(SRname).Integral(0,1000000)
          #if 'stop_M1000_' in fn:
          #  nevt_sigs = 6.83 * nevt_sigs
          sigss.append(sig(nevt_sigs,nevt_bkg,nevt_bkg_uncert))
        sigs.append(sigss)
      sigs = np.array(sigs)
      fig, ax = plt.subplots()
      im = ax.imshow(sigs)
      # Show all ticks and label them with the respective list entries
      ax.set_yticks(np.arange(len(TKDXYSIG)), labels=TKDXYSIG)
      ax.set_xticks(np.arange(len(TKDXYDZ)), labels=TKDXYDZ)
      # Loop over data dimensions and create text annotations.
      for i in range(len(TKDXYSIG)):
        for j in range(len(TKDXYDZ)):
          text = ax.text(j, i, '%.3f'%(sigs[i, j]),
          ha="center", va="center", color="w")
      ax.set_title("significance of {}".format(fn.replace('_2018_hist.root','')))
      ax.set_ylabel("track dxy significance cut value")
      ax.set_xlabel("track |dxy/dz| cut value")
      fig.tight_layout()
      #plt.show()
      plt.savefig('significance{}.png'.format(fn.replace('.root','')))
      plt.close(fig)


  for d in os.listdir(args.input):
    #if not d=='cutscan__DPHIMET__1p5__DPHIJET__1__LXYSIG__20__PANGLE__0p2__NGOODTK__2__TKDXYSIG__4__TKDXYDZ__0p25':
    #  continue
    if not d=='MLNanoAODv3_dphidrisoSR_0328':
      continue

    if not ("background_2018_hist.root" in os.listdir(os.path.join(args.input,d))):
      haddcmd = "hadd {} {}".format(os.path.join(args.input,d,"background_2018_hist.root"), os.path.join(args.input,d,"*jetsto*.root"))
      print("hadding files: {}".format(haddcmd))
      p = subprocess.Popen(args=haddcmd,stdout = subprocess.PIPE,stderr = subprocess.STDOUT, shell=True)
      print(p.stdout.read())
    f_bkg = ROOT.TFile.Open(os.path.join(args.input,d,"background_2018_hist.root"))
    bkg_uncert = ctypes.c_double(0)
    if not f_bkg.Get(SRname):
      print("Fail to get {} from {}".format(SRname,f_bkg.GetName()))
    hbkg = f_bkg.Get(SRname)
    binlow = hbkg.FindBin(args.metcut)
    nevt_bkg = hbkg.IntegralAndError(binlow,1000000,bkg_uncert)
    bkg_uncert = bkg_uncert.value
    #nevt_bkg *= 1.23
    #bkg_uncert *= 1.23
    nevt_bkg_uncert = getbErr(nevt_bkg,bkg_uncert,l=1,syst=0.2)
    fs_sig = []
    nevt_sigs = []
    nevt_uncert_sigs = []
    for fn in sig_fns:
      nevt_sig_uncert = ctypes.c_double(0)
      fs_sig.append(ROOT.TFile.Open(os.path.join(args.input,d,fn)))
      hsig = fs_sig[-1].Get(SRname)
      binlow = hsig.FindBin(args.metcut)
      nevt_sig = hsig.IntegralAndError(binlow,1000000,nevt_sig_uncert)
      nevt_sig_uncert = nevt_sig_uncert.value
      #if 'stop_M1000_' in fn:
      #  nevt_sig = 6.83 * nevt_sig
      #  nevt_sig_uncert = 6.83 * nevt_sig_uncert
      nevt_sigs.append(nevt_sig)
      nevt_uncert_sigs.append(nevt_sig_uncert)


    for i in range(len(sig_fns)):
      if sig(nevt_sigs[i],nevt_bkg,nevt_bkg_uncert) > max_sig[i]:
        max_sig[i] = max(sig(nevt_sigs[i],nevt_bkg,nevt_bkg_uncert),max_sig[i])
        max_sig_cuts[i] = d

    print('==================================')
    print(d)
    print("background # evts: {:.02f} +- {:.02f}".format(nevt_bkg,nevt_bkg_uncert))
    for i in range(len(sig_fns)):
      #print("bkg: {}; sig1: {}; sig2: {}".format(nevt_bkg,nevt_sigs[0],nevt_sigs[1]))
      print("signal {} #evts: {:.02f} +- {:.02f}; significance: {:.02f}".format(i,nevt_sigs[i],nevt_uncert_sigs[i],sig(nevt_sigs[i],nevt_bkg,nevt_bkg_uncert)))

  #for i in range(len(sig_fns)):
  #  print('==================================')
  #  print("Best significance: {}".format(max_sig[i]))
  #  print("Cuts: {}".format(max_sig_cuts[i]))


