#!/bin/bash -x

[ "$CMSSW_VERSION" != "CMSSW_10_2_22" ] && exit 1

cmsRun ./Proposal_AOD_To_MiniAOD.py \
    inputFiles="file:/scratch-cbe/users/dietrich.liko/antrag/stop4b_1000_975_0/TestAntragIVF1_AODSIM_1000_975_0_0.root" \
    outputFile="/scratch-cbe/users/$USER/Proposal_MiniAOD.root" \
    histoFile="/scratch-cbe/users/$USER/Proposal_MiniAOD_histo.root" \
    maxEvents=100
