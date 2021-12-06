#!/bin/env python
from __future__ import unicode_literals

import os
from argparse import ArgumentParser

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

import numpy as np
import pandas as pd
import seaborn as sns
import atlas_mpl_style as ampl
from ATLASlabel import drawThesisLabel




def getArgs():
    """Get arguments from command line."""
    parser = ArgumentParser()
    parser.add_argument('inputFile', help='CSV file containing significances')
    parser.add_argument('-o', '--outputName', default='monoHbb-zhdm-significances', help='Name of output file (+.png, .pdf, .eps)')
    parser.add_argument('-e', '--expected', action='store_true', help='Show expected limit instead of observed.')
    return parser.parse_args()


def getInput(inputFile):
    """Get pandas dataframe with limits from input file."""
    df = pd.read_csv(inputFile)
    print(df)
    return df


def plotLimit(inputFile, args):  # exp, exp_1m, exp_1p, exp_2m, exp_2p):
    """Create pretty limit plot with matplotlib."""
    fig, axes = plt.subplots(figsize=(15,5))

    # get input for limit plots
    data = getInput(inputFile)

    # plot limit as heatmap
    limit = data.pivot(index='mA', columns='mzp', values='exp' if args.expected else 'obs')

    # first observed, then check expected
    limit_annot = limit.to_numpy(copy=True)
    limit_annot = [["{b:2.2f}".format(b=b) if not np.isnan(b) else '' for b in a] for a in limit_annot]
    heatmap = sns.heatmap(limit, cmap="coolwarm", center=1., annot=limit_annot, fmt='', annot_kws={"size": 16}, cbar_kws={'label': '{v} discovery significance'.format(v='Expected' if args.expected else 'Oberved')}, vmin=0.00, vmax=5)

    left_position = 0.0

    # label plot
    axes.set_xlabel(r"$m_{Z'}$ [GeV]",
                    horizontalalignment="right", x=1, labelpad=14, fontsize=20)
    axes.set_ylabel(r"$m_{A}$ [GeV]",
                    horizontalalignment="right", y=1, labelpad=14, fontsize=20)
    # add text
    model1Text = "$E_{T}^{miss}$ + $h$($b\overline{b}$): Z'-2HDM"
    model2Text = "$\\tan \\beta = 1$, $g_{Z'}$ = 0.8, $m_{\\chi}$ = 100\,GeV, $m_{H} = m_{H^{\pm}}$ = 300\,GeV"

    drawThesisLabel(left_position, 1.12, axes, energy='13 TeV', lumi=79.8)

    axes.text(left_position+0.75, 1.12, model1Text,
              verticalalignment='center', horizontalalignment='left',
              transform=axes.transAxes, fontsize=16)
    axes.text(left_position+0.41, 1.05, model2Text,
              verticalalignment='center', horizontalalignment='left',
              transform=axes.transAxes, fontsize=16)


    # invert y axis
    axes.invert_yaxis()

    return fig, axes



def main():
    """Create limit plot for the mono-h(bb) analysis with ATLAS style."""

    # use ATLAS style
    ampl.use_atlas_style()

    # get input
    args = getArgs()

    # plot limit
    fig, ax = plotLimit(args.inputFile, args)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())

    # conform to the ugly ROOT standard of having axis ticks inside of plot
    ax.get_yaxis().set_tick_params(which='both', direction='in', left=True, right=True)
    ax.get_xaxis().set_tick_params(which='both', direction='in', top=True, bottom=True)

    # save plots
    outputName = args.outputName + ('_expected' if args.expected else '_observed')
    fig.savefig('{out}.pdf'.format(out=outputName), transparent=False, dpi=300, bbox_inches="tight")


if __name__ == '__main__':
    main()

