
import CRABClient
from CRABClient.UserUtilities import config 

config = config()

# config.General.requestName = 'tutorial_Aug2021_Data_analysis'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '/users/alikaan.gueven/COPY/CMSSW_10_6_28/src/SoftDisplacedVertices/CustomNanoAOD/configuration/Data_UL18_CustomNanoAOD.py'
config.JobType.maxMemoryMB = 8000
config.JobType.numCores = 4

config.Data.inputDataset = '/MET/aguven-Run2018A-15Feb2022_UL2018-v1-dd1ffd5402fcc3f75701653b84d21aa6/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'Automatic'
config.Data.publication = True
config.Data.outputDatasetTag = 'Run2018A-15Feb2022_CustomNanoAOD_golden_v1'
config.Data.lumiMask = 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt'
# config.Data.ignoreLocality = True

config.Site.blacklist=["T2_BR_SPRACE"]
# config.Site.whitelist=["T2_AT_Vienna"]
# config.Site.ignoreGlobalBlacklist = True
config.Site.storageSite = "T2_AT_Vienna"
