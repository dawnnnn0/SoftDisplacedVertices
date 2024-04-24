import subprocess


notFinishedLumisJSON = {
#     'Run2018B-15Feb2022': '/users/alikaan.gueven/COPY/CMSSW_10_6_28/src/SoftDisplacedVertices/CustomMiniAOD/testK/crab_projects/crab_20240226_135242/results/notFinishedLumis.json',
#     'Run2018C-15Feb2022': '/users/alikaan.gueven/COPY/CMSSW_10_6_28/src/SoftDisplacedVertices/CustomMiniAOD/testK/crab_projects/crab_20240226_135304/results/notFinishedLumis.json',
    'Run2018D-15Feb2022_UL2018-v1': '/users/alikaan.gueven/COPY/CMSSW_10_6_28/src/SoftDisplacedVertices/CustomMiniAOD/testK/crab_projects/crab_20240222_191722/results/notPublishedLumis.json'
}


for tag, name in notFinishedLumisJSON.items():

    crabConfig = """
import CRABClient
from CRABClient.UserUtilities import config 

config = config()

config.General.requestName = '{}_recoveryTask_test'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '/users/alikaan.gueven/COPY/CMSSW_10_6_28/src/SoftDisplacedVertices/CustomMiniAOD/configuration/Data_UL18_CustomMiniAOD.py'
config.JobType.maxMemoryMB = 8000
config.JobType.numCores = 4

config.Data.userInputFiles = open('/users/alikaan.gueven/tmp/missingFilesRun2018D.txt').readlines()
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.totalUnits = 77
config.Data.publication = True
config.Data.outputPrimaryDataset = 'MET'
config.Data.outputDatasetTag = '{}'
config.Data.lumiMask = '{}'
config.Data.ignoreLocality = True
# config.Data.partialDataset = True

# config.Site.ignoreGlobalBlacklist = True
# config.Site.blacklist=["T1_FR_CCIN2P3_Disk"]
config.Site.whitelist = ["T2_AT_Vienna"]
config.Site.storageSite = "T2_AT_Vienna"

""".format(tag, tag, notFinishedLumisJSON[tag])
    with open("crabConfig_recovery.py", "w") as f:
        f.write(crabConfig)
    
    print name
    subprocess.call(['crab', 'submit', '-c', 'crabConfig_recovery.py'])

