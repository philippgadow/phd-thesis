from uproot.rootio import open
from argparse import ArgumentParser
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import atlas_mpl_style as ampl

from ATLASlabel import drawThesisLabel

# use ATLAS style
ampl.use_atlas_style()
ampl.set_color_cycle(pal='Paper', n=4)


def getArgParser():
    parser = ArgumentParser()
    parser.add_argument("--data", default='data/data.root')
    parser.add_argument("--mc", default='data/mc.root')
    parser.add_argument("--region", default='SR_Resolved_150_200_2b')
    return parser


def makeMassPlot(data, mc, region='SR_Resolved_150_200_2b'):
    # get histogram
    h_data_DPhifailMSfail = data['MonoH_Nominal']['{region}_DPhifailMSfail'.format(region=region)]['m_jj']
    h_data_DPhifailMSpass = data['MonoH_Nominal']['{region}_DPhifailMSpass'.format(region=region)]['m_jj']
    h_data_DPhipassMSfail = data['MonoH_Nominal']['{region}_DPhipassMSfail'.format(region=region)]['m_jj']
    h_data_DPhipassMSpass = data['MonoH_Nominal']['{region}_DPhipassMSpass'.format(region=region)]['m_jj']

    h_mc_DPhifailMSfail = mc['MonoH_Nominal']['{region}_DPhifailMSfail'.format(region=region)]['m_jj']
    h_mc_DPhifailMSpass = mc['MonoH_Nominal']['{region}_DPhifailMSpass'.format(region=region)]['m_jj']
    h_mc_DPhipassMSfail = mc['MonoH_Nominal']['{region}_DPhipassMSfail'.format(region=region)]['m_jj']
    h_mc_DPhipassMSpass = mc['MonoH_Nominal']['{region}_DPhipassMSpass'.format(region=region)]['m_jj']


    luminosity = 79.8
    edges = h_data_DPhifailMSfail.edges

    multijet_DPhifailMSfail = h_data_DPhifailMSfail.values - h_mc_DPhifailMSfail.values * luminosity
    int_DPhifailMSfail = np.sum(multijet_DPhifailMSfail)
    multijet_DPhifailMSfail /= int_DPhifailMSfail
    e_multijet_DPhifailMSfail = np.sqrt(h_data_DPhifailMSfail.variances + h_mc_DPhifailMSfail.variances * luminosity**2)
    e_multijet_DPhifailMSfail /= int_DPhifailMSfail

    multijet_DPhifailMSpass = h_data_DPhifailMSpass.values - h_mc_DPhifailMSpass.values * luminosity
    int_DPhifailMSpass = np.sum(multijet_DPhifailMSpass)
    multijet_DPhifailMSpass /= int_DPhifailMSpass
    e_multijet_DPhifailMSpass = np.sqrt(h_data_DPhifailMSpass.variances + h_mc_DPhifailMSpass.variances * luminosity**2)
    e_multijet_DPhifailMSpass /= int_DPhifailMSpass

    multijet_DPhipassMSfail = h_data_DPhipassMSfail.values - h_mc_DPhipassMSfail.values * luminosity
    int_DPhipassMSfail = np.sum(multijet_DPhipassMSfail)
    multijet_DPhipassMSfail /= int_DPhipassMSfail
    e_multijet_DPhipassMSfail = np.sqrt(h_data_DPhipassMSfail.variances + h_mc_DPhipassMSfail.variances * luminosity**2)
    e_multijet_DPhipassMSfail /= int_DPhipassMSfail

    multijet_DPhipassMSpass = h_data_DPhipassMSpass.values - h_mc_DPhipassMSpass.values * luminosity
    int_DPhipassMSpass = np.sum(multijet_DPhipassMSpass)
    multijet_DPhipassMSpass /= int_DPhipassMSpass
    e_multijet_DPhipassMSpass = np.sqrt(h_data_DPhipassMSpass.variances + h_mc_DPhipassMSpass.variances * luminosity**2)
    e_multijet_DPhipassMSpass /= int_DPhipassMSpass


    # make canvas
    fig = plt.figure(figsize=(6, 4), dpi=600)
    ax0 = fig.add_subplot()


    # plot histograms
    ampl.plot.plot_1d("region A (multijet)", edges, multijet_DPhifailMSfail, stat_errs=e_multijet_DPhifailMSfail, ax=ax0, color='blue')
    # ampl.plot.plot_1d("region B", edges, multijet_DPhifailMSpass, stat_errs=e_multijet_DPhifailMSpass, ax=ax0, color='red')
    # ampl.plot.plot_1d("region C", edges, multijet_DPhipassMSfail, stat_errs=e_multijet_DPhipassMSfail, ax=ax0, color='orange')
    ampl.plot.plot_1d("region D (SR)", edges, multijet_DPhipassMSpass, stat_errs=e_multijet_DPhifailMSpass, ax=ax0, color='green')

    # label axes
    ampl.plot.set_xlabel('$m_{jj}$ [GeV]')
    ampl.plot.set_ylabel("Fraction of events")

    # set axis range
    ax0.set_xlim((50, 280))
    if region == 'SR_Resolved_350_500_2b':
        drawThesisLabel(0.5, 0.9, ax0, energy='13 TeV', lumi=79.8)
    else:
        drawThesisLabel(0.5, 0.7, ax0, energy='13 TeV', lumi=79.8)
    plt.legend(frameon=False)
    plt.tight_layout()

    # save plot
    fig.savefig('monoHmultijet_correlation-mass_{region}.pdf'.format(region=region))


def main():
    args = getArgParser().parse_args()

    data = open(args.data)
    mc = open(args.mc)
    makeMassPlot(data, mc, args.region)


if __name__ == '__main__':
    main()
