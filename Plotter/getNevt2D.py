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
parser.add_argument('--SR', type=str, nargs='+', 
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

def getEvts(SRname):
    out_d = {
        'nevt_A': [],
        'nevt_A_uncert': [],
        'nevt_B': [],
        'nevt_B_uncert': [],
        'nevt_C': [],
        'nevt_C_uncert': [],
        'nevt_D': [],
        'nevt_D_uncert': [],
        }
    fs_sig = []

    for fn in sig_fns:
      nevt_sig_uncert = ctypes.c_double(0)
      fs_sig.append(ROOT.TFile.Open(os.path.join(args.input,fn)))
      hsig = fs_sig[-1].Get(SRname)
      binlow = hsig.FindBin(args.metcut)
      xcut = hsig.GetXaxis().FindBin(700)
      ycut = hsig.GetYaxis().FindBin(20)
      nevt_A_uncert = ctypes.c_double(0)
      nevt_A = hsig.IntegralAndError(xcut,1000000,ycut,1000000,nevt_A_uncert)
      nevt_A_uncert = nevt_A_uncert.value
      nevt_B_uncert = ctypes.c_double(0)
      nevt_B = hsig.IntegralAndError(0,xcut-1,ycut,1000000,nevt_B_uncert)
      nevt_B_uncert = nevt_B_uncert.value
      nevt_C_uncert = ctypes.c_double(0)
      nevt_C = hsig.IntegralAndError(xcut,1000000,0,ycut-1,nevt_C_uncert)
      nevt_C_uncert = nevt_C_uncert.value
      nevt_D_uncert = ctypes.c_double(0)
      nevt_D = hsig.IntegralAndError(0,xcut-1,0,ycut-1,nevt_D_uncert)
      nevt_D_uncert = nevt_D_uncert.value

      for r in ['A','B','C','D']:
        eval("out_d['nevt_{0}'].append(nevt_{0})".format(r))
        eval("out_d['nevt_{0}_uncert'].append(nevt_{0}_uncert)".format(r))

    return out_d

if __name__=="__main__":
  sig_fns = [
      "met2018_hist.root",
      #"background_2018_hist.root",
      #"stop_M600_575_ct0p2_2018_hist.root",
      #"stop_M600_580_ct2_2018_hist.root",
      #"stop_M600_585_ct20_2018_hist.root",
      #"stop_M600_588_ct200_2018_hist.root",
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
        SRname = "{}".format(sr)
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
    SRname = "{}".format(d)
    devts = getEvts(SRname)
    print(d)
    for r in ['A','B','C','D']:
      print("REGION {}".format(r))
      print('==================================')
      for i in range(len(sig_fns)):
        #print("bkg: {}; sig1: {}; sig2: {}".format(nevt_bkg,nevt_sigs[0],nevt_sigs[1]))
        print("Process {} #evts: {:.02f} +- {:.02f}".format(sig_fns[i],devts['nevt_{}'.format(r)][i],devts['nevt_{}_uncert'.format(r)][i]))

  #for i in range(len(sig_fns)):
  #  print('==================================')
  #  print("Best significance: {}".format(max_sig[i]))
  #  print("Cuts: {}".format(max_sig_cuts[i]))


