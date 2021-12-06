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


"""Input data has pre-selection cuts applied"""


def getArgParser():
    parser = ArgumentParser()
    parser.add_argument("--data", default='data/monoSvvzp1700dm200dh160.root')
    return parser


def plot_2d(x, y, bins, ax):
    """Two dimensional plot: fix of ampl plot_2d."""
    X, Y = np.meshgrid(x, y)
    mesh = ax.pcolormesh(X, Y, bins.transpose(), rasterized=True)
    cbar = ax.figure.colorbar(mesh, ax=ax, pad=0.05)
    cbar.set_label('Events', rotation=270, labelpad=20)
    return mesh, cbar


def makePlot(histogram, xlabel, ylabel, desc, title, outname):
    # make canvas
    fig = plt.figure(figsize=(7, 5), dpi=600)
    ax0 = fig.add_subplot()

    # plot histograms
    # mesh, cbar = ampl.plot.plot_2d(*histogram.edges, histogram.values, ax=ax0, pad=0.01)
    luminosity = 139.
    values = histogram.values * luminosity
    mesh, cbar = plot_2d(*histogram.edges, values, ax=ax0)

    # add white line indicating cut value
    x = np.linspace(0, 400, 10)
    y = np.ones_like(x) * (0.3 if ylabel == "$\\tau_{42}$" else 0.6)
    ax0.plot(x, y, 'k--', color='#999999')

    # label axes
    ampl.plot.set_xlabel(xlabel)
    ampl.plot.set_ylabel(ylabel)

    # add text
    drawThesisLabel(0.05, 1.25, ax0, energy='13 TeV', lumi=luminosity, desc=desc)
    ax0.text(0.65, 1.25, title, verticalalignment='top', horizontalalignment='left',
             transform=ax0.transAxes, fontsize=16)
    plt.tight_layout()

    # save plot
    fig.savefig(outname)
    plt.close()


def main():
    args = getArgParser().parse_args()

    with open(args.data) as data:
        # tau42 vs mass
        hist = data['tarjet_leading_lt4matchedquarks_mVStau42']
        xlabel = '$m_{VV}$ [GeV]'
        ylabel = "$\\tau_{42}$"
        desc = '$E_{T}^{miss} + s(VV)$: $m_{Z\'} = 1.7\,$TeV, $m_{s} = 160\,$GeV'
        # desc = '$E_{T}^{miss} + s(VV)$: $m_{Z\'} = 2.1\,$TeV, $m_{s} = 210\,$GeV'
        title = 'less than  4 matched partons'
        outname = 'sVVmerged_truth_lt4matchedquarks_mVStau42.pdf'
        makePlot(hist, xlabel, ylabel, desc, title, outname)

        hist = data['tarjet_leading_4matchedquarks_mVStau42']
        xlabel = '$m_{VV}$ [GeV]'
        ylabel = "$\\tau_{42}$"
        desc = '$E_{T}^{miss} + s(VV)$: $m_{Z\'} = 1.7\,$TeV, $m_{s} = 160\,$GeV'
        # desc = '$E_{T}^{miss} + s(VV)$: $m_{Z\'} = 2.1\,$TeV, $m_{s} = 210\,$GeV'
        title = '4 matched partons'
        outname = 'sVVmerged_truth_4matchedquarks_mVStau42.pdf'
        makePlot(hist, xlabel, ylabel, desc, title, outname)

        hist = data['tarjet_leading_lt4matchedquarks_mVStau43']
        xlabel = '$m_{VV}$ [GeV]'
        ylabel = "$\\tau_{43}$"
        desc = '$E_{T}^{miss} + s(VV)$: $m_{Z\'} = 1.7\,$TeV, $m_{s} = 160\,$GeV'
        # desc = '$E_{T}^{miss} + s(VV)$: $m_{Z\'} = 2.1\,$TeV, $m_{s} = 210\,$GeV'
        title = 'less than 4 matched partons'
        outname = 'sVVmerged_truth_lt4matchedquarks_mVStau43.pdf'
        makePlot(hist, xlabel, ylabel, desc, title, outname)

        hist = data['tarjet_leading_4matchedquarks_mVStau43']
        xlabel = '$m_{VV}$ [GeV]'
        ylabel = "$\\tau_{43}$"
        desc = '$E_{T}^{miss} + s(VV)$: $m_{Z\'} = 1.7\,$TeV, $m_{s} = 160\,$GeV'
        # desc = '$E_{T}^{miss} + s(VV)$: $m_{Z\'} = 2.1\,$TeV, $m_{s} = 210\,$GeV'
        title = '4 matched partons'
        outname = 'sVVmerged_truth_4matchedquarks_mVStau43.pdf'
        makePlot(hist, xlabel, ylabel, desc, title, outname)



if __name__ == '__main__':
    main()
