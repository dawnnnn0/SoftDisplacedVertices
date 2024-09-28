for s in 'All' 'VR1s' 'VR2s' 'lessPV' #'SRs'  #'lowTrack' 'highMET' #'VR' 'VR_CRlowMET' 'VR_CRlowLxy' 'VR_CRlowLxylowMET' 'SR_CRlowMET' 'SR_CRlowLxy' 'SR_CRlowLxylowMET'
do
  for o in '_evt' '_SDVSecVtx_all' '_SDVSecVtx_sel_val1' '_SDVSecVtx_sel_val2' '_SDVSecVtx_sel' '_SDVTrack_all' '_SDVTrack_GoodTrack' #'_SDVTrack_allInSV' '_SDVTrack_GoodTrackdxydzInSV' '_SDVTrack_phisel' '_SDVTrack_loweta' '_SDVTrack_higheta'
  do
    #python3 compare.py --input /eos/vbc/group/cms/ang.li/DataHistos_VRCR2/met2018_hist.root /eos/vbc/group/cms/ang.li/MCHistos_VRCR2/background_2018_hist.root --dirs "$s$o" --nice "Data" "Simulation" --output /groups/hephy/cms/ang.li/SDV/DataMCComp2_$s$o --commands "h.Rebin(5) if ('LxySig' in h.GetName()) else None" --datamc --ratio
    python3 compare_data_new.py --data /eos/vbc/group/cms/ang.li/DataHistos_VRCR${1}/met2018_hist.root --bkg /eos/vbc/group/cms/ang.li/MCHistos_VRCR${1}/qcd_2018_hist.root /eos/vbc/group/cms/ang.li/MCHistos_VRCR${1}/wjets_2018_hist.root /eos/vbc/group/cms/ang.li/MCHistos_VRCR${1}/zjets_2018_hist.root --bkgnice "QCD" "WJets" "ZJets" --signal /eos/vbc/group/cms/ang.li/MCHistos_VRCR${1}/stop_M600_585_ct20_2018_hist.root --signice "signal" --output /groups/hephy/cms/ang.li/SDV/DataMCComp${1}_$s$o --dirs "$s$o" --commands "h.Rebin(5) if ('LxySig' in h.GetName()) else h.GetXaxis().SetRangeUser(0,20) if ('pfRel' in  h.GetName()) else None" --ratio 
  done
done

for s in 'All' 'SRs' 'VR1s' 'VR2s' 'lessPV' #'SRs'  #'lowTrack' 'highMET' #'VR' 'VR_CRlowMET' 'VR_CRlowLxy' 'VR_CRlowLxylowMET' 'SR_CRlowMET' 'SR_CRlowLxy' 'SR_CRlowLxylowMET'
do
  for o in '_evt' '_SDVSecVtx_all' '_SDVSecVtx_sel_val1' '_SDVSecVtx_sel_val2' '_SDVSecVtx_sel' '_SDVTrack_all' '_SDVTrack_GoodTrack' #'_SDVTrack_allInSV' '_SDVTrack_GoodTrackdxydzInSV' '_SDVTrack_phisel' '_SDVTrack_loweta' '_SDVTrack_higheta'
  do
    python3 compare_data_new.py  --bkg /eos/vbc/group/cms/ang.li/MCHistos_VRCR${1}/qcd_2018_hist.root /eos/vbc/group/cms/ang.li/MCHistos_VRCR${1}/wjets_2018_hist.root /eos/vbc/group/cms/ang.li/MCHistos_VRCR${1}/zjets_2018_hist.root  --bkgnice "QCD" "WJets" "ZJets" --signal /eos/vbc/group/cms/ang.li/MCHistos_VRCR${1}_sig/stop_M600_585_ct20_2018_hist.root --signice "signal" --output /groups/hephy/cms/ang.li/SDV/SigBkgComp${1}_$s$o --dirs "$s$o" --commands "h.Rebin(5) if ('LxySig' in h.GetName()) else h.GetXaxis().SetRangeUser(0,20) if ('pfRel' in  h.GetName()) else None" --norm
  done
done

