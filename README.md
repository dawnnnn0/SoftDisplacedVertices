# SoftDisplacedVertices
Framework for Soft Displaced Vertices analysis.

This package is currently in a very preliminary stage. Tracks are selected and passed to the **InclusiveVertexFinder** to reconstruct secondary vertices.

This version utilizes the chain:
 [SUS-chain_RunIISummer20UL18wmLHEGEN_flowRunIISummer20UL18SIM_flowRunIISummer20UL18DIGIPremix_flowRunIISummer20UL18HLT_flowRunIISummer20UL18RECO_flowRunIISummer20UL18MiniAODv2_flowRunIISummer20UL18NanoAODv9-00066](https://cms-pdmv.cern.ch/mcm/chained_requests?prepid=SUS-chain_RunIISummer20UL18wmLHEGEN_flowRunIISummer20UL18SIM_flowRunIISummer20UL18DIGIPremix_flowRunIISummer20UL18HLT_flowRunIISummer20UL18RECO_flowRunIISummer20UL18MiniAODv2_flowRunIISummer20UL18NanoAODv9-00066).

[SUS-RunIISummer20UL18MiniAODv2-00068](https://cms-pdmv.cern.ch/mcm/requests?prepid=SUS-RunIISummer20UL18MiniAODv2-00068&page=0), is the first file we generate. \
[SUS-RunIISummer20UL18NanoAODv9-00068](https://cms-pdmv.cern.ch/mcm/requests?prepid=SUS-RunIISummer20UL18NanoAODv9-00068&page=0) is the final product.

For different MC files it might be worth checking:
 - [History of MC Production Campaigns](https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmVMcCampaigns)
 - [NanoAOD Specific Explanations for the MC Campaigns](https://gitlab.cern.ch/cms-nanoAOD/nanoaod-doc/-/wikis/home)

\
In this repository there are two configuration files (*_cfg.py) that can be run by cmsRun:

 - customMiniAODv2_cfg.py: Produces miniAODv2 and appends a custom collection of filtered reco::Tracks.

 - customNanoAOD_cfg.py: Reconstructs secondary vertices, and produces NanoAOD. The output (nanoAOD) contains only flat n-tuples.

To set up the environment:
```
cmsrel CMSSW_10_6_27
cd CMSSW_10_6_27/src
git clone git@github.com:HephyAnalysisSW/SoftDisplacedVertices.git
git checkout main
scram b -j8
```



To produce miniAOD:
```
cd CMSSW_10_6_27/src/CustomMiniAOD/test_cfg
cmsenv
bash MC_UL18_CustomMiniAOD.sh
```

To produce nanoAOD:
```
cd CMSSW_10_6_27/src/CustomNanoAOD/test_cfg
cmsenv
bash MC_UL18_CustomNanoAOD.sh
```

N.B. Please modify the paths to the input and output files in:
 - SoftDisplacedVertices/CustomMiniAOD/test_cfg/MC_UL18_CustomMiniAOD.sh
 - SoftDisplacedVertices/CustomNanoAOD/test_cfg/MC_UL18_CustomNanoAOD.sh