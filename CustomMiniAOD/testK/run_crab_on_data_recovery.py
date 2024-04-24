import subprocess

datasets = {
#     'Run2018A-15Feb2022': '/MET/Run2018A-15Feb2022_UL2018-v1/AOD',
#     'Run2018B-15Feb2022': '/MET/Run2018B-15Feb2022_UL2018-v1/AOD',
#     'Run2018C-15Feb2022': '/MET/Run2018C-15Feb2022_UL2018-v1/AOD',
    'Run2018D-15Feb2022': '/MET/Run2018D-15Feb2022_UL2018-v1/AOD',
}

notFinishedLumisJSON = {
#     'Run2018B-15Feb2022': '/users/alikaan.gueven/COPY/CMSSW_10_6_28/src/SoftDisplacedVertices/CustomMiniAOD/testK/crab_projects/crab_20240226_135242/results/notFinishedLumis.json',
#     'Run2018C-15Feb2022': '/users/alikaan.gueven/COPY/CMSSW_10_6_28/src/SoftDisplacedVertices/CustomMiniAOD/testK/crab_projects/crab_20240226_135304/results/notFinishedLumis.json',
    'Run2018D-15Feb2022': '/users/alikaan.gueven/COPY/CMSSW_10_6_28/src/SoftDisplacedVertices/CustomMiniAOD/testK/crab_projects/crab_20240222_191722/results/notPublishedLumis.json'
}


for tag, name in datasets.items():

    crabConfig = """
import CRABClient
from CRABClient.UserUtilities import config 

config = config()

config.General.requestName = '{}_recoveryTask_pv10'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '/users/alikaan.gueven/COPY/CMSSW_10_6_28/src/SoftDisplacedVertices/CustomMiniAOD/configuration/Data_UL18_CustomMiniAOD.py'
config.JobType.maxMemoryMB = 8000
config.JobType.maxJobRuntimeMin = 1440
config.JobType.numCores = 4

config.Data.inputDataset = '{}'
config.Data.inputDBS = 'global'
# config.Data.splitting = 'Automatic'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1

config.Data.publication = True
config.Data.outputDatasetTag = '{}_pv8'
config.Data.partialDataset = True
config.Data.ignoreLocality = True
config.Data.lumiMask = '{}'

# config.Site.ignoreGlobalBlacklist = True
config.Site.whitelist=["T2_AT_Vienna"]
# config.Site.blacklist=["T2_BR_SPRACE", "T2_IN_TIFR"]
config.Site.storageSite = "T2_AT_Vienna"

""".format(tag, name, tag, notFinishedLumisJSON[tag])
    with open("crabConfig_recovery.py", "w") as f:
        f.write(crabConfig)
    
    print name
    subprocess.call(['crab', 'submit', '-c', 'crabConfig_recovery.py'])

