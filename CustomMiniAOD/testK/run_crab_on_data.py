import subprocess

datasets = {
#     'Run2018A-15Feb2022': '/MET/Run2018A-15Feb2022_UL2018-v1/AOD',
    'Run2018B-15Feb2022': '/MET/Run2018B-15Feb2022_UL2018-v1/AOD',
    'Run2018C-15Feb2022': '/MET/Run2018C-15Feb2022_UL2018-v1/AOD',
#     'Run2018D-15Feb2022': '/MET/Run2018D-15Feb2022_UL2018-v1/AOD',
}


for tag, name in datasets.items():

    crabConfig = """
import CRABClient
from CRABClient.UserUtilities import config 

config = config()

# config.General.requestName = 'tutorial_Aug2021_Data_analysis'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '/users/alikaan.gueven/COPY/CMSSW_10_6_28/src/SoftDisplacedVertices/CustomMiniAOD/configuration/Data_UL18_CustomMiniAOD.py'
config.JobType.maxMemoryMB = 8000
config.JobType.numCores = 4

config.Data.inputDataset = '{}'
config.Data.inputDBS = 'global'
config.Data.splitting = 'Automatic'
config.Data.publication = True
config.Data.outputDatasetTag = '{}'
config.Data.partialDataset = True
# config.Data.ignoreLocality = True

config.Site.blacklist=["T2_BR_SPRACE"]
# config.Site.blacklist=["T2_BR_SPRACE", "T2_IT_Pisa"]
# config.Site.whitelist=["T1_RU_JINR_Tape"]
# config.Site.whitelist=["T1_RU*", "T1_US*"]
# config.Site.ignoreGlobalBlacklist = True

config.Site.storageSite = "T2_AT_Vienna"
""".format(name, tag)
    with open("crabConfig.py", "w") as f:
        f.write(crabConfig)
    
    print name
    subprocess.call(['crab', 'submit', '-c', 'crabConfig.py'])

