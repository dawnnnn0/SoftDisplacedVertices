#!/usr/bin/env python

import ROOT

ROOT.gROOT.SetBatch(True)
file1 = ROOT.TFile.Open("MET_2018A_CustomMiniAODv1-1.root")
hist1 = file1.Get("slimmedMet")
print(hist1)
file2 = ROOT.TFile.Open("MET_2018A_CustomMiniAODv1.root")
hist2 = file2.Get("slimmedMet")

c = ROOT.TCanvas()
hist2.Draw()
hist1.SetFillStyle(1001)
hist1.SetFillColor(1)
hist1.Draw("same")
c.SaveAs("plot.png")

