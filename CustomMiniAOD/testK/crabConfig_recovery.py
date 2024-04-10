
import CRABClient
from CRABClient.UserUtilities import config 

config = config()

config.General.requestName = 'Run2018D-15Feb2022_UL2018-v1_recoveryTask_test'
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
config.Data.outputDatasetTag = 'Run2018D-15Feb2022_UL2018-v1'
config.Data.lumiMask = '/users/alikaan.gueven/COPY/CMSSW_10_6_28/src/SoftDisplacedVertices/CustomMiniAOD/testK/crab_projects/crab_20240222_191722/results/notPublishedLumis.json'
config.Data.ignoreLocality = True
# config.Data.partialDataset = True

# config.Site.ignoreGlobalBlacklist = True
# config.Site.blacklist=["T1_FR_CCIN2P3_Disk"]
config.Site.whitelist = ["T2_AT_Vienna"]
config.Site.storageSite = "T2_AT_Vienna"

