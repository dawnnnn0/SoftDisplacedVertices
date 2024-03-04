plots = {
    'nSDVSecVtx_CCsel':('nSDVSecVtx_CCsel',";Number of vertices (CC);A.U.",20,0,20),
    'nSDVSecVtx_MLsel':('nSDVSecVtx_MLsel',";Number of vertices (ML);A.U.",20,0,20),
    'SDVSecVtx_ParTScore':('SDVSecVtx_ParTScore',";ParTScore;A.U.",50,0,1),
    'SDVSecVtx_LxySig_CCsel_max':('SDVSecVtx_LxySig_CCsel_max',";max vertex (CC) L_{xy}/#sigma_{L_{xy}};A.U.",100,0,100),
    'SDVSecVtx_LxySig_MLsel_max':('SDVSecVtx_LxySig_MLsel_max',";max vertex (ML) L_{xy}/#sigma_{L_{xy}};A.U.",100,0,100),
    'SDVSecVtx_Lxy':('SDVSecVtx_Lxy',";vertex L_{xy} (cm);A.U.",100,0,10),
    'SDVSecVtx_Lxy_err':('SDVSecVtx_Lxy_err',";vertex #sigmaL_{xy} (cm);A.U.",100,0,0.5),
    'SDVSecVtx_LxySig':('SDVSecVtx_LxySig',";vertex L_{xy}/#sigmaL_{xy};A.U.",500,0,100),
    'SDVSecVtx_dphi_L_MET':('SDVSecVtx_dphi_L_MET',";#Delta#phi(Lxy,MET)",64,0,3.2),
    'SDVSecVtx_dphi_L_jet0':('SDVSecVtx_dphi_L_jet0',";#Delta#phi(Lxy,jet0)",64,0,3.2),
    'SDVSecVtx_pAngle':('SDVSecVtx_pAngle',";vertex pAngle;A.U.",64,0,3.2),
    'SDVSecVtx_dlen':('SDVSecVtx_dlen',";vertex dlen (cm);A.U.",100,0,10),
    'SDVSecVtx_dlen_err':('SDVSecVtx_dlen_err',";vertex #sigmadlen (cm);A.U.",100,0,0.5),
    'SDVSecVtx_dlenSig':('SDVSecVtx_dlenSig',";vertex dlen/#sigmadlen;A.U.",500,0,100),
    'SDVSecVtx_nTracks':('SDVSecVtx_nTracks',";vertex nTracks;A.U.",20,0,20),
    'SDVSecVtx_nGoodTrack':('SDVSecVtx_nGoodTrack',";vertex ngoodTrack;A.U.",20,0,20),
    #'SDVSecVtx_nMatchedTk':('SDVSecVtx_nMatchedTk',";vertex nTrack matched with LLP;A.U.",20,0,20),
    'SDVSecVtx_chi2':('SDVSecVtx_chi2',";vertex chi2;A.U.",50,0,10),
    'SDVSecVtx_normalizedChi2':('SDVSecVtx_normalizedChi2',";vertex norm chi2;A.U.",50,0,10),
    'SDVSecVtx_ndof':('SDVSecVtx_ndof',";vertex ndof;A.U.",20,0,20),
    'SDVSecVtx_L_eta_abs':('SDVSecVtx_L_eta_abs',";vertex |#eta|;A.U.",200,0,10),
    'SDVSecVtx_matchedLLPIdx_bydau':('SDVSecVtx_matchedLLPIdx_bydau',";vertex matched LLP idx;A.U.",5,-1,4),
    'SDVSecVtx_matchedLLPnDau_bydau':('SDVSecVtx_matchedLLPnDau_bydau',";vertex number of tracks matched with LLP;A.U.",10,0,10),
    'SDVSecVtx_TkMaxdphi':('SDVSecVtx_TkMaxdphi',";vertex track max(d#phi);A.U.",64,0,3.2),
    'SDVSecVtx_TkMindphi':('SDVSecVtx_TkMindphi',";vertex track min(d#phi);A.U.",64,0,3.2),
    'SDVSecVtx_TkMaxdeta':('SDVSecVtx_TkMaxdeta',";vertex track max(d#eta);A.U.",100,0,5),
    'SDVSecVtx_TkMindeta':('SDVSecVtx_TkMindeta',";vertex track min(d#eta);A.U.",100,0,5),
    'SDVSecVtx_TkMaxdR':('SDVSecVtx_TkMaxdR',";vertex track max(dR);A.U.",100,0,5),
    'SDVSecVtx_TkMindR':('SDVSecVtx_TkMindR',";vertex track min(dR);A.U.",100,0,5),
    'MET_pt':('MET_pt',";MET (GeV);A.U.",100,0,1000),

    }

plots_2d = {
    #'SDVSecVtx_dlen':['SDVSecVtx_Lxy','SDVSecVtx_Lxy_err','SDVSecVtx_LxySig','SDVSecVtx_pAngle','SDVSecVtx_dlen_err','SDVSecVtx_dlenSig','SDVSecVtx_nTracks','SDVSecVtx_ngoodTrack','SDVSecVtx_chi2','SDVSecVtx_normalizedChi2','SDVSecVtx_ndof','SDVSecVtx_L_eta_abs'],
    #'SDVSecVtx_Lxy':['SDVSecVtx_L_eta_abs','SDVSecVtx_dlen']
    }
