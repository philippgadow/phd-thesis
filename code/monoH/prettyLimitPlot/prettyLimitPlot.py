#!/bin/env python
from __future__ import unicode_literals

import os
import numpy as np
from argparse import ArgumentParser

from rootpy.io import root_open, DoesNotExist
from rootpy.plotting.style import set_style

import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from ATLASlabel import drawATLASLabel


def getArgs():
    """Get arguments from command line."""
    parser = ArgumentParser()
    parser.add_argument('inputFile', help='ROOT file containing limits as TGraphs')
    parser.add_argument('-o', '--outputName', default='monoHbb-95CLsLimitPlot', help='Name of output file (+.png, .pdf, .eps)')
    parser.add_argument('-e', '--expectedOnly', action='store_true', help='Only show expected limit')

    return parser.parse_args()


def getInput(inputFile):
    """Get all graphs from file as numpy arrays."""
    content = {}
    try:
        with root_open(inputFile) as f:
            for root, dirs, files in f.walk():
                for file in files:
                    data = f.Get(file)
                    # Create buffers
                    x_buff = data.GetX()
                    y_buff = data.GetY()
                    N = data.GetN()
                    x_buff.SetSize(N)
                    y_buff.SetSize(N)
                    # Create arrays from buffers, copy to prevent data loss
                    x_arr = np.array(x_buff, copy=True)
                    y_arr = np.array(y_buff, copy=True)
                    content[file] = [x_arr, y_arr]
    except DoesNotExist:
        print("File does not exist!")

    return content



def plotLimit(inputFile, args):  # exp, exp_1m, exp_1p, exp_2m, exp_2p):
    """Create pretty limit plot with matplotlib."""
    fig, axes = plt.subplots()

    # get input for limit plots
    data = getInput(inputFile)
    obs = data['observed']
    exp = data['expected']
    exp_1m = data['expected_1m']
    exp_1p = data['expected_1p']

    reference = data['run2_2016']

    # plot expected limit contours
    axes.fill_between(exp_1m[0], 0, exp_1m[1], facecolor='#59D354')
    axes.fill_between(exp_1p[0], 0, exp_1p[1], facecolor='white')

    # plot observed and expected limits
    if not args.expectedOnly:
        observedLimit, = axes.plot(obs[0], obs[1], '-', markeredgewidth=0, color='black', linewidth=3)
    expectedLimit, = axes.plot(exp[0], exp[1], '--', markeredgewidth=0, color='black', linewidth=2)

    referenceLimit, = axes.plot(reference[0], reference[1], '-.', markeredgewidth=0, color='#d37254', linewidth=3)

    # plot kinematic limit
    x = np.linspace(300+125, 700+125, 2)
    y = np.linspace(300, 700, 2)
    axes.plot(x, y, 'k-.', color='#999999')
    axes.text(0.1, 0.28, "Kin. limit : $m_{A} = m_{Z'} - m_{h}$",
              verticalalignment='center', horizontalalignment='center',
              transform=axes.transAxes, color='#999999', rotation=70, fontsize=14)


    # add legend
    #yellow_patch, = plt.plot([-1], color='yellow', linewidth=20)
    green_patch, = plt.plot([-1], color='#59D354', linewidth=10)
    handles = []
    names = []
    if not args.expectedOnly:
        names.append('Observed 95% CL')
        handles.append(observedLimit)
    #names.append('Expected 95% CL\n($\pm 1 \sigma$ and $\pm 2 \sigma$)')
    #handles.append((yellow_patch, green_patch, expectedLimit))
    names.append('Expected 95% CL ($\pm 1 \sigma$)')
    handles.append((green_patch, expectedLimit))
    names.append('PRL 119, 181804')
    handles.append(referenceLimit)
 
    leg = plt.legend(handles, names, loc='upper right', bbox_to_anchor=(0.88, 1.0))
    plt.setp(leg.get_title(), fontsize=14)

    # label plot
    axes.set_xlabel(r"$m_{Z'}$ [GeV]",
                    horizontalalignment="right", x=1, labelpad=14, fontsize=24)
    axes.set_ylabel(r"$m_{A}$ [GeV]",
                    horizontalalignment="right", y=1, labelpad=14, fontsize=24)
    # add text
    model1Text = "h(bb) + $E_{T}^{miss}$: Z'+2HDM simplified model"
    model2Text = "$\\tan \\beta$ = 1, $g_{Z}$ = 0.8, $m_{\\chi}$ = 100 GeV, $m_{H} = m_{H^{\pm}}$ = 300 GeV"

    drawATLASLabel(0.05, 0.92, axes, 'prelim', energy='13 TeV', lumi=79.8)

    axes.text(0.05, 0.69, model1Text,
              verticalalignment='center', horizontalalignment='left',
              transform=axes.transAxes, fontsize=18)
    axes.text(0.05, 0.62, model2Text,
              verticalalignment='center', horizontalalignment='left',
              transform=axes.transAxes, fontsize=18)
    axes.set_xlim(300, 3200)
    axes.set_ylim(310, 1000)

    return fig, axes


def main():
    """Create limit plot for the mono-V analysis with ATLAS style."""
    set_style('ATLAS', mpl=True)

    # get input
    args = getArgs()

    # plot limit
    fig, ax = plotLimit(args.inputFile, args)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())

    # conform to the ugly ROOT standard of having axis ticks inside of plot
    ax.get_yaxis().set_tick_params(which='both', direction='in', left='True', right='True')
    ax.get_xaxis().set_tick_params(which='both', direction='in', top='True', bottom='True')

    # save plots
    fig.savefig('{out}.pdf'.format(out=args.outputName), transparent=False, dpi=300, bbox_inches="tight")
    # fig.savefig('{out}.eps'.format(out=args.outputName), transparent=False, dpi=300, bbox_inches="tight")
    print("pdftops -f $1 -l $1 -eps {out}.pdf".format(out=args.outputName))
    os.system("pdftops -f 1 -l 1 -eps {out}.pdf".format(out=args.outputName))
    fig.savefig('{out}.png'.format(out=args.outputName), transparent=False, dpi=300, bbox_inches="tight")


if __name__ == '__main__':
    main()
