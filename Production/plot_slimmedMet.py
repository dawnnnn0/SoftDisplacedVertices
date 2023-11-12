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
    handle = Handle('vector<pat::MET>')
    label = ("slimmedMETs")
    
    h_genmet = ROOT.TH1F("slimmedMet", "slimmedMET", 100, 0., 2000.)
    for event in events:
        event.getByLabel(label, handle)
        
        slimmedMETs = handle.product()
        
        h_genmet.Fill(slimmedMETs[0].pt())
        
    c = ROOT.TCanvas()
    h_genmet.Draw()
    c.SaveAs("slimmedmet.png")

if __name__ == "__main__":
    main()
