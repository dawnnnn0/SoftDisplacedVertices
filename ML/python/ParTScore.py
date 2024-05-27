from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import onnxruntime as ort
import numpy as np
import json
import vector
vector.register_awkward()
import os 

class ParTScoreProducer(Module):
    def __init__(self,model_path='',preprocess_json_path=''):
        self.model_path = model_path
        self.preprocess_json_path = preprocess_json_path
        pass

    def deltaPhi(self,dphi):
        #if np.isscalar(dphi):
        o2pi = 1. / (2. * np.pi)
        mask = np.abs(dphi) > np.pi
        n = np.round(dphi*o2pi)
        return dphi - n * mask * (2. * np.pi)

    def ArraytoNumpy(self,array):
        arr_np = []
        for i in array:
          arr_np.append(i)
        arr_np = np.array(arr_np)
        return arr_np

    def beginJob(self):
        self.ort_sess = ort.InferenceSession(self.model_path, providers=['CPUExecutionProvider'])
        self.params = None
        self.excludeinput = ['pf_points']
        with open(self.preprocess_json_path,'r') as fj:
          self.params = json.load(fj)

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("SDVSecVtx_ParTScore", "F", lenVar="nSDVSecVtx")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        SDVSecVtx = Collection(event, "SDVSecVtx")
        SDVTrack = Collection(event, "SDVTrack")
        SDVIdxLUT = Collection(event, "SDVIdxLUT")

        Jet = Collection(event, "Jet")
        jet0_phi = Jet[0].phi
        #MET = Collection(event, "MET")
        met_phi = event.MET_phi

        SVIdx = event.SDVIdxLUT_SecVtxIdx
        SVIdx = self.ArraytoNumpy(SVIdx)
        TkIdx = event.SDVIdxLUT_TrackIdx
        TkIdx = self.ArraytoNumpy(TkIdx)

        d = {
          "tk_pt": self.ArraytoNumpy(event.SDVTrack_pt),
          "tk_eta": self.ArraytoNumpy(event.SDVTrack_eta),
          "tk_phi": self.ArraytoNumpy(event.SDVTrack_phi),
          "tk_nvalidhits": self.ArraytoNumpy(event.SDVTrack_numberOfValidHits),
          "tk_normchi2": self.ArraytoNumpy(event.SDVTrack_normalizedChi2),
          "tk_pterr": self.ArraytoNumpy(event.SDVTrack_ptError),
          "tk_dxy": self.ArraytoNumpy(event.SDVTrack_dxy),
          "tk_dxyerr": self.ArraytoNumpy(event.SDVTrack_dxyError),
          "tk_dz": self.ArraytoNumpy(event.SDVTrack_dz),
          "tk_dzerr": self.ArraytoNumpy(event.SDVTrack_dzError),
        }

        d_vtx_evals = {
            #"vtx_pt": "pt",
            #"vtx_energy": "energy",
            "vtx_L_eta": "L_eta",
            "vtx_L_phi": "L_phi",
            "vtx_lxy": "Lxy",
            "vtx_lxySig": "LxySig",
            "vtx_ndof": "ndof",
            "vtx_acollinearity": "pAngle",
        }

        evals = {
            "vtx_lxy_err": "dv['vtx_lxy']",
            "vtx_dphi_jet1": "self.deltaPhi(dv['vtx_L_phi']-jet0_phi)",
            "vtx_dphi_met": "self.deltaPhi(dv['vtx_L_phi']-met_phi)",
            "vtx_tk_pt_log": "np.log(dv['vtx_tk_pt'])",
            "vtx_tk_E_log": "np.log(dv['vtx_tk_E'])",
            #"vtx_tk_logptrel": "np.log(dv['vtx_tk_pt']/vtx_pt)",
            #"vtx_tk_logerel": "np.log(dv['vtx_tk_E']/vtx_energy)",
            "vtx_tk_pterrratio": "dv['vtx_tk_pterr']/dv['vtx_tk_pt']",
            "vtx_tk_deta_Lvtx": "np.abs(dv['vtx_tk_eta']-SDVSecVtx_L_eta)",
            "vtx_tk_dphi_Lvtx": "self.deltaPhi(dv['vtx_tk_phi']-SDVSecVtx_L_phi)",
            "vtx_tk_deltaR": "np.hypot(dv['vtx_tk_deta_Lvtx'], dv['vtx_tk_dphi_Lvtx'])",
            "vtx_tk_dxy_th": "np.tanh(dv['vtx_tk_dxy'])",
            "vtx_tk_dz_th": "np.tanh(dv['vtx_tk_dz'])",
            "vtx_tk_mask": "np.ones_like(dv['vtx_tk_pt'])",
            }

        # create input data
        d_input = {}
        for input_name in self.params['input_names']:
          if input_name in self.excludeinput:
            continue
          d_input[input_name] = []

        mass = 0.13957018

        for ivtx in range(len(SDVSecVtx)):
            d_input_pervtx = {}
            for input_name in d_input:
              d_input_pervtx[input_name] = []
            vtxtksIdx = TkIdx[SVIdx==ivtx].astype(np.int32)
            SDVSecVtx_L_phi = SDVSecVtx[ivtx].L_phi
            SDVSecVtx_L_eta = SDVSecVtx[ivtx].L_eta
            dv = {}
            for ie in d_vtx_evals:
              dv[ie] = getattr(SDVSecVtx[ivtx],d_vtx_evals[ie])
            for ie in d:
              dv["vtx_"+ie] = np.array(d[ie])[vtxtksIdx]
            dv["vtx_tk_M"] = np.array([mass]*len(dv["vtx_tk_pt"]))
            p4 = vector.array({
              "pt":dv["vtx_tk_pt"],
              "phi":dv["vtx_tk_phi"],
              "eta":dv["vtx_tk_eta"],
              "M":dv["vtx_tk_M"]
              })
            dv["vtx_tk_px"] = p4.px
            dv["vtx_tk_py"] = p4.py
            dv["vtx_tk_pz"] = p4.pz
            dv["vtx_tk_E"] = p4.E
            for ie in evals:
              dv[ie] = eval(evals[ie])

            for input_name in d_input:
              for vn in self.params[input_name]['var_names']:
                varr = dv[vn]
                if np.isscalar(varr):
                  varr = np.array([varr])
                if vn in self.params[input_name]['var_infos']:
                  # Normalise the data
                  median = self.params[input_name]['var_infos'][vn]['median']
                  norm_factor = self.params[input_name]['var_infos'][vn]['norm_factor']
                  varr = (varr-median)*norm_factor

                # Pad the data (zero-padding)
                npfs = self.params[input_name]['var_length']
                pad_value = self.params[input_name]['var_infos'][vn]['pad']
                if npfs-len(varr)>0:
                  varr = np.pad(varr,(0,npfs-len(varr)),'constant',constant_values=pad_value)
                varr = varr[:npfs]

                d_input_pervtx[input_name].append(varr)
              d_input_pervtx[input_name] = np.array(d_input_pervtx[input_name])
              d_input[input_name].append(d_input_pervtx[input_name])

        if (len(SDVSecVtx)>0):
          for input_name in d_input:
            d_input[input_name] = np.array(d_input[input_name]).astype(np.float32)

          # run inference
          outputs = self.ort_sess.run(None, d_input)[0]
          # print input and output
          #print('input ->', data)
        else:
          outputs = np.zeros((0,2))
        #print('output ->', outputs[:,0])

        self.out.fillBranch("SDVSecVtx_ParTScore", outputs[:,0])
        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

ParTScoreModuleConstr = lambda : ParTScoreProducer('/scratch/ang.li/MLinput/ParTLLP_vtx_0227_3.onnx', '/scratch/ang.li/MLinput/preprocess_0227_3.json')
#ParTScoreModuleConstr = lambda : ParTScoreProducer('/scratch/ang.li/MLinput/ParTLLP_0222_1.onnx', '/scratch/ang.li/MLinput/preprocess_0222_1.json')
