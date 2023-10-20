#!/bin/bash

export SCRAM_ARCH=slc7_amd64_gcc700
source /cvmfs/cms.cern.ch/cmsset_default.sh
n=5000
HOME="$PWD"
STORE="/scratch/felix.lang/SignalProduction"

SEED=$(($(date +%N) % 100 + 1))
echo simulating with seed = $SEED

if [ ! -r CMSSW_10_6_30/src ]; then
  scram p CMSSW CMSSW_10_6_30
fi
cd CMSSW_10_6_30/src
mkdir -p Configuration/GenProduction/python/
cp $HOME/test-fragment.py Configuration/GenProduction/python/fragment.py
eval `scram runtime -sh`
scram b

#LHE,GEN-SIM
cmsDriver.py Configuration/GenProduction/python/fragment.py --python_filename LHEGENSIM-cfg.py --eventcontent RAWSIM,LHE --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM,LHE --fileout file:LHEGENSIM.root --conditions 106X_upgrade2018_realistic_v4 --beamspot Realistic25ns13TeVEarly2018Collision --step LHE,GEN,SIM --geometry DB:Extended --era Run2_2018 --no_exec --mc --customise_commands process.RandomNumberGeneratorService.externalLHEProducer.initialSeed="int(${SEED})" -n $n
cmsRun LHEGENSIM-cfg.py

#PREMIX
cp $HOME/drivers/PREMIX-cfg.py PREMIX-cfg.py
cmsRun PREMIX-cfg.py

cd $HOME
if [ ! -r CMSSW_10_2_16_UL/src ]; then
  scram p CMSSW CMSSW_10_2_16_UL
fi
cd CMSSW_10_2_16_UL/src
eval `scram runtime -sh`
scram b

cp $HOME/CMSSW_10_6_30/src/PREMIX.root .

#HLT
cp $HOME/drivers/HLT-cfg.py HLT-cfg.py
cmsRun HLT-cfg.py

cd $HOME/CMSSW_10_6_30/src
eval `scramv1 runtime -sh`

cp $HOME/CMSSW_10_2_16_UL/src/HLT.root .

#AODSIM (with IVF1)
cp $HOME/drivers/AODSIM-IVF1-cfg.py AODSIM-IVF1-cfg.py
cmsRun AODSIM-IVF1-cfg.py

#MINIAOD
cp $HOME/drivers/MINIAODSIM-cfg.py MINIAODSIM-cfg.py
cmsRun MINIAODSIM-cfg.py

#NANOAOD
cp $HOME/drivers/NANOAODSIM-cfg.py NANOAODSIM-cfg.py
cmsRun NANOAODSIM-cfg.py

#COPY FILES
cd $STORE

directories=("samples" "samples/AODSIM" "samples/MINIAODSIM" "samples/NANOAODSIM")

for dir in "${directories[@]}"; do
  if [ ! -d "$dir" ]; then
    mkdir -p "$dir"
  fi
done

cp $HOME/CMSSW_10_6_30/src/AODSIM.root samples/AODSIM/testIVF1_AODSIM_STOPMASS_LSPMASS_CTAUVALUE_Standard_$$.root
cp $HOME/CMSSW_10_6_30/src/MINIAODSIM.root samples/MINIAODSIM/testIVF1_MINIAODSIM_STOPMASS_LSPMASS_CTAUVALUE_Standard_$$.root
cp $HOME/CMSSW_10_6_30/src/NANOAODSIM.root samples/NANOAODSIM/testIVF1_NANOAODSIM_STOPMASS_LSPMASS_CTAUVALUE_Standard_$$.root

rm -r $HOME/CMSSW_10_6_30
rm -r $HOME/CMSSW_10_2_16_UL