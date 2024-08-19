# Plotter

A plotter is developed to make plots in a flexible way. 

## Script description:

- autoplotter.py
This script generates root files that include histograms. Histograms will be organized in different directories based on search region definition and object selections.
Parameters:
`--sample`: input samples to make histograms. It has to be defined in the [Samples module](https://github.com/HephyAnalysisSW/SoftDisplacedVertices/blob/new_CMSSW/Samples/python/Samples.py) and can be a single sample (such as `wjetstolnuht0600_2018`) or a list of samples (`wlnu_2018`). For a list of samples, the script will generate one root file for each sample.

`--output`: directory of output.

`--config`: configure file that defines event selections and what variables to plot. [Example config](https://github.com/HephyAnalysisSW/SoftDisplacedVertices/blob/new_CMSSW/Plotter/configs/plotconfig_sig.yaml) is provided. When new variables are added, please add a new entry in the [plot\_setting module](https://github.com/HephyAnalysisSW/SoftDisplacedVertices/blob/new_CMSSW/Plotter/python/plot_setting.py) to set the plot binning and title.

`--lumi`: luminosity to normalise the MC, unit in `pb-1`.

`--json`: Name of the json file that records the file path of the samples. The default path is under `SoftDisplacedVertices/Samples/json`.

`--metadata`: Name of the yaml file that records the GenSumWeight of MC samples. The default path is under `SoftDisplacedVertices/Samples/json`.

`--datalabel`: Lable of the dataset used for making histogram. It should be consistent with what is available in the json file.

## Prerequisites:

- The NanoAOD files are recorded in a json file, like the ones under `SoftDisplacedVertices/Samples/json`.
- If Filters are applied before or during the generation of MiniAOD, a metadata yaml file should be available to provide the information of total events generated without filters. This ensures the normalisation for MC is done correctly.

## Environmental setup:

For the first time to run the code, set up CMSSW 13 or above:

```
cmsrel CMSSW_13_0_0
cd CMSSW_13_3_0/src
git clone git@github.com:HephyAnalysisSW/SoftDisplacedVertices.git
git checkout new_CMSSW
scram b -j 8
cmsenv
```

The above setup has to be done only once. If already set up, just do:
```
cd CMSSW_13_3_0/src
cmsenv
```

## Steps:

First, generate the metadata yaml files if not already available:
```
python3 getMCInfo.py --sample_version CustomMiniAOD_v3 --json CustomMiniAOD_v3 --outDir ../Samples/json/
```

Then generate the histograms:

To run interactively:
```
python3 autoplotter.py --sample stop_M600_580_ct2_2018 --output ./ --config /users/ang.li/public/SoftDV/CMSSW_13_3_0/src/SoftDisplacedVertices/Plotter/plotconfig_sig.yaml --lumi 59683. --json MLNanoAOD.json --metadata metadata_CustomMiniAOD_v3.yaml --datalabel MLNanoAODv2
```

To submit jobs:
```
python3 autoplotter.py --sample stop_2018 --output /eos/vbc/group/cms/ang.li/MLhists/MLNanoAODv2_submit/ --config /users/ang.li/public/SoftDV/CMSSW_13_3_0/src/SoftDisplacedVertices/Plotter/configs/plotconfig_sig.yaml --submit
```


To compare histograms, do:
```
python3 compare.py --input /users/ang.li/public/SoftDV/CMSSW_13_3_0/src/SoftDisplacedVertices/Plotter/plots_ML_METSlice/bkg_2018_MLNanoAODv0_hist.root /users/ang.li/public/SoftDV/CMSSW_13_3_0/src/SoftDisplacedVertices/Plotter/plots_ML_METSlice/stop_M600_588_ct200_2018_MLNanoAODv0_hist.root --dirs '' --nice 'signal' 'bkg' --scale
```

To [make CMS style comparison plots](https://cms-analysis.docs.cern.ch/guidelines/plotting/#__tabbed_1_2), new package is required:

Do this once in CMSSW:
```
cd CMSSW_13_3_0/src
scram-venv
pip3 install cmsstyle
```

Once the enviroment is set up, do:
```
python3 compare_data_new.py --data data_hist.root --bkg wjets_2018_hist.root zjets_2018_hist.root --bkgnice "WJets" "ZJets" --signal stop_M600_585_ct20_2018_hist.root --signice "signal" --output dir_output/ --dirs "All_SDVTrack_all" --commands "h.Rebin(5) if ('LxySig' in h.GetName()) else None" --ratio 
```
