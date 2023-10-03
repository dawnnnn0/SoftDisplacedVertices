"""
WARNING:
You must adapt your the input source and output filename before you run this.
"""

# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: --python_filename miniAOD_generation2_cfg.py --eventcontent MINIAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier MINIAODSIM --fileout file:SUS-RunIISummer20UL18MiniAODv2-00068.root --conditions 106X_upgrade2018_realistic_v16_L1v1 --step PAT --procModifiers run2_miniAOD_UL --geometry DB:Extended --filein dbs:/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v1/AODSIM --era Run2_2018 --runUnscheduled --no_exec --mc -n 100
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run2_2018_cff import Run2_2018
from Configuration.ProcessModifiers.run2_miniAOD_UL_cff import run2_miniAOD_UL

from SoftDisplacedVertices.VtxReco.VertexReco_cff import VertexFilterSeq
import HLTrigger.HLTfilters.hltHighLevel_cfi as hlt


process = cms.Process('customMiniAODv2',Run2_2018,run2_miniAOD_UL)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('PhysicsTools.PatAlgos.slimming.metFilterPaths_cff')
process.load('Configuration.StandardSequences.PATMC_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

# Import Ang's configurations
process.load("SoftDisplacedVertices.VtxReco.VertexReco_cff")
process.load("SoftDisplacedVertices.VtxReco.GenProducer_cfi")
process.load("SoftDisplacedVertices.VtxReco.GenMatchedTracks_cfi")
process.load("TrackingTools/TransientTrack/TransientTrackBuilder_cfi")

# Import IsolatedTrack equivalent collections
process.load("SoftDisplacedVertices.VtxReco.VertexTracks_cfi")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/0798C2C1-91C9-AE40-A8AD-9C6298204B60.root', 
        '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/0828F7CE-98C4-7F4B-8CD1-3D68E33EA7A1.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/0BBC6E3D-B41A-C242-88C6-E77AC709BF57.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/0F8A8E4B-43F8-3F4E-83B0-20231F327BCC.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/12C75DAA-8550-B349-BC68-40483A19CBEB.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/1A9C85CD-D8E5-F24C-9824-9B21CD17673C.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/211AECA1-70FB-4844-8D15-969DA198C319.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/244BFDDF-478F-AF40-A8AB-861B4CB39508.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/29B445B4-DAB1-1140-A884-11B34FBF3FD4.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/2D063279-9AC6-FE44-AD73-D11BF66BCB82.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/2ECB421C-8065-CE4A-9BB5-C40997036E7E.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/333E4722-76B8-F844-AFC1-A47E916A0769.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/347EC03A-AF04-D447-94C3-003522C27BE3.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/36323FD3-EFAC-D641-8365-FA2CC54BC447.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/3B471127-D681-3542-B137-5DDBA0A3B46B.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/3B75234F-43F0-4B4F-A283-935444D661B2.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/451C0A7C-5A92-D041-B3C8-404FEBEF8CED.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/475B1C66-D494-D940-AC46-D74EAE414257.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/5587D3AF-751B-2C47-8632-43C39349A7DB.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/58FA544D-3546-2445-8DD1-F4AF6C7AB052.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/5FEE226A-BD33-D641-9255-0614E43FBD7F.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/63D9F9F8-26BF-5B4E-A881-3A2AF649B276.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/6F5BA9CE-F870-C143-A370-26DE5C162A3F.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/78537866-8FA9-8A44-8C0D-E7EBAD7A8E97.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/7A1CA45C-11BD-CA42-BEF2-02AA22E2FEF9.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/7BBB7A4C-1458-2642-9A27-73C2FA3C8AE1.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/8034D13D-5083-C64B-A419-01B15784F313.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/82458460-B924-A44C-BCD2-C2948097F557.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/87D7D084-4505-7A47-99E6-F1A1CD127A58.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/8F3D339B-5014-104A-8E4C-7A4842205FCF.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/8F61C1AD-9740-AD4B-87D9-C849131540B5.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/90AA6CDC-26B8-CD48-82C2-C08692382215.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/9107DC29-CD08-C44B-80C7-64E51A0B56CE.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/9589AD42-1DDA-E440-B919-8272FBCF858B.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/9C68E8C7-94B0-9744-9FBF-C4AA68986EBF.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/9C78FA9F-519F-A04E-8F21-64B9213C24EE.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/9DB653E0-8082-224B-BC4A-31C8F0964097.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/A241B9C7-5AAD-FC40-AF00-00CEACE86AFC.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/A64DBB36-012A-BB44-866B-1FD6D3A0B181.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/B0483B4E-B0AD-6742-A807-553DDAA7627E.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/B302B1A4-DB20-BD49-BADC-A67654ABF2AE.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/B616C6E9-F12E-3942-9E2A-EB2F4C04BFC3.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/B8E69DAE-0BED-3F4A-9A66-85FA82A33B26.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/BA50AB99-8E94-9942-B0A7-F720E2139F45.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/BD699DC2-9AE2-EF41-8424-7D3FE0999D8B.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/C1FA18B0-820E-EA49-846F-9F58394411DB.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/C5064C20-4D82-D248-8121-E309132E2749.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/C6A425EF-F529-3241-AAF5-F56150675F5D.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/C6B696B0-4FFB-C34A-BF20-9E57714A0525.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/C75F0B16-65D8-3C46-A37A-C20F8307F61D.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/CAEA5B26-4930-5244-8793-64442936917D.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/CD632250-4021-144F-8D38-CB99FBC8B6A2.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/D2D3429A-F990-BE4D-B2D1-11BD6FF1FC3D.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/D5102477-AA4D-0843-9291-8CF279640AD9.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/D5CE7363-522E-1949-8F82-EEABAA673FC8.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/D9A381E1-A4B9-8340-B07C-68EE704094DA.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/DF3A7A26-28FF-9C47-87B4-49407BD727E0.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/DF7BD700-A3A9-3043-BA9A-6BC74671C196.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/E1F564CE-A523-934E-9702-74E2E994C41F.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/E8351CBD-53E3-B949-911D-75BB54C50E48.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/F2567D56-D6AA-C34B-846A-890C2450376F.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/FE4DA3A2-C387-B144-A259-78FA7B4CBB16.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2500000/FFAFFC14-70A8-D34F-84B2-C3DA78DE68AF.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2520000/1A25C813-CDF7-0444-A474-CF5AE10B4294.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2520000/1E4B6A11-6274-4F41-8D02-48520B2908C5.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2520000/53903D9A-675A-434C-8AE9-8C0623CDAE6B.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2520000/6AA0CF84-1CEE-3C46-8D63-90273A1E7F99.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2520000/93809E5B-1303-FE4B-B8D2-65437825D3F7.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2520000/DEE604C6-B900-9E41-9B23-7C17C6EB44B7.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2520000/FCB42924-825E-2543-BE77-A2A06998A5D5.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/2520000/FFB075DB-7DBE-AC4A-9D70-53ABB6B54BBD.root', 
        # '/store/mc/RunIISummer20UL18RECO/SMS-T2tt-4bd_genMET-100_genHT200_mStop-300_mLSP-290_TuneCP5_LLStop_13TeV-madgraphMLM-pythia8/AODSIM/106X_upgrade2018_realistic_v11_L1v1-v1/25210000/A292F69F-A82D-EC47-9D40-D9B545F733E9.root'
    ),
    secondaryFileNames = cms.untracked.vstring()
)



