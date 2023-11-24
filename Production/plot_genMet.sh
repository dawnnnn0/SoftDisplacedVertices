#!/bin/bash

INPUT_URL="root://eos.grid.vbc.ac.at//eos/vbc/experiments/cms/store/user/liko/ZJetsToNuNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetToNuNu_HT-100To200_MC_UL18_CustomMiniAODv1/231029_221218/0000"
STAGE_PATH="/scratch-cbe/users/$USER/ZJetsToNuNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/ZJetToNuNu_HT-100To200_MC_UL18_CustomMiniAODv1/231029_221218/0000"
NR_FILES=3

mkdir -p "$STAGE_PATH"
inputFiles=()
for ((i=1; i<=$NR_FILES; ++i))
do
    path="$STAGE_PATH/MiniAOD_$i.root"
    inputFiles=( ${inputFiles[@]} ${path})
    if [ -e "$path" ]
    then
       continue
    fi
    xrdcp "$INPUT_URL/MiniAOD_$i.root" "$path"
done

IFS=,
./plot_pfMet.py inputFiles="${inputFiles[*]}"