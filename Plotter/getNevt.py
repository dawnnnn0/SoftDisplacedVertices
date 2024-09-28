import os
import uuid
import shutil
import itertools
import ctypes
import subprocess
import math
from uncertainties import ufloat
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
parser.add_argument('--SR', type=str, nargs='+', 
                        help='Signal region')
parser.add_argument('--metcut', type=float, #nargs='+', 
                        help='MET cut')
args = parser.parse_args()

def dict_product(dicts):
    return (dict(zip(dicts, x)) for x in itertools.product(*dicts.values()))

def getbErr(b,uncert,l,syst):
  # Poisson statistical uncertainty
  # Pearson's chi2 intervals
  b_low = math.sqrt(b*l+l*l/4)-l/2
  b_high = math.sqrt(b*l+l*l/4)+l/2
  b_stat = max(abs(b_high),(b_low))/b
  b_syst2 = syst*syst + (uncert/b)*(uncert/b)
  #return b*math.sqrt(b_stat*b_stat + b_syst*b_syst)
  return b*math.sqrt(b_syst2)

def sig(s,b,b_err):
  return math.sqrt(2*((s+b)*math.log(((s+b)*(b+b_err*b_err))/(b*b+(s+b)*b_err*b_err)) - (b*b/(b_err*b_err))*math.log(1+(b_err*b_err*s)/(b*(b+b_err*b_err)))))

def getEvts(SRname):
    out_d = {}
    fs_sig = []
    nevt_sigs = []
    nevt_uncert_sigs = []
    for fn in sig_fns:
      nevt_sig_uncert = ctypes.c_double(0)
      fs_sig.append(ROOT.TFile.Open(os.path.join(args.input,fn)))
      hsig = fs_sig[-1].Get(SRname)
      binlow = hsig.FindBin(args.metcut)
      nevt_sig = hsig.IntegralAndError(binlow,1000000,nevt_sig_uncert)
      nevt_sig_uncert = nevt_sig_uncert.value
      nevt_sigs.append(nevt_sig)
      nevt_uncert_sigs.append(nevt_sig_uncert)

    out_d['nevt_sigs'] = nevt_sigs
    out_d['nevt_uncert_sigs'] = nevt_uncert_sigs

    return out_d

if __name__=="__main__":
  sig_fns = [
      #"met2018_hist.root",
      "background_2018_hist.root",
      "stop_M600_575_ct0p2_2018_hist.root",
      "stop_M600_580_ct2_2018_hist.root",
      "stop_M600_585_ct20_2018_hist.root",
      "stop_M600_588_ct200_2018_hist.root",
      #"stop_M1000_975_ct0p2_2018_hist.root",
      #"stop_M1000_980_ct2_2018_hist.root",
      #"stop_M1000_985_ct20_2018_hist.root",
      #"stop_M1000_988_ct200_2018_hist.root",
      #"stop_M1400_1375_ct0p2_2018_hist.root",
      #"stop_M1400_1380_ct2_2018_hist.root",
      #"stop_M1400_1385_ct20_2018_hist.root",
      #"stop_M1400_1388_ct200_2018_hist.root",
      ]

  #sig_fns = []
  #for fn in os.listdir(args.input):
  #  if '.root' in fn:
  #    sig_fns.append(fn)


  max_sig = [0] * len(sig_fns)
  max_sig_cuts = [''] * len(sig_fns)

  if False:
    sigs = []
    for i in range(len(sig_fns)):
      sigss = []
      for sr in args.SR:
        SRname = "{}/MET_pt".format(sr)
        evt = getEvts(SRname)
        sigss.append(sig(evt['nevt_sigs'][i],evt['nevt_bkg'],evt['nevt_bkg_uncert']))
      sigs.append(sigss)
    sigs = np.array(sigs)
    fig, ax = plt.subplots()
    im = ax.imshow(sigs)
    # Show all ticks and label them with the respective list entries
    ax.set_yticks(np.arange(len(sig_fns)), labels=sig_fns)
    nicex = ['dphi','Iso','dphi+Iso','dphi+dr+Iso','dr+Iso']
    ax.set_xticks(np.arange(len(args.SR)), labels=nicex)
    # Loop over data dimensions and create text annotations.
    for i in range(len(sig_fns)):
      for j in range(len(args.SR)):
        text = ax.text(j, i, '%.3f'%(sigs[i, j]),
        ha="center", va="center", color="w")
    ax.set_title("significance of MET>{}".format(args.metcut))
    ax.set_ylabel("signal")
    ax.set_xlabel("cuts")
    ax.tick_params(axis='x', labelrotation=45)
    fig.tight_layout()
    #plt.show()
    plt.savefig('significanceMET{}.png'.format(args.metcut))
    plt.close(fig)


  for d in args.SR:
    SRname = "{}/MET_pt".format(d)
    devts = getEvts(SRname)

    print('==================================')
    print(d)
    for i in range(len(sig_fns)):
      #print("bkg: {}; sig1: {}; sig2: {}".format(nevt_bkg,nevt_sigs[0],nevt_sigs[1]))
      print("{} & ${:.02fL}$ & ${:.04fL}$ \\\\".format(sig_fns[i].replace('_2018_hist.root','').replace('_','\\_'),ufloat(devts['nevt_sigs'][i],devts['nevt_uncert_sigs'][i]),ufloat(devts['nevt_sigs'][i],devts['nevt_uncert_sigs'][i])/ufloat(devts['nevt_sigs'][0],devts['nevt_uncert_sigs'][0])))

  #for i in range(len(sig_fns)):
  #  print('==================================')
  #  print("Best significance: {}".format(max_sig[i]))
  #  print("Cuts: {}".format(max_sig_cuts[i]))


