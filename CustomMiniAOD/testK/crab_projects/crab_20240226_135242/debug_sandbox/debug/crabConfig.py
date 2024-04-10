from WMCore.Configuration import Configuration
config = Configuration()
config.section_('General')
config.General.transferOutputs = True
config.General.workArea = 'crab_projects'
config.section_('JobType')
config.JobType.psetName = '/users/alikaan.gueven/COPY/CMSSW_10_6_28/src/SoftDisplacedVertices/CustomMiniAOD/configuration/Data_UL18_CustomMiniAOD.py'
config.JobType.pluginName = 'Analysis'
config.JobType.numCores = 4
config.JobType.maxMemoryMB = 8000
config.section_('Data')
config.Data.inputDataset = '/MET/Run2018B-15Feb2022_UL2018-v1/AOD'
config.Data.outputDatasetTag = 'Run2018B-15Feb2022'
config.Data.publication = True
config.Data.partialDataset = True
config.Data.inputDBS = 'global'
config.Data.splitting = 'Automatic'
config.section_('Site')
config.Site.blacklist = ['T2_BR_SPRACE']
config.Site.storageSite = 'T2_AT_Vienna'
config.section_('User')
config.section_('Debug')
