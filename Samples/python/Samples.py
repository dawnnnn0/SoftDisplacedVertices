#!/usr/bin/env python

import json
from SoftDisplacedVertices.Samples.Sample import *

def loadData(samples, json_path, label):
  with open(json_path,'r') as fj:
    d = json.load(fj)

  assert label in d

  for s in samples:
    if s.name in d[label]["dataset"]:
      s.setDataset(label=label,dataset=d[label]["dataset"][s.name],instance='phys03')
    elif s.name in d[label]["dir"]:
      s.setDirs(label=label,dirs=d[label]["dir"][s.name])
    else:
      print("Sample {} has no records!".format(b.name))


background = [
    Sample("ZJetsToNuNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8",xsec=280.35),
    Sample("ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8", xsec=77.67),
    Sample("ZJetsToNuNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8", xsec=10.73),
    Sample("ZJetsToNuNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8", xsec=2.559),
    Sample("ZJetsToNuNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8", xsec=1.1796),
    Sample("ZJetsToNuNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8",xsec=0.28833),
    Sample("ZJetsToNuNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8",xsec=0.006945),
    ]

znunu_2018 = [
    Sample("zjetstonunuht0100_2018",xsec=280.35),
    Sample("zjetstonunuht0200_2018", xsec=77.67),
    Sample("zjetstonunuht0400_2018", xsec=10.73),
    Sample("zjetstonunuht0600_2018", xsec=2.559),
    Sample("zjetstonunuht0800_2018", xsec=1.1796),
    Sample("zjetstonunuht1200_2018",xsec=0.28833),
    Sample("zjetstonunuht2500_2018",xsec=0.006945),
    ]

stop_2018 = [
    Sample("stop_M600_588_ct200", xsec=1e-03),
    Sample("stop_M600_585_ct20", xsec=1e-03),
    Sample("stop_M600_580_ct2", xsec=1e-03),
    Sample("stop_M1000_988_ct200", xsec=1e-03),
    Sample("stop_M1000_985_ct20", xsec=1e-03),
    Sample("stop_M1000_980_ct2", xsec=1e-03),
    ]

all_samples = [
    znunu_2018,
    stop_2018,
]

for samples in all_samples:
  for s in samples:
    exec("{} = s".format(s.name))

#MINIAOD_datasets = [
#    '/ZJetsToNuNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/liko-ZJetToNuNu_HT-100To200_MC_UL18_CustomMiniAODv1-1-d89a5f51c8622d62b5accbd8b7f90262/USER',
#    '/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/liko-ZJetsToNuNu_HT-200To400_MC_UL18_CustomMiniAODv1-1-d89a5f51c8622d62b5accbd8b7f90262/USER',
#    '/ZJetsToNuNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/liko-ZJetsToNuNu_HT-400To600_MC_UL18_CustomMiniAODv1-1-d89a5f51c8622d62b5accbd8b7f90262/USER',
#    '/ZJetsToNuNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/liko-ZJetsToNuNu_HT-600To800_MC_UL18_CustomMiniAODv1-1-d89a5f51c8622d62b5accbd8b7f90262/USER',
#    '/ZJetsToNuNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/liko-ZJetsToNuNu_HT-800To1200_MC_UL18_CustomMiniAODv1-1-d89a5f51c8622d62b5accbd8b7f90262/USER',
#    '/ZJetsToNuNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/liko-ZJetsToNuNu_HT-1200To2500_MC_UL18_CustomMiniAODv1-1-d89a5f51c8622d62b5accbd8b7f90262/USER',
#    '/ZJetsToNuNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/liko-ZJetsToNuNu_HT-2500ToInf_MC_UL18_CustomMiniAODv1-1-d89a5f51c8622d62b5accbd8b7f90262/USER',
#    ]
#
#for i in range(len(background)):
#  background[i].setDataset(tier='MINIAOD', dataset=MINIAOD_datasets[i], instance='phys03')
#
#background[0].setDirs(tier='MINIAOD',dirs="/eos/vbc/experiments/cms/store/user/liko/ZJetsToNuNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetToNuNu_HT-100To200_MC_UL18_CustomMiniAODv1-1/231112_223048/")
