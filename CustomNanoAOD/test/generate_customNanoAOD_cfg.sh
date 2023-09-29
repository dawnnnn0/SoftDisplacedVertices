#!/bin/bash

# Maximum validation duration: 28800s
# Margin for validation duration: 30%
# Validation duration with margin: 28800 * (1 - 0.30) = 20160s
# Time per event for each sequence: 0.4300s
# Threads for each sequence: 2
# Time per event for single thread for each sequence: 2 * 0.4300s = 0.8600s
# Which adds up to 0.8600s per event
# Single core events that fit in validation duration: 20160s / 0.8600s = 23441
# Produced events limit in McM is 10000
# According to 1.0000 efficiency, validation should run 10000 / 1.0000 = 10000 events to reach the limit of 10000
# Take the minimum of 23441 and 10000, but more than 0 -> 10000
# It is estimated that this validation will produce: 10000 * 1.0000 = 10000 events
EVENTS=-1


# cmsDriver command
cmsDriver.py  --python_filename NanoAOD_generation_cfg.py                                                       \
              --eventcontent NANOAODSIM                                                                         \
              --customise Configuration/DataProcessing/Utils.addMonitoring                                      \
              --datatier NANOAODSIM                                                                             \
              --fileout file:/users/alikaan.gueven/AOD_to_nanoAOD/data/SUS-RunIISummer20UL18NanoAOD-00069.root  \
              --conditions 106X_upgrade2018_realistic_v16_L1v1                                                  \
              --step NANO                                                                                       \
              --filein "file:/users/alikaan.gueven/AOD_to_nanoAOD/data/SUS-RunIISummer20UL18MiniAOD-00069.root" \
              --era Run2_2018,run2_nanoAOD_106Xv2                                                               \
              --no_exec                                                                                         \
              --mc                                                                                              \
              -n $EVENTS ;
