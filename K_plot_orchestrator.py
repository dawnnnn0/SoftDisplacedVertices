import ROOT

import K_plotter as K
import varcutlib

# plot_args = K.DotDict()
# plot_args.var = 'GenMET_pt'
# plot_args.title = 'Simulated Event Distributions After Cuts'
# plot_args.nb = 20
# plot_args.xlow = 0
# plot_args.xup = 2000
# plot_args.savename = f'{plot_args.var}_w_cuts.png'
# print(f'Plotting: {plot_args.var}')

# ev = 'MET'
# sv = 'DPHIRM,RALPHA,LXYSIG,NGTR'
# tr = 'DXYSIG,DZ,NVH,RSPT'
# cuts = varcutlib.get_cuts(ev, sv, tr)

# df = K.data_load_step()
# df_ev, df_sv = K.filtering_step(df, cuts)
# hh_ev, hh_sv, hh_cut_efficacy = K.histogram_step(df_ev, df_sv, plot_args, debug=True)
# K.plotting_step(hh_ev, hh_sv, hh_cut_efficacy, plot_args)


# plot_args = K.DotDict()
# plot_args.var = 'PuppiMET_pt'
# plot_args.title = 'Simulated Event Distributions After Cuts'
# plot_args.nb = 20
# plot_args.xlow = 0
# plot_args.xup = 2000
# plot_args.savename = f'{plot_args.var}_w_cuts.png'
# print(f'Plotting: {plot_args.var}')

# ev = 'RawMET'
# sv = 'DPHIRM,RALPHA,LXYSIG,NGTR'
# tr = 'DXYSIG,DZ,NVH,RSPT'
# cuts = varcutlib.get_cuts(ev, sv, tr)

# df = K.data_load_step()
# df_ev, df_sv = K.filtering_step(df, cuts)
# hh_ev, hh_sv, hh_cut_efficacy = K.histogram_step(df_ev, df_sv, plot_args, debug=True)
# K.plotting_step(hh_ev, hh_sv, hh_cut_efficacy, plot_args)


plot_args = K.DotDict()
plot_args.var = 'SDVSecVtx_Lxy'
plot_args.title = 'Simulated Event Distributions After Cuts'
plot_args.nb = 40
plot_args.xlow = 0
plot_args.xup = 120
plot_args.savename = f'{plot_args.var}_w_cuts.png'
print(f'Plotting: {plot_args.var}')

ev = 'RawMET'
sv = 'DPHIRM,RALPHA,LXYSIG,NGTR'
tr = 'DXYSIG,DZ,NVH,RSPT'
cuts = varcutlib.get_cuts(ev, sv, tr)

df = K.data_load_step()
df_ev, df_sv = K.masking_step(df, plot_args.var, cuts)
hh_ev, hh_sv, hh_cut_efficacy = K.histogram_step(df_ev, df_sv, plot_args, is_masked=True, debug=True)
K.plotting_step(hh_ev, hh_sv, hh_cut_efficacy, plot_args)













