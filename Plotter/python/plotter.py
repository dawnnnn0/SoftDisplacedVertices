import os
import yaml
import ROOT
import SoftDisplacedVertices.Samples.Samples as s
import SoftDisplacedVertices.Plotter.plot_setting as ps
ROOT.gInterpreter.Declare('#include "{}/src/SoftDisplacedVertices/Plotter/RDFHelper.h"'.format(os.environ['CMSSW_BASE']))
ROOT.EnableImplicitMT(4)
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.TH1.SetDefaultSumw2(True)
ROOT.gStyle.SetOptStat(0)

class Plotter:
  def __init__(self,s=None,datalabel="",outputDir="./",lumi=1,info_path="",input_json="",config=""):
    self.s = None
    self.datalabel = datalabel
    self.outputDir = outputDir
    self.lumi = lumi
    self.info_path = info_path
    self.input_json = input_json
    with open(config, "r") as f_cfg:
      cfg = yaml.load(f_cfg, Loader=yaml.FullLoader)
    self.cfg = cfg



  #def __init__(self,s=None,datalabel="",outputDir="./",lumi=1,presel="",info_path="",input_json="",d_addvar=dict(),d_varsel=dict(),dplots=dict(),dregion=dict()):
  #  self.s = None
  #  self.datalabel = datalabel
  #  self.outputDir = outputDir
  #  self.lumi = lumi
  #  self.presel = presel
  #  self.info_path = info_path
  #  self.input_json = input_json
  #  self.dAddVar = d_addvar
  #  self.d_varsel = d_varsel
  #  self.dplots = dplots
  #  self.dregion = dregion

  def setLumi(self,lumi):
    self.lumi = lumi

  def setSample(self,s):
    self.s = s

  def valid(self):
    if self.s is None:
      return False
    return True

  def setPresel(self,presel):
    self.config['presel'] = presel
  def setSampleInfo(self,info_path):
    self.info_path = info_path

  def setJson(self,input_json):
    self.input_json = input_json

  def setAddVar(self,d_addvar):
    self.dAddVar = d_addvar

  def setVarWithSelection(self,d_varsel):
    """
    d_varsel = {
      label:(variables,selection)
    }
    """
    self.d_varsel = d_varsel

  def setdPlots(self,dplots):
    """
    dplots = {
      label:(plots,plots2d)
    }
    """
    self.dplots = dplots

  def defineRegions(self,dregion):
    """
    dregion = {
      region_name:"selections"
    }
    """
    self.dregion = dregion

  def getSumWeight(self):
    with open(self.info_path,'r') as f_sample_info:
      sample_info = yaml.safe_load(f_sample_info)
    for i in sample_info:
      if not self.s.name in i:
        continue
      return sample_info[i]['totalsumWeights']
    print("No sum weight record found for {}!".format(self.s.name))
    return -1
  
  def AddVars(self,d):
      d = d.Define("SDVTrack_isGoodTrack","( (abs(SDVTrack_dxy)/SDVTrack_dxyError)>4 ) && (SDVTrack_normalizedChi2 < 5) && (abs(SDVTrack_dz)<4.) && (SDVTrack_numberOfValidHits>13) && ( (SDVTrack_ptError/SDVTrack_pt)<0.015 ) && ( acos(cos(SDVTrack_phi-Jet_phi[0]))>1 ) && ( acos(cos(SDVTrack_phi-MET_phi))<1.5 )")
      d = d.Define("SDVSecVtx_nGoodTrack","SDVSecVtx_nGoodTrack(SDVIdxLUT_SecVtxIdx,SDVIdxLUT_TrackIdx,SDVTrack_isGoodTrack,nSDVSecVtx)")
      vtx_sel_CC = "( acos(cos(SDVSecVtx_L_phi-MET_phi))<1.5 )&&(SDVSecVtx_LxySig>=20.)&&(SDVSecVtx_pAngle>0.2)&&(SDVSecVtx_nGoodTrack>=2)&&( acos(cos(SDVSecVtx_L_phi-Jet_phi[0]))>1 ) && (SDVSecVtx_ndof>1)"
      vtx_sel_ML = "( acos(cos(SDVSecVtx_L_phi-MET_phi))<1.5 ) && (SDVSecVtx_ParTScore>0.98) && ( acos(cos(SDVSecVtx_L_phi-Jet_phi[0]))>1 )"
      d = d.Define("nSDVSecVtx_CCsel","Sum({})".format(vtx_sel_CC))
      d = d.Define("nSDVSecVtx_MLsel","Sum({})".format(vtx_sel_ML))
  
      d = d.Define("SDVSecVtx_dphi_L_MET","acos(cos(SDVSecVtx_L_phi-MET_phi))")
      d = d.Define("SDVSecVtx_dphi_L_jet0","acos(cos(SDVSecVtx_L_phi-Jet_phi[0]))")
  
      d = d.Define("SDVSecVtx_LxySig_CCsel_max","Max(SDVSecVtx_LxySig[{}])".format(vtx_sel_CC))
      d = d.Define("SDVSecVtx_LxySig_MLsel_max","Max(SDVSecVtx_LxySig[{}])".format(vtx_sel_ML))
      d = d.Define("SDVSecVtx_Lxy_err","SDVSecVtx_Lxy/SDVSecVtx_LxySig")
      d = d.Define("SDVSecVtx_dlen_err","SDVSecVtx_dlen/SDVSecVtx_dlenSig")
      d = d.Define("SDVSecVtx_L_eta_abs","abs(SDVSecVtx_L_eta)")
  
      d = d.Define("SDVSecVtx_TkMaxdphi","SDV_TkMaxdphi(SDVIdxLUT_TrackIdx, SDVIdxLUT_SecVtxIdx, nSDVSecVtx, SDVTrack_phi)")
      d = d.Define("SDVSecVtx_TkMindphi","SDV_TkMindphi(SDVIdxLUT_TrackIdx, SDVIdxLUT_SecVtxIdx, nSDVSecVtx, SDVTrack_phi)")
      d = d.Define("SDVSecVtx_TkMaxdeta","SDV_TkMaxdphi(SDVIdxLUT_TrackIdx, SDVIdxLUT_SecVtxIdx, nSDVSecVtx, SDVTrack_eta)")
      d = d.Define("SDVSecVtx_TkMindeta","SDV_TkMindphi(SDVIdxLUT_TrackIdx, SDVIdxLUT_SecVtxIdx, nSDVSecVtx, SDVTrack_eta)")
      d = d.Define("SDVSecVtx_TkMaxdR","SDV_TkMaxdR(SDVIdxLUT_TrackIdx, SDVIdxLUT_SecVtxIdx, nSDVSecVtx, SDVTrack_eta, SDVTrack_phi)")
      d = d.Define("SDVSecVtx_TkMindR","SDV_TkMindR(SDVIdxLUT_TrackIdx, SDVIdxLUT_SecVtxIdx, nSDVSecVtx, SDVTrack_eta, SDVTrack_phi)")
      if self.cfg['new_variables'] is not None:
        for newvar in self.cfg['new_variables']:
          d = d.Define(newvar,self.cfg['new_variables'][newvar])
      return d
  
  def AddVarsWithSelection(self,d):
    for obj in self.cfg['objects']:
      selections = self.cfg['objects'][obj]['selections']
      variables  = self.cfg['objects'][obj]['variables']
      for sel in selections:
        for v in variables:
          d = d.Define(v+sel,"{0}[{1}]".format(v,selections[sel]))
    return d
  
  def FilterEvents(self,d):
    d_filter = d.Filter(self.presel)
    return d_filter

  def AddWeights(self,d,weight):
      d = d.Define("evt_weight","Generator_weight*{0}".format(weight))
      return d
  
  def getRDF(self):
    '''
    This function gets RDataFrame for a given sample
    - Add desired variables
    - Filter events
    - Produce normalisation weights based on xsec
    '''
    fns = self.s.getFileList(self.datalabel,"")
    d = ROOT.RDataFrame("Events",fns)
    d = self.AddVars(d)
    d = self.AddVarsWithSelection(d)
    if self.cfg['presel'] is not None:
      d = d.Filter(self.cfg['presel'])
    nevt = self.getSumWeight()
    if nevt==-1:
      print("No sum weight record, using total events in NanoAOD...")
      dw = ROOT.RDataFrame("Runs",fns)
      nevt = dw.Sum("genEventSumw")
      nevt = nevt.GetValue()
    xsec_weights = self.lumi*self.s.xsec/(nevt)
    d = self.AddWeights(d,xsec_weights)
    return d,xsec_weights

  def getplotsOld(self,d,weight):
    dhs = dict()
    for varlabel in self.dplots:
      hs = []
      plots = self.dplots[varlabel][0]
      plots_2d = self.dplots[varlabel][1]
      for plt in plots:
        h = d.Histo1D(ps.plots[plt],plt+varlabel,weight)
        hs.append(h)
  
      for x in plots_2d:
        for y in plots_2d[x]:
          xax = ps.plots[x]
          yax = ps.plots[y]
          xtitle_idx0 = xax[1].find(';')
          xtitle_idx1 = xax[1].find(';',xtitle_idx0+1)
          xtitle = xax[1][xtitle_idx0+1:xtitle_idx1]
          ytitle_idx0 = yax[1].find(';')
          ytitle_idx1 = yax[1].find(';',ytitle_idx0+1)
          ytitle = yax[1][ytitle_idx0+1:ytitle_idx1]
          hset = (xax[0]+'_vs_'+yax[0],";{0};{1}".format(xtitle,ytitle),xax[2],xax[3],xax[4],yax[2],yax[3],yax[4])
          h = d.Histo2D(hset,x+varlabel,y_varlabel,weight)
          hs.append(h)
  
      for i in range(len(hs)):
        hs[i] = hs[i].Clone()
        hs[i].SetName(hs[i].GetName())

      dhs[varlabel] = hs
  
    return dhs
  
  def getplots(self,d,weight,plots_1d,plots_2d,varlabel):
    hs = []
    if plots_1d is None:
      plots_1d = []
    if plots_2d is None:
      plots_2d = []

    for plt in plots_1d:
      h = d.Histo1D(ps.plots[plt],plt+varlabel,weight)
      hs.append(h)
  
    for x,y in plots_2d:
        xax = ps.plots[x]
        yax = ps.plots[y]
        xtitle_idx0 = xax[1].find(';')
        xtitle_idx1 = xax[1].find(';',xtitle_idx0+1)
        xtitle = xax[1][xtitle_idx0+1:xtitle_idx1]
        ytitle_idx0 = yax[1].find(';')
        ytitle_idx1 = yax[1].find(';',ytitle_idx0+1)
        ytitle = yax[1][ytitle_idx0+1:ytitle_idx1]
        hset = (xax[0]+'_vs_'+yax[0],";{0};{1}".format(xtitle,ytitle),xax[2],xax[3],xax[4],yax[2],yax[3],yax[4])
        h = d.Histo2D(hset,x+varlabel,y+varlabel,weight)
        hs.append(h)
  
    for i in range(len(hs)):
      hs[i] = hs[i].Clone()
      hs[i].SetName(hs[i].GetName())

    return hs

  def writeplots(self,rootdir,d,weight,plots_1d,plots_2d,varlabel):
    hs = self.getplots(d,weight,plots_1d,plots_2d,varlabel)
    rootdir.cd()
    for h in hs:
      h.Write()

  def makeHistFiles(self):
      if not os.path.exists(self.outputDir):
          os.makedirs(self.outputDir)
      fout = ROOT.TFile("{}/{}_hist.root".format(self.outputDir,self.s.name),"RECREATE")
      d,w = self.getRDF()

      for sr in self.cfg['regions']:
        d_sr = d
        if self.cfg['regions'][sr] is not None:
          d_sr = d_sr.Filter(self.cfg['regions'][sr])
        newd_evt = fout.mkdir("{}_evt".format(sr))
        hs = self.getplots(d_sr,weight="evt_weight",plots_1d=self.cfg['event_variables'],plots_2d=self.cfg['event_2d_plots'],varlabel="")
        newd_evt.cd()
        for h in hs:
          h.Write()
        #self.writeplots(newd_evt,d=d_sr,weight="evt_weight",plots_1d=self.cfg['event_variables'],plots_2d=self.cfg['event_2d_plots'],varlabel="")
        for obj in self.cfg['objects']:
          for sels in self.cfg['objects'][obj]['selections']:
            newd = fout.mkdir("{}_{}_{}".format(sr,obj,sels))
            hs = self.getplots(d=d_sr,weight="evt_weight",plots_1d=self.cfg['objects'][obj]['variables'],plots_2d=self.cfg['objects'][obj]['2d_plots'],varlabel=sels)
            newd.cd()
            for h in hs:
              h.Write()
            #self.writeplots(newd,d=d_sr,weight="evt_weight",plots_1d=self.cfg['objects'][obj]['variables'],plots_2d=self.cfg['objects'][obj]['2d_plots'],varlabel=sels)

      fout.Close()
  
  
