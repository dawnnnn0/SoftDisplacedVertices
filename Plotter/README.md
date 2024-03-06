# Plotter

A plotter is developed to make plots in a flexible way. 

## Script description:

To ba added.

## Prerequisites:

- The NanoAOD files are recorded in a json file, like the ones under `SoftDisplacedVertices/Samples/json`.
- If Filters are applied before or during the generation of MiniAOD, a metadata yaml file should be available to provide the information of total events generated without filters. This ensures the normalisation for MC is done correctly.

## Environmental setup:

For the first time to run the code, set up CMSSW 13 or above:

```
cmsrel CMSSW\_13\_0\_0
cd CMSSW\_13\_3\_0/src
git clone git@github.com:HephyAnalysisSW/SoftDisplacedVertices.git
git checkout new\_CMSSW
scram b -j 8
cmsenv
```

The above setup has to be done only once. If already set up, just do:
```
cd CMSSW\_13\_3\_0/src
cmsenv
```

## Steps:

First, generate the metadata yaml files if not already available:
```
python3 getMCInfo.py --sample_version CustomMiniAOD_v3 --json CustomMiniAOD_v3 --outDir ../Samples/json/
```

Then generate the histograms:
```
python3 autoplotter.py --sample stop_M600_580_ct2_2018 --output ./ --config /users/ang.li/public/SoftDV/CMSSW_13_3_0/src/SoftDisplacedVertices/Plotter/plotconfig_sig.yaml --lumi 59683. --json MLNanoAOD.json --metadata metadata_CustomMiniAOD_v3.yaml --datalabel MLNanoAODv2

```

To compare histograms, do:
```
python3 compare.py --input /users/ang.li/public/SoftDV/CMSSW_13_3_0/src/SoftDisplacedVertices/Plotter/plots_ML_METSlice/bkg_2018_MLNanoAODv0_hist.root /users/ang.li/public/SoftDV/CMSSW_13_3_0/src/SoftDisplacedVertices/Plotter/plots_ML_METSlice/stop_M600_588_ct200_2018_MLNanoAODv0_hist.root --dirs '' --nice 'signal' 'bkg' --scale
```