###### SKIP SOME EVENTS #########################################
# process.source.skipEvents = cms.untracked.uint32(19200)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('--python_filename nevts:100'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

output_mod = cms.OutputModule("PoolOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(4),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('MINIAODSIM'),
        filterName = cms.untracked.string('')
    ),
    dropMetaData = cms.untracked.string('ALL'),
    eventAutoFlushCompressedSize = cms.untracked.int32(-900),
    fastCloning = cms.untracked.bool(False),
    fileName = cms.untracked.string('file:/users/alikaan.gueven/AOD_to_nanoAOD/data/SUS-RunIISummer20UL18MiniAODv2-00068.root'),
    # maxSize = cms.untracked.int32(1), # kB
    outputCommands = process.MINIAODSIMEventContent.outputCommands,
    overrideBranchesSplitLevel = cms.untracked.VPSet(
        cms.untracked.PSet(
            branch = cms.untracked.string('patPackedCandidates_packedPFCandidates__*'),
            splitLevel = cms.untracked.int32(99)
        ), 
        cms.untracked.PSet(
            branch = cms.untracked.string('recoGenParticles_prunedGenParticles__*'),
            splitLevel = cms.untracked.int32(99)
        ), 
        cms.untracked.PSet(
            branch = cms.untracked.string('patTriggerObjectStandAlones_slimmedPatTrigger__*'),
            splitLevel = cms.untracked.int32(99)
        ), 
        cms.untracked.PSet(
            branch = cms.untracked.string('patPackedGenParticles_packedGenParticles__*'),
            splitLevel = cms.untracked.int32(99)
        ), 
        cms.untracked.PSet(
            branch = cms.untracked.string('patJets_slimmedJets__*'),
            splitLevel = cms.untracked.int32(99)
        ), 
        cms.untracked.PSet(
            branch = cms.untracked.string('recoVertexs_offlineSlimmedPrimaryVertices__*'),
            splitLevel = cms.untracked.int32(99)
        ), 
        cms.untracked.PSet(
            branch = cms.untracked.string('recoCaloClusters_reducedEgamma_reducedESClusters_*'),
            splitLevel = cms.untracked.int32(99)
        ), 
        cms.untracked.PSet(
            branch = cms.untracked.string('EcalRecHitsSorted_reducedEgamma_reducedEBRecHits_*'),
            splitLevel = cms.untracked.int32(99)
        ), 
        cms.untracked.PSet(
            branch = cms.untracked.string('EcalRecHitsSorted_reducedEgamma_reducedEERecHits_*'),
            splitLevel = cms.untracked.int32(99)
        ), 
        cms.untracked.PSet(
            branch = cms.untracked.string('recoGenJets_slimmedGenJets__*'),
            splitLevel = cms.untracked.int32(99)
        ), 
        cms.untracked.PSet(
            branch = cms.untracked.string('patJets_slimmedJetsPuppi__*'),
            splitLevel = cms.untracked.int32(99)
        ), 
        cms.untracked.PSet(
            branch = cms.untracked.string('EcalRecHitsSorted_reducedEgamma_reducedESRecHits_*'),
            splitLevel = cms.untracked.int32(99)
        )
    ),
    overrideInputFileSplitLevels = cms.untracked.bool(True),
    splitLevel = cms.untracked.int32(0)
)

# Preparing Ang's output definitions in the MiniAOD output
# output_mod.outputCommands.append('drop *') # already included in MINIAODSIMEventContent.outputCommands
output_mod.outputCommands.append('keep *_VertexTracksFilter_*_*')
output_mod.outputCommands.append('keep *_VertexTracks_*_*')
process.MINIAODSIMoutput = output_mod

# process.MINIAODSIMEventContent.outputCommands.append('keep *_VertexTracksFilter_*_*')
# process.RAWMINIAODSIMEventContent.outputCommands.append('keep *_VertexTracksFilter_*_*')

# HLT trigger requirement
process.trig_filter = hlt.hltHighLevel.clone(
    HLTPaths = ['HLT_PFMET120_PFMHT120_IDTight_v*'],
    throw = False
)


# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '106X_upgrade2018_realistic_v16_L1v1', '')



# Defining globally acessible service object that does not affect physics results.
process.TFileService = cms.Service("TFileService", fileName = cms.string("/users/alikaan.gueven/AOD_to_nanoAOD/data/vtxreco_histos.root") )

VertexFilterSeq(process, useMINIAOD=False, useIVF=True)
process.p = cms.Path(process.VertexTracksFilter + process.trig_filter + process.vtxfilter)


# Path and EndPath definitions
process.Flag_trackingFailureFilter = cms.Path(process.goodVertices+process.trackingFailureFilter)
process.Flag_goodVertices = cms.Path(process.primaryVertexFilter)
process.Flag_CSCTightHaloFilter = cms.Path(process.CSCTightHaloFilter)
process.Flag_trkPOGFilters = cms.Path(process.trkPOGFilters)
process.Flag_HcalStripHaloFilter = cms.Path(process.HcalStripHaloFilter)
process.Flag_trkPOG_logErrorTooManyClusters = cms.Path(~process.logErrorTooManyClusters)
process.Flag_hfNoisyHitsFilter = cms.Path(process.hfNoisyHitsFilter)
process.Flag_EcalDeadCellTriggerPrimitiveFilter = cms.Path(process.EcalDeadCellTriggerPrimitiveFilter)
process.Flag_ecalLaserCorrFilter = cms.Path(process.ecalLaserCorrFilter)
process.Flag_globalSuperTightHalo2016Filter = cms.Path(process.globalSuperTightHalo2016Filter)
process.Flag_eeBadScFilter = cms.Path(process.eeBadScFilter)
process.Flag_METFilters = cms.Path(process.metFilters)
process.Flag_chargedHadronTrackResolutionFilter = cms.Path(process.chargedHadronTrackResolutionFilter)
process.Flag_globalTightHalo2016Filter = cms.Path(process.globalTightHalo2016Filter)
process.Flag_CSCTightHaloTrkMuUnvetoFilter = cms.Path(process.CSCTightHaloTrkMuUnvetoFilter)
process.Flag_HBHENoiseIsoFilter = cms.Path(process.HBHENoiseFilterResultProducer+process.HBHENoiseIsoFilter)
process.Flag_BadChargedCandidateSummer16Filter = cms.Path(process.BadChargedCandidateSummer16Filter)
process.Flag_hcalLaserEventFilter = cms.Path(process.hcalLaserEventFilter)
process.Flag_BadPFMuonFilter = cms.Path(process.BadPFMuonFilter)
process.Flag_ecalBadCalibFilter = cms.Path(process.ecalBadCalibFilter)
process.Flag_HBHENoiseFilter = cms.Path(process.HBHENoiseFilterResultProducer+process.HBHENoiseFilter)
process.Flag_trkPOG_toomanystripclus53X = cms.Path(~process.toomanystripclus53X)
process.Flag_EcalDeadCellBoundaryEnergyFilter = cms.Path(process.EcalDeadCellBoundaryEnergyFilter)
process.Flag_BadChargedCandidateFilter = cms.Path(process.BadChargedCandidateFilter)
process.Flag_trkPOG_manystripclus53X = cms.Path(~process.manystripclus53X)
process.Flag_BadPFMuonSummer16Filter = cms.Path(process.BadPFMuonSummer16Filter)
process.Flag_muonBadTrackFilter = cms.Path(process.muonBadTrackFilter)
process.Flag_CSCTightHalo2015Filter = cms.Path(process.CSCTightHalo2015Filter)
process.Flag_BadPFMuonDzFilter = cms.Path(process.BadPFMuonDzFilter)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.MINIAODSIMoutput_step = cms.EndPath(process.MINIAODSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.p,
                                process.Flag_HBHENoiseFilter,
                                process.Flag_HBHENoiseIsoFilter,
                                process.Flag_CSCTightHaloFilter,
                                process.Flag_CSCTightHaloTrkMuUnvetoFilter,
                                process.Flag_CSCTightHalo2015Filter,
                                process.Flag_globalTightHalo2016Filter,
                                process.Flag_globalSuperTightHalo2016Filter,
                                process.Flag_HcalStripHaloFilter,
                                process.Flag_hcalLaserEventFilter,
                                process.Flag_EcalDeadCellTriggerPrimitiveFilter,
                                process.Flag_EcalDeadCellBoundaryEnergyFilter,
                                process.Flag_ecalBadCalibFilter,
                                process.Flag_goodVertices,
                                process.Flag_eeBadScFilter,
                                process.Flag_ecalLaserCorrFilter,
                                process.Flag_trkPOGFilters,
                                process.Flag_chargedHadronTrackResolutionFilter,
                                process.Flag_muonBadTrackFilter,
                                process.Flag_BadChargedCandidateFilter,
                                process.Flag_BadPFMuonFilter,
                                process.Flag_BadPFMuonDzFilter,
                                process.Flag_hfNoisyHitsFilter,
                                process.Flag_BadChargedCandidateSummer16Filter,
                                process.Flag_BadPFMuonSummer16Filter,
                                process.Flag_trkPOG_manystripclus53X,
                                process.Flag_trkPOG_toomanystripclus53X,
                                process.Flag_trkPOG_logErrorTooManyClusters,
                                process.Flag_METFilters,
                                process.endjob_step,
                                process.MINIAODSIMoutput_step
                                )


process.schedule.associate(process.patTask)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# customisation of the process.

# Automatic addition of the customisation function from Configuration.DataProcessing.Utils
from Configuration.DataProcessing.Utils import addMonitoring 

#call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
process = addMonitoring(process)

# End of customisation functions
#do not add changes to your config after this point (unless you know what you are doing)
from FWCore.ParameterSet.Utilities import convertToUnscheduled
process=convertToUnscheduled(process)

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.PatAlgos.slimming.miniAOD_tools
from PhysicsTools.PatAlgos.slimming.miniAOD_tools import miniAOD_customizeAllMC 

#call to customisation function miniAOD_customizeAllMC imported from PhysicsTools.PatAlgos.slimming.miniAOD_tools
process = miniAOD_customizeAllMC(process)

# End of customisation functions

# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
