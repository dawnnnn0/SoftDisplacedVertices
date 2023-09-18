#!/bin/bash

# Maximum validation duration: 28800s
# Margin for validation duration: 30%
# Validation duration with margin: 28800 * (1 - 0.30) = 20160s
# Time per event for each sequence: 0.6000s
# Threads for each sequence: 4
# Time per event for single thread for each sequence: 4 * 0.6000s = 2.4000s
# Which adds up to 2.4000s per event
# Single core events that fit in validation duration: 20160s / 2.4000s = 8400
# Produced events limit in McM is 10000
# According to 1.0000 efficiency, validation should run 10000 / 1.0000 = 10000 events to reach the limit of 10000
# Take the minimum of 8400 and 10000, but more than 0 -> 8400
# It is estimated that this validation will produce: 8400 * 1.0000 = 8400 events
EVENTS=100

# cmsDriver command
cmsDriver.py  --python_filename customMiniAOD_cfg.py --eventcontent MINIAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier MINIAODSIM --fileout file:SUS-RunIISummer20UL18MiniAODv2-00068.root --conditions 106X_upgrade2018_realistic_v16_L1v1 --step PAT --procModifiers run2_miniAOD_UL --geometry DB:Extended --filein "dbs:/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v1/AODSIM" --era Run2_2018 --runUnscheduled --no_exec --mc -n $EVENTS || exit $? ;
