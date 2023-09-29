#!/bin/bash +x

cmsRun ./MC_UL18_CustomNanoAOD.py \
  inputFiles="file:/scratch-cbe/users/$USER/MC_UL18_CustomMiniAOD_numEvent10.root" \
  outputFile="/scratch-cbe/users/$USER/MC_UL18_CustomNanoAOD.root" \
  maxEvents=10
