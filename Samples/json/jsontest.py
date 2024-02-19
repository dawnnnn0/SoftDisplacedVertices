#!/usr/bin/env python

import json

d = {
  "AOD":{
    "dataset":{
    },
    "dir":{
      "stop_M600_588_ct200":"/eos/vbc/experiments/cms/store/user/felang/SignalProduction/samples/Stop/600_588_200/AODSIM/",
      "stop_M600_585_ct20":"/eos/vbc/experiments/cms/store/user/felang/SignalProduction/samples/Stop/600_585_20/AODSIM/",
      "stop_M600_580_ct2":"/eos/vbc/experiments/cms/store/user/felang/SignalProduction/samples/Stop/600_580_2/AODSIM/",
      "stop_M1000_988_ct200":"/eos/vbc/experiments/cms/store/user/felang/SignalProduction/samples/Stop/1000_988_200/AODSIM/",
      "stop_M1000_985_ct20":"/eos/vbc/experiments/cms/store/user/felang/SignalProduction/samples/Stop/1000_985_20/AODSIM/",
      "stop_M1000_980_ct2":"/eos/vbc/experiments/cms/store/user/felang/SignalProduction/samples/Stop/1000_980_2/AODSIM/",
    },
  },
  "CustomMiniAODv1-1":{
    "dataset":{
      "zjetstonunuht0100_2018":"/ZJetsToNuNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/liko-ZJetToNuNu_HT-100To200_MC_UL18_CustomMiniAODv1-1-d89a5f51c8622d62b5accbd8b7f90262/USER",
      "zjetstonunuht0200_2018":"/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/liko-ZJetsToNuNu_HT-200To400_MC_UL18_CustomMiniAODv1-1-d89a5f51c8622d62b5accbd8b7f90262/USER",
      "zjetstonunuht0400_2018":"/ZJetsToNuNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/liko-ZJetsToNuNu_HT-400To600_MC_UL18_CustomMiniAODv1-1-d89a5f51c8622d62b5accbd8b7f90262/USER",
      "zjetstonunuht0600_2018":"/ZJetsToNuNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/liko-ZJetsToNuNu_HT-600To800_MC_UL18_CustomMiniAODv1-1-d89a5f51c8622d62b5accbd8b7f90262/USER",
      "zjetstonunuht0800_2018":"/ZJetsToNuNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/liko-ZJetsToNuNu_HT-800To1200_MC_UL18_CustomMiniAODv1-1-d89a5f51c8622d62b5accbd8b7f90262/USER",
      "zjetstonunuht1200_2018":"/ZJetsToNuNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/liko-ZJetsToNuNu_HT-1200To2500_MC_UL18_CustomMiniAODv1-1-d89a5f51c8622d62b5accbd8b7f90262/USER",
      "zjetstonunuht2500_2018":"/ZJetsToNuNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/liko-ZJetsToNuNu_HT-2500ToInf_MC_UL18_CustomMiniAODv1-1-d89a5f51c8622d62b5accbd8b7f90262/USER",
    },
    "dir":{
    },
  },
  "CustomMiniAODv1":{
    "dataset":{
    },
    "dir":{
      "zjetstonunuht0100_2018":"/eos/vbc/experiments/cms/store/user/liko/ZJetsToNuNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetToNuNu_HT-100To200_MC_UL18_CustomMiniAODv1/231029_221218/",
      "zjetstonunuht0200_2018":"/eos/vbc/experiments/cms/store/user/liko/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT-200To400_MC_UL18_CustomMiniAODv1/231030_165533/",
      "zjetstonunuht0400_2018":"/eos/vbc/experiments/cms/store/user/liko/ZJetsToNuNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT-400To600_MC_UL18_CustomMiniAODv1/231029_221210/",
      "zjetstonunuht0600_2018":"/eos/vbc/experiments/cms/store/user/liko/ZJetsToNuNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT-600To800_MC_UL18_CustomMiniAODv1/231029_221234/",
      "zjetstonunuht0800_2018":"/eos/vbc/experiments/cms/store/user/liko/ZJetsToNuNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT-800To1200_MC_UL18_CustomMiniAODv1/231029_221258/",
      "zjetstonunuht1200_2018":"/eos/vbc/experiments/cms/store/user/liko/ZJetsToNuNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT-1200To2500_MC_UL18_CustomMiniAODv1/231029_221242/",
      "zjetstonunuht2500_2018":"/eos/vbc/experiments/cms/store/user/liko/ZJetsToNuNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetsToNuNu_HT-2500ToInf_MC_UL18_CustomMiniAODv1/231029_221250/",
    },
  },
}


with open("test.json", "w") as f:
  json.dump(d,f, indent=4)
