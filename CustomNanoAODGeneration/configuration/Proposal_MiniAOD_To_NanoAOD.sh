#!/bin/bash -x

[ "$CMSSW_VERSION" != "CMSSW_10_2_22" ] && exit 1

cmsRun ./Proposal_MiniAOD_To_NanoAOD.py \
    inputFiles="file:/scratch-cbe/users/$USER/MiniAOD_numEvent100.root" \
    outputFile="/scratch-cbe/users/$USER/Proposal_NanoAOD.root" \
    maxEvents=100