#!/usr/bin/env python

import sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from DataFormats.FWLite import Events, Handle
from FWCore.ParameterSet.VarParsing import VarParsing


def main():
    """Plot pfMet."""
    ROOT.gROOT.SetBatch()
    options = VarParsing ('python')
    options.parseArguments()
    
    events = Events(options)
    handle = Handle('vector<reco::PFMET>')
    label = ("pfMet")
    
    h_genmet = ROOT.TH1F("pfMet", "pfMET", 100, 0., 2000.)
    for event in events:
        event.getByLabel(label, handle)
        
        genMetTrue = handle.product()
        
        h_genmet.Fill(genMetTrue[0].pt())
        
    c = ROOT.TCanvas()
    h_genmet.Draw()
    c.SaveAs("pfmet.png")

if __name__ == "__main__":
    main()
