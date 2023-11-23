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
    
    if len(options.inputFiles) == 1 and options.inputFiles[0].endswith(".txt"):
        inputFiles = open(options.inputFiles[0],"r").read().splitlines()
        inputFiles = [ "root://eos.grid.vbc.ac.at/"+f for f in inputFiles ]
        events = Events(inputFiles)
    else:
        events = Events(options)
    handle = Handle('vector<pat::MET>')
    label = ("slimmedMETs")
    
    h_genmet = ROOT.TH1F("slimmedMet", "slimmedMET", 100, 0., 2000.)
    for event in events:
        event.getByLabel(label, handle)
        
        slimmedMETs = handle.product()
        
        h_genmet.Fill(slimmedMETs[0].pt())

    rout = ROOT.TFile.Open(options.outputFile,"RECREATE")
    h_genmet.Write()
    rout.Close()
        
    c = ROOT.TCanvas()
    h_genmet.Draw()
    c.SaveAs(options.outputFile.split(".")[0]+".png")

if __name__ == "__main__":
    main()
