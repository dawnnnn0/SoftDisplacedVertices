## Limit plots

### Setup

In addition to the CMSSW we currently have, we need an additional CMSSW environment for Combine:
https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/latest/#combine-v10-recommended-version

```
cmsrel CMSSW_14_1_0_pre4
cd CMSSW_14_1_0_pre4/src
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit

cd $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v10.0.2
scramv1 b clean; scramv1 b # always make a clean build
```

[A simple script](https://github.com/HephyAnalysisSW/SoftDisplacedVertices/blob/new_CMSSW/Plotter/limits/runCombine.sh) that automatically runs Combine using Asymptotic method is provided. You can put the script under `HiggsAnalysis/CombinedLimit` if you like.

Limit plots are produced with the following procedure:
- Run the autoplotter to get events in all serach regions:
```
./submitplotter.sh datacard_1 datacard
```
- After the jobs finish, `hadd` all of the output files:
```
./haddjobs.sh datacard_1
```
- Generate the datacards:
```
python3 datacard.py --year 2018
```
- Go to the Combine environment:
```
cd Combine/CMSSW_14_1_0_pre4/src
cmsenv
cd HiggsAnalysis/CombinedLimit
```
- Run Combine using the datacard:
```
./runCombine.sh /path/to/datacard
```
- Go back to the plotter CMSSW and make the limit plots:
```
cd path/to/CMSSW_13_3_0/src/SoftDisplacedVertices/Plotter/limits
python3 limitplot.py
```