def AddHists(hs,ws):
  assert len(hs)==len(ws)
  for i in range(len(hs)):
    hs[i].Scale(ws[i])
    if i>0:
      hs[0].Add(hs[i])
  return hs[0]

def StackHists(hs,ws):
  assert len(hs)==len(ws)
  h = ROOT.THStack("h","")
  for i in range(len(hs)):
    hs[i].Scale(ws[i])
    hs[i].SetLineColor(i+1)
    hs[i].SetFillColor(i+1)
    h.Add(hs[i])
  return h



def comparehists(name,hs,legend,colors,scale):
  c = ROOT.TCanvas("c"+name,"c"+name,600,600)
  l = ROOT.TLegend(0.6,0.7,0.9,0.9)
  y_max = 0
  for i in range(len(hs)):
    if scale:
      hs[i].Scale(1./hs[i].Integral())
    hs[i].SetLineWidth(2)
    hs[i].SetLineColor(colors[i])
    y_max = max(y_max,hs[i].GetMaximum())

  for i in range(len(hs)):
    if i==0:
      hs[i].SetMaximum(1.2*y_max)
      hs[i].DrawClone()
    else:
      hs[i].DrawClone("same")
    l.AddEntry(hs[i],legend[i])

  l.Draw()
  c.Update()
  c.SaveAs("{}.pdf".format(name))

