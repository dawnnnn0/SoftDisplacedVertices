#!/usr/bin/env python

import json
from SoftDisplacedVertices.Samples.Sample import *

def loadData(samples, json_path, label):
  with open(json_path,'r') as fj:
    d = json.load(fj)

  assert label in d

  for s in samples:
    setable = False
    if ("xs" in d) and (s.name in d['xs']):
      s.setxsec(d['xs'][s.name])
    if ('totalsumWeights' in d[label]) and (s.name in d[label]['totalsumWeights']):
      s.setNEvents(label,d[label]['totalsumWeights'][s.name])
    if ("dataset" in d[label]) and (s.name in d[label]["dataset"]):
      s.setDataset(label=label,dataset=d[label]["dataset"][s.name],instance='phys03')
      setable = True
    if ("dir" in d[label]) and (s.name in d[label]["dir"]):
      s.setDirs(label=label,dirs=d[label]["dir"][s.name])
      setable = True
    if ("logical_dir" in d[label]) and (s.name in d[label]["logical_dir"]):
      s.setEOSDirs(label=label,dirs=d[label]["logical_dir"][s.name])
      setable = True
    if not setable:
      print("Sample {} has no records!".format(b.name))

znunu_2018 = [
    Sample("zjetstonunuht0100_2018",xsec=344.83),
    Sample("zjetstonunuht0200_2018", xsec=95.53),
    Sample("zjetstonunuht0400_2018", xsec=13.20),
    Sample("zjetstonunuht0600_2018", xsec=3.148),
    Sample("zjetstonunuht0800_2018", xsec=1.451),
    Sample("zjetstonunuht1200_2018",xsec=0.355),
    Sample("zjetstonunuht2500_2018",xsec=0.00855),
    ]

wlnu_2018 = [
    Sample("wjetstolnuht0100_2018",xsec=1530.0),
    Sample("wjetstolnuht0200_2018", xsec=405.96),
    Sample("wjetstolnuht0400_2018", xsec=54.75),
    Sample("wjetstolnuht0600_2018", xsec=13.27),
    Sample("wjetstolnuht0800_2018", xsec=5.97),
    Sample("wjetstolnuht1200_2018",xsec=1.40),
    Sample("wjetstolnuht2500_2018",xsec=0.03255),
    ]

wlnu_2018 = [
    Sample("wjetstolnuht0100_2018",xsec=1.255e+03),
    Sample("wjetstolnuht0200_2018", xsec=3.364e+02),
    Sample("wjetstolnuht0400_2018", xsec=4.526e+01),
    Sample("wjetstolnuht0600_2018", xsec=1.099e+01),
    Sample("wjetstolnuht0800_2018", xsec=4.924),
    Sample("wjetstolnuht1200_2018",xsec=1.157),
    Sample("wjetstolnuht2500_2018",xsec=2.623e-02),
    ]

stop_2018 = [
    Sample("stop_M600_588_ct200_2018", xsec=0.205, filter_eff=0.294),
    Sample("stop_M600_585_ct20_2018", xsec=0.205, filter_eff=0.292),
    Sample("stop_M600_580_ct2_2018", xsec=0.205, filter_eff=0.292),
    Sample("stop_M1000_988_ct200_2018", xsec=0.00683, filter_eff=0.343),
    Sample("stop_M1000_985_ct20_2018", xsec=0.00683, filter_eff=0.347),
    Sample("stop_M1000_980_ct2_2018", xsec=0.00683, filter_eff=0.348),
    ]

c1n2_2018 = [
    Sample("C1N2_M600_588_ct200_2018", xsec=1e-03),
    ]

all_samples = [
    znunu_2018,
    wlnu_2018,
    stop_2018,
    c1n2_2018,
]

for samples in all_samples:
  for s in samples:
    exec("{} = s".format(s.name))

