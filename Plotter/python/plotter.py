import os
import yaml
import ROOT
import correctionlib
correctionlib.register_pyroot_binding()
import SoftDisplacedVertices.Samples.Samples as s
ROOT.gInterpreter.Declare('#include "{}/src/SoftDisplacedVertices/Plotter/RDFHelper.h"'.format(os.environ['CMSSW_BASE']))
ROOT.gInterpreter.Declare('#include "{}/src/SoftDisplacedVertices/Plotter/METxyCorrection.h"'.format(os.environ['CMSSW_BASE']))
ROOT.EnableImplicitMT(16)
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.TH1.SetDefaultSumw2(True)
ROOT.gStyle.SetOptStat(0)

class Plotter:
  def __init__(self,s=None,datalabel="",outputDir="./",lumi=1,info_path="",input_json="",config="",year="",isData=False):
    self.s = None
    self.datalabel = datalabel
    self.outputDir = outputDir
    self.lumi = lumi
    self.info_path = info_path
    self.input_json = input_json
    self.year = year
    self.isData = isData
    with open(config, "r") as f_cfg:
      cfg = yaml.load(f_cfg, Loader=yaml.FullLoader)
    self.cfg = cfg
    if not self.isData:
      self.setCorrections()

  def setCorrections(self):
    if self.cfg['corrections'] is not None:
      if self.cfg['corrections']['PU'] is not None:
        ROOT.gInterpreter.Declare('auto puf = correction::CorrectionSet::from_file("{}");'.format(self.cfg['corrections']['PU']['path']))
        ROOT.gInterpreter.Declare('auto pu = puf->at("{}");'.format(self.cfg['corrections']['PU']['name']))

  def applyCorrections(self,d):
    self.weightstr = ''
    if self.isData:
      d = d.Define("puweight","1")
    else:
      if self.cfg['corrections'] is not None:
        if self.cfg['corrections']['PU'] is not None:
          d = d.Define("puweight",('pu->evaluate({{Pileup_nTrueInt,"{0}"}})'.format(self.cfg['corrections']['PU']['mode'])))
          self.weightstr += ' * puweight'
    return d

    self.f1 = ROOT.TFile.Open("/eos/user/w/wuzh/dv/CMSSW_13_3_0/src/SoftDisplacedVertices/Plotter/Material_Map_HIST.root")
    ROOT.gInterpreter.ProcessLine("auto h_mm = material_map; h_mm->SetDirectory(0);")
    self.f1.Close()

  def setLumi(self,lumi):
    self.lumi = lumi

  def setSample(self,s):
    self.s = s

  def valid(self):
    if self.s is None:
      return False
    return True

  def setSampleInfo(self,info_path):
    self.info_path = info_path

  def setJson(self,input_json):
    self.input_json = input_json

  def getSumWeight(self):
    nevt = self.s.getNEvents(self.datalabel)
    if nevt != -1:
      return nevt
    with open(self.info_path,'r') as f_sample_info:
      sample_info = yaml.safe_load(f_sample_info)
    for i in sample_info:
      if not self.s.name in i:
        continue
      return sample_info[i]['totalsumWeights']
    print("No sum weight record found for {}!".format(self.s.name))
    return -1
  
  def AddVars(self,d):
      d = d.Define("SDVSecVtx_dphi_L_MET","acos(cos(SDVSecVtx_L_phi-MET_phi))")
      d = d.Define("SDVSecVtx_dphi_L_jet0","acos(cos(SDVSecVtx_L_phi-Jet_phi[0]))")
  
      d = d.Define("SDVSecVtx_Lxy_err","SDVSecVtx_Lxy/SDVSecVtx_LxySig")
      d = d.Define("SDVSecVtx_dlen_err","SDVSecVtx_dlen/SDVSecVtx_dlenSig")
      d = d.Define("SDVSecVtx_L_eta_abs","abs(SDVSecVtx_L_eta)")
  
      d = d.Define("SDVSecVtx_TkMaxdphi","SDV_TkMaxdphi(SDVIdxLUT_TrackIdx, SDVIdxLUT_SecVtxIdx, nSDVSecVtx, SDVTrack_phi)")
      d = d.Define("SDVSecVtx_TkMindphi","SDV_TkMindphi(SDVIdxLUT_TrackIdx, SDVIdxLUT_SecVtxIdx, nSDVSecVtx, SDVTrack_phi)")
      d = d.Define("SDVSecVtx_TkMaxdeta","SDV_TkMaxdphi(SDVIdxLUT_TrackIdx, SDVIdxLUT_SecVtxIdx, nSDVSecVtx, SDVTrack_eta)")
      d = d.Define("SDVSecVtx_TkMindeta","SDV_TkMindphi(SDVIdxLUT_TrackIdx, SDVIdxLUT_SecVtxIdx, nSDVSecVtx, SDVTrack_eta)")
      d = d.Define("SDVSecVtx_TkMaxdR","SDV_TkMaxdR(SDVIdxLUT_TrackIdx, SDVIdxLUT_SecVtxIdx, nSDVSecVtx, SDVTrack_eta, SDVTrack_phi)")
      d = d.Define("SDVSecVtx_TkMindR","SDV_TkMindR(SDVIdxLUT_TrackIdx, SDVIdxLUT_SecVtxIdx, nSDVSecVtx, SDVTrack_eta, SDVTrack_phi)")
      d = d.Define("SDVSecVtx_mmoverlap","return ROOT::VecOps::Map(SDVSecVtx_x,SDVSecVtx_y, [](float x, float y){return h_mm->GetBinContent(h_mm->FindBin(x,y)) > 0.01;})")
      
      # MET xy corrections
      d = d.Define("MET_corr",'SDV::METXYCorr_Met_MetPhi(MET_pt,MET_phi,run,"{}",{},PV_npvs)'.format(self.year,"false" if self.isData else "true"))
      d = d.Define("MET_pt_corr",'MET_corr.first')
      d = d.Define("MET_phi_corr",'MET_corr.second')
      if self.cfg['new_variables'] is not None:
        for newvar in self.cfg['new_variables']:
          if isinstance(self.cfg['new_variables'][newvar],list):
            formatstr = [self.cfg[self.cfg['new_variables'][newvar][i]] for i in range(1,len(self.cfg['new_variables'][newvar]))]
            var_define = self.cfg['new_variables'][newvar][0].format(*formatstr)
          elif isinstance(self.cfg['new_variables'][newvar],str):
            var_define = self.cfg['new_variables'][newvar]
          d = d.Define(newvar,var_define)
      print("Defining new variables finished") 
      # HEM veto for 2018 data
      if self.year=="2018" and self.isData:
        d = d.Define("nJetHEM", self.cfg['nJetHEM'])
      else:
        d = d.Define("nJetHEM", "0")
      return d
  
  def AddVarsWithSelection(self,d):
    if not self.cfg['objects']:
      return d
    for obj in self.cfg['objects']:
      selections = self.cfg['objects'][obj]['selections']
      variables  = self.cfg['objects'][obj]['variables']
      for sel in selections:
        for v in variables:
          if selections[sel]:
            d = d.Define(v+sel,"{0}[{1}]".format(v,selections[sel]))
          else:
            d = d.Define(v+sel,"{0}".format(v))
        if ('nm1' in self.cfg['objects'][obj]) and (self.cfg['objects'][obj]['nm1']):
          nm1s = self.cfg['objects'][obj]['nm1']
          cutstr_objsel = ""
          if selections[sel]:
            cutstr_objsel = "({}) && ".format(selections[sel])
          for i in range(len(nm1s)):
            cutstrs = []
            for j in range(len(nm1s)):
              if j==i:
                continue
              cutstrs.append("({})".format(''.join(nm1s[j])))
            cutstr = "&&".join(cutstrs)
            cutstr = cutstr_objsel + "({})".format(cutstr)
            d = d.Define(nm1s[i][0]+sel+'_nm1',"{0}[{1}]".format(nm1s[i][0],cutstr))
            #print("define {}: {}".format(nm1s[i][0]+sel+'_nm1',"{0}[{1}]".format(nm1s[i][0],cutstr)))

    return d
  
  def FilterEvents(self,d):
    d_filter = d.Filter(self.presel)
    return d_filter

  def AddWeights(self,d,weight):
    if self.isData:
      d = self.applyCorrections(d)
      d = d.Define("evt_weight","{0}".format(weight))
    else:
      d = self.applyCorrections(d)
      d = d.Define("evt_weight0","Generator_weight*{0}{1}".format(weight,self.weightstr))
      d = d.Define("met_weight","returnRS(MET_pt)")
      d = d.Define("evt_weight","evt_weight0*met_weight")
    return d
  
  def getRDF(self):
    '''
    This function gets RDataFrame for a given sample
    - Add desired variables
    - Filter events
    - Produce normalisation weights based on xsec
    '''
    fns = self.s.getFileList(self.datalabel,"")
    print("Load file {}".format(fns))
    d = ROOT.RDataFrame("Events",fns)
    #d = d(1000)
    d = self.AddVars(d)
    d = self.AddVarsWithSelection(d)
    if self.cfg['presel'] is not None:
      d = d.Filter(self.cfg['presel'])
    if self.lumi==-1:
      xsec_weights = 1
    else:
      nevt = self.getSumWeight()
      if nevt==-1:
        print("No sum weight record, using total events in NanoAOD...")
        dw = ROOT.RDataFrame("Runs",fns)
        nevt = dw.Sum("genEventSumw")
        nevt = nevt.GetValue()
        print("Total events in NanoAOD {}".format(nevt))
      xsec_weights = self.lumi*self.s.xsec/(nevt)
      print("Total gen events {}, xsec {}, weight {}".format(nevt,self.s.xsec,xsec_weights))
    d = self.AddWeights(d,xsec_weights)
    #d = d.Range(1000)
    #print("RDF finished initializing with range 1000")
    return d,xsec_weights

  def getplotsOld(self,d,weight):
    dhs = dict()
    for varlabel in self.dplots:
      hs = []
      plots = self.dplots[varlabel][0]
      plots_2d = self.dplots[varlabel][1]
      for plt in plots:
        if self.isData:
          h = d.Histo1D(tuple(self.cfg['plot_setting'][plt]),plt+varlabel)
        else:
          h = d.Histo1D(tuple(self.cfg['plot_setting'][plt]),plt+varlabel,weight)
        hs.append(h)
  
      for x in plots_2d:
        for y in plots_2d[x]:
          xax = tuple(self.cfg['plot_setting'][x])
          yax = tuple(self.cfg['plot_setting'][y])
          xtitle_idx0 = xax[1].find(';')
          xtitle_idx1 = xax[1].find(';',xtitle_idx0+1)
          xtitle = xax[1][xtitle_idx0+1:xtitle_idx1]
          ytitle_idx0 = yax[1].find(';')
          ytitle_idx1 = yax[1].find(';',ytitle_idx0+1)
          ytitle = yax[1][ytitle_idx0+1:ytitle_idx1]
          hset = (xax[0]+'_vs_'+yax[0],";{0};{1}".format(xtitle,ytitle),xax[2],xax[3],xax[4],yax[2],yax[3],yax[4])
          if self.isData:
            h = d.Histo2D(hset,x+varlabel,y_varlabel)
          else:
            h = d.Histo2D(hset,x+varlabel,y_varlabel,weight)
          hs.append(h)
  
      for i in range(len(hs)):
        hs[i] = hs[i].Clone()
        hs[i].SetName(hs[i].GetName())

      dhs[varlabel] = hs
  
    return dhs
  
  def getplots(self,d,weight,plots_1d,plots_2d,plots_nm1,varlabel):
    hs = []
    if plots_1d is None:
      plots_1d = []
    if plots_2d is None:
      plots_2d = []
    if plots_nm1 is None:
      plots_nm1 = []

    for plt in plots_1d:
      if self.isData:
        h = d.Histo1D(tuple(self.cfg['plot_setting'][plt]),plt+varlabel)
      else:
        h = d.Histo1D(tuple(self.cfg['plot_setting'][plt]),plt+varlabel,weight)
      hs.append(h)

    for plt in plots_nm1:
      nm1_setting = (self.cfg['plot_setting'][plt[0]]).copy()
      nm1_setting[0] += 'nm1'
      nm1_setting = tuple(nm1_setting)
      if self.isData:
        h = d.Histo1D(nm1_setting,plt[0]+varlabel+'_nm1')
      else:
        h = d.Histo1D(nm1_setting,plt[0]+varlabel+'_nm1',weight)
      hs.append(h)
  
    for x,y in plots_2d:
        xax = tuple(self.cfg['plot_setting'][x])
        yax = tuple(self.cfg['plot_setting'][y])
        xtitle_idx0 = xax[1].find(';')
        xtitle_idx1 = xax[1].find(';',xtitle_idx0+1)
        xtitle = xax[1][xtitle_idx0+1:xtitle_idx1]
        ytitle_idx0 = yax[1].find(';')
        ytitle_idx1 = yax[1].find(';',ytitle_idx0+1)
        ytitle = yax[1][ytitle_idx0+1:ytitle_idx1]
        hset = (xax[0]+'_vs_'+yax[0],";{0};{1}".format(xtitle,ytitle),xax[2],xax[3],xax[4],yax[2],yax[3],yax[4])
        x2d = x+varlabel
        if x not in plots_1d:
          print("Warning! Variable {} not registered in this level!".format(x))
          x2d = x
        y2d = y+varlabel
        if y not in plots_1d:
          print("Warning! Variable {} not registered in this level!".format(y))
          y2d = y
        #h = d.Histo2D(hset,x+varlabel,y+varlabel,weight)
        if self.isData:
          h = d.Histo2D(hset,x2d,y2d)
        else:
          h = d.Histo2D(hset,x2d,y2d,weight)
        hs.append(h)
  
    for i in range(len(hs)):
      print(hs[i].GetName(),"passes")
      hs[i] = hs[i].Clone()
      hs[i].SetName(hs[i].GetName())
      #print(hs[i].GetName(),"passes")
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
        hs = self.getplots(d_sr,weight="evt_weight",plots_1d=self.cfg['event_variables'],plots_2d=self.cfg['event_2d_plots'],plots_nm1=self.cfg.get('event_nm1'),varlabel="")
        newd_evt.cd()
        for h in hs:
          h.Write()
        #self.writeplots(newd_evt,d=d_sr,weight="evt_weight",plots_1d=self.cfg['event_variables'],plots_2d=self.cfg['event_2d_plots'],varlabel="")
        if self.cfg['objects']:
          for obj in self.cfg['objects']:
            for sels in self.cfg['objects'][obj]['selections']:
              newd = fout.mkdir("{}_{}_{}".format(sr,obj,sels))
              hs = self.getplots(d=d_sr,weight="evt_weight",plots_1d=self.cfg['objects'][obj]['variables'],plots_2d=self.cfg['objects'][obj]['2d_plots'],plots_nm1=self.cfg['objects'][obj].get('nm1'),varlabel=sels)
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

