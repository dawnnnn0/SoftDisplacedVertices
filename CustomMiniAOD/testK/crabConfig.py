import CRABClient
from CRABClient.UserUtilities import config 

config = config()

# config.General.requestName = 'tutorial_Aug2021_Data_analysis'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '/users/alikaan.gueven/COPY/CMSSW_10_6_28/src/SoftDisplacedVertices/CustomMiniAOD/configuration/Data_UL18_CustomMiniAOD.py'


dataset_name = '/MET/Run2018D-15Feb2022_UL2018-v1/AOD'

config.JobType.maxMemoryMB = 3000
config.Data.inputDataset = dataset_name
config.Data.inputDBS = 'global'
config.Data.splitting = 'Automatic'
config.Data.publication = True
config.Data.outputDatasetTag = dataset_name

config.Site.storageSite = "T2_AT_Vienna"
