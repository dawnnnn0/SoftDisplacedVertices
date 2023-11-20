import click_try

my_cuts = ['my_cut1', 'my_cut2']
histograms = click_try.calc_histograms(my_cuts)
click_try.plot_histograms(histograms)