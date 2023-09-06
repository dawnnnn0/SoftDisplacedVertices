# SoftDisplacedVertices
Framework for Soft Displaced Vertices analysis.

This package is current in a very preliminary stage. Tracks are selected and passed to the Inclusive Vertex Finder to reconstruct secondary vertices.

Two config files can be run in the package:
- vtxreco\_cfg.py: take AOD or MINIAOD files as input and output a ROOT file (MINIAOD-like) including reconstructed vertices, beamspot, MET, and jets.
- eventtree.py: take the output of vtxreco\_cfg.py as input and output a plain TTree.

To set up the environment:
```
cmsrel CMSSW_10_6_30
cd CMSSW_10_6_30/src
git cms-init
git clone git@github.com:HephyAnalysisSW/SoftDisplacedVertices.git
scram b -j 4
```


