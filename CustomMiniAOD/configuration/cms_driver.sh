#!/bin/bash -x

declare -A MC_GT
MC_GT["UL16preVFP"]="106X_mcRun2_asymptotic_preVFP_v11"
MC_GT["UL16"]="106X_mcRun2_asymptotic_v17"
MC_GT["UL17"]="106X_mc2017_realistic_v9"
MC_GT["UL18"]="106X_upgrade2018_realistic_v16_L1v1"

declare -A MC_ERA
MC_ERA["UL16preVFP"]="Run2_2016_HIPM"
MC_ERA["UL16"]="Run2_2016"
MC_ERA["UL17"]="Run2_2017"
MC_ERA["UL18"]="Run2_2018"

for era in "UL16preVFP" "UL16" "UL17" "UL18"
do
    cmsDriver.py CustomMiniAOD --python_filename "MC_${era}_CustomMiniAOD.py" \
        --filein "file:AOD.root" \
        --fileout "MiniAOD.root" \
        --step PAT \
        --eventcontent MINIAODSIM \
        --datatier MINIAODSIM \
        --customise Configuration/DataProcessing/Utils.addMonitoring \
        --customise SoftDisplacedVertices/CustomMiniAOD/miniAOD_cff.miniAOD_customise_SoftDisplacedVerticesMC \
        --conditions "${MC_GT[$era]}" \
        --procModifiers run2_miniAOD_UL \
        --geometry DB:Extended \
        --era "${MC_ERA[$era]}" \
        --runUnscheduled \
        --no_exec \
        --mc


# does not work. Also geometry might be wrong

#    cmsDriver.py --python_filename "Data_${era}_CustomMiniAOD.py" \
#        --filein "file:AOD.root" \
#        --fileout "MiniAOD.root" \
#        --step PAT \
#        --eventcontent MINIAOD \
#        --datatier MINIAOD \
#        --customise Configuration/DataProcessing/Utils.addMonitoring \
#        --customise SoftDisplacedVertices/CustomMiniAOD/miniAOD_cff.miniAOD_customise_SoftDisplacedVertices \
#        --conditions "${DATA_GT[$era]}" \
#        --procModifiers run2_miniAOD_UL \
#        --geometry DB:Extended \
#        --era "${DATA_ERA[$era]}" \
#        --runUnscheduled \
#        --no_exec \
#        --data
done
