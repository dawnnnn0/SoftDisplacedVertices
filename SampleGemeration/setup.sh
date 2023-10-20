#!/bin/bash

export SCRAM_ARCH=slc7_amd64_gcc700
source /cvmfs/cms.cern.ch/cmsset_default.sh
n=5000
HOME="$PWD"

if [ ! -d "setup" ]; then
    mkdir -p "setup"
  fi
cd setup

if [ ! -r CMSSW_10_6_30/src ]; then
  scram p CMSSW CMSSW_10_6_30
fi
cd CMSSW_10_6_30/src
eval `scram runtime -sh`
scram b

cmsDriver.py  --python_filename PREMIX-cfg.py --eventcontent PREMIXRAW --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-DIGI --fileout file:PREMIX.root --pileup_input "dbs:/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL18_106X_upgrade2018_realistic_v11_L1v1-v2/PREMIX" --conditions 106X_upgrade2018_realistic_v11_L1v1 --step DIGI,DATAMIX,L1,DIGI2RAW --procModifiers premix_stage2 --geometry DB:Extended --filein file:LHEGENSIM.root --datamix PreMix --era Run2_2018 --runUnscheduled --no_exec --mc -n $n

cd ../..
if [ ! -r CMSSW_10_2_16_UL/src ]; then
  scram p CMSSW CMSSW_10_2_16_UL
fi
cd CMSSW_10_2_16_UL/src
eval `scram runtime -sh`
scram b

cmsDriver.py  --python_filename HLT-cfg.py --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RAW --fileout file:HLT.root --conditions 102X_upgrade2018_realistic_v15 --customise_commands 'process.source.bypassVersionCheck = cms.untracked.bool(True)' --step HLT:2018v32 --geometry DB:Extended --filein file:PREMIX.root --era Run2_2018 --no_exec --mc -n $n

cd ../..
cd CMSSW_10_6_30/src
eval `scramv1 runtime -sh`

cmsDriver.py  --python_filename AODSIM-cfg.py --eventcontent AODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier AODSIM --fileout file:AODSIM.root --conditions 106X_upgrade2018_realistic_v11_L1v1 --step RAW2DIGI,L1Reco,RECO,RECOSIM,EI --geometry DB:Extended --filein file:HLT.root --era Run2_2018 --runUnscheduled --no_exec --mc -n $n

cmsDriver.py  --python_filename MINIAODSIM-cfg.py --eventcontent MINIAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier MINIAODSIM --fileout file:MINIAODSIM.root --conditions 106X_upgrade2018_realistic_v16_L1v1 --step PAT --procModifiers run2_miniAOD_UL --geometry DB:Extended --filein file:AODSIM.root --era Run2_2018 --runUnscheduled --no_exec --mc -n $n

cmsDriver.py  --python_filename NANOAODSIM-cfg.py --eventcontent NANOEDMAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:NANOAODSIM.root --conditions 106X_upgrade2018_realistic_v16_L1v1 --step NANO --filein file:MINIAODSIM.root --era Run2_2018,run2_nanoAOD_106Xv2 --no_exec --mc -n $n

cd $HOME
if [ ! -d "drivers" ]; then
    mkdir -p "drivers"
  fi

cp setup/CMSSW_10_6_30/src/PREMIX-cfg.py drivers/PREMIX-cfg.py
cp setup/CMSSW_10_2_16_UL/src/HLT-cfg.py drivers/HLT-cfg.py
cp setup/CMSSW_10_6_30/src/AODSIM-cfg.py drivers/AODSIM-cfg.py
cp setup/CMSSW_10_6_30/src/AODSIM-cfg.py drivers/AODSIM-IVF1-cfg.py
config_content=$(cat <<EOL
#####################################

process.inclusiveVertexFinder.minPt = cms.double(0.5)
process.inclusiveVertexFinder.minHits = cms.uint32(6)
process.inclusiveVertexFinder.maximumLongitudinalImpactParameter = cms.double(20.)
process.inclusiveVertexFinder.vertexMinAngleCosine = cms.double(0.00001)

process.trackVertexArbitrator.dRCut = cms.double(1.57)
process.trackVertexArbitrator.distCut = cms.double(0.1)
process.trackVertexArbitrator.trackMinPixels = cms.int32(0)

#####################################
EOL
)
echo "$config_content" >> "drivers/AODSIM-IVF1-cfg.py"
cp setup/CMSSW_10_6_30/src/MINIAODSIM-cfg.py drivers/MINIAODSIM-cfg.py
cp setup/CMSSW_10_6_30/src/NANOAODSIM-cfg.py drivers/NANOAODSIM-cfg.py

rm -r setup