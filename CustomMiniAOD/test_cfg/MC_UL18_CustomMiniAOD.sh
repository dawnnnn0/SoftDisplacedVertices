#!/bin/bash -x

cmsRun ./MC_UL18_CustomMiniAOD.py \
   inputFiles="/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/0798C2C1-91C9-AE40-A8AD-9C6298204B60.root" \
   outputFile="/scratch-cbe/users/$USER/MC_UL18_CustomMiniAOD.root" \
   maxEvents=10
