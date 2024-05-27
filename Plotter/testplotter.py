import os
import SoftDisplacedVertices.Plotter.plotter as p
import SoftDisplacedVertices.Plotter.plot_setting as ps
import SoftDisplacedVertices.Samples.Samples as s

if __name__=="__main__":
  lumi = 59683. # units in pb-1
  
  label = "MLNanoAODv2"
  input_json = "MLNanoAOD.json"
  ss = s.stop_2018
  s.loadData(ss,os.path.join(os.environ['CMSSW_BASE'],'src/SoftDisplacedVertices/Samples/json/{}'.format(input_json)),label)
  info_path = os.path.join(os.environ['CMSSW_BASE'],'src/SoftDisplacedVertices/Plotter/metadata_CustomMiniAOD_v3.yaml')

  evt_sel = "MET_pt>200&&HLT_PFMET120_PFMHT120_IDTight && Jet_pt[0]>100 && !nMuon && !nPhoton && !nTau && !nElectron && Flag_METFilters && Jet_chHEF[0]>0.1 && Jet_neHEF[0]<0.8"
  
  variables = ["SDVSecVtx_nTracks","SDVSecVtx_pAngle","SDVSecVtx_nGoodTrack","SDVSecVtx_dlen","SDVSecVtx_dlenSig","SDVSecVtx_dlen_err","SDVSecVtx_Lxy","SDVSecVtx_LxySig","SDVSecVtx_Lxy_err","SDVSecVtx_chi2","SDVSecVtx_normalizedChi2","SDVSecVtx_ndof","SDVSecVtx_L_eta_abs","SDVSecVtx_matchedLLPIdx_bydau","SDVSecVtx_matchedLLPnDau_bydau","SDVSecVtx_TkMaxdphi","SDVSecVtx_TkMindphi","SDVSecVtx_TkMaxdeta","SDVSecVtx_TkMindeta","SDVSecVtx_TkMaxdR","SDVSecVtx_TkMindR","SDVSecVtx_dphi_L_MET","SDVSecVtx_dphi_L_jet0"]

  dAddVar = {
      # Example:
      #"SDVSecVtx_dphi_L_MET":"acos(cos(SDVSecVtx_L_phi-MET_phi))",
      }

  d_varsel = {
      #label:(variables,selection)
      "tag": (variables,"SDVSecVtx_ParTScore>0.98"),
      "untag": (variables,"SDVSecVtx_ParTScore<0.98"),
      "genmatch": (variables,"SDVSecVtx_matchedLLPnDau_bydau>1"),
      "genmatchtag": (variables,"SDVSecVtx_matchedLLPnDau_bydau>1 && SDVSecVtx_ParTScore>0.98"),
      }

  dplots = {
      #label:(plots,plots2d)
      "":(ps.plots.keys(),[]),
      "tag":(variables,[]),
      "untag":(variables,[]),
      "genmatch":(variables,[]),
      "genmatchtag":(variables,[]),
      }

  inputdict = {
      'lumi':lumi,
      'presel': evt_sel,
      'info_path': info_path,
      'dAddVar': dAddVar,
      'd_varsel': d_varsel,
      'dplots': dplots,
      }
  plotter = p.Plotter(datalabel=label,lumi=lumi,presel=evt_sel,info_path=info_path,d_addvar=dAddVar,d_varsel=d_varsel,dplots=dplots)

  for sample in ss:
    plotter.setSample(sample)
    plotter.makeHistFiles("test")
    break
