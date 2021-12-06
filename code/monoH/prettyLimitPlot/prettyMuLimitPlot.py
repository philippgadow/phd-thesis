#!/bin/env python
from __future__ import unicode_literals

import numpy as np
import csv
from argparse import ArgumentParser

from rootpy.plotting.style import set_style
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from ATLASlabel import drawATLASLabel
import re

matplotlib.rc('text', usetex = True)

def getArgs():
    """Get arguments from command line."""
    parser = ArgumentParser()
    parser.add_argument('inputFile', help='Text file containing upper cross-section limits')
    parser.add_argument('-o', '--outputName', default='monoHbb-mulimit', help='Name of output file (+.png, .pdf, .eps)')
    return parser.parse_args()


def getInput(inputFile):
    """Get all graphs from file as numpy arrays and convert from CSV structure.
       Assumed input structure: mzp + mA + str(exp)+"  "+str(obs)+"  "+str(err1p)+"  "+str(err1m)+"  "+str(err2p)+"  "+str(err2m)
       Output structure: content dictionary with entries
                         observerved, expected, expected_1m, expected_1p, expected_2m, expected_2p"""
    content = {}

    x = []
    observed = []
    expected = []
    expected1m = []
    expected1p = []
    expected2m = []
    expected2p = []

    with open(inputFile, "r") as ifile:

        # input structure
        # mzp + mA + str(exp)+"  "+str(obs)+"  "+str(err1p)+"  "+str(err1m)+"  "+str(err2p)+"  "+str(err2m)
        for row in sorted(ifile):
            print(row)
            row = re.sub("\s+", ",", row.strip())
            print(row)
            if row.startswith('#') or row.startswith('file'):
                continue
            row = row.split(',')
            print(row)
            mzp = float(row[0])
            mA = float(row[1])

            x.append(mzp)
            expected.append(float(row[2]))
            observed.append(float(row[3]))
            expected1m.append(float(row[4]))
            expected1p.append(float(row[5]))
            expected2m.append(float(row[6]))
            expected2p.append(float(row[7]))


    x_arr = np.array(x, copy=True)
    observed_arr = np.array(observed, copy=True)
    expected_arr = np.array(expected, copy=True)
    expected1m_arr = np.array(expected1m, copy=True)
    expected1p_arr = np.array(expected1p, copy=True)
    expected2m_arr = np.array(expected2m, copy=True)
    expected2p_arr = np.array(expected2p, copy=True)

    content['expected'] = [x_arr, observed_arr]
    content['observed'] = [x_arr, expected_arr]
    content['expected_1m'] = [x_arr, expected1m_arr]
    content['expected_1p'] = [x_arr, expected1p_arr]
    content['expected_2m'] = [x_arr, expected2m_arr]
    content['expected_2p'] = [x_arr, expected2p_arr]

    return content


def plotLimit(inputFile):  # exp, exp_1m, exp_1p, exp_2m, exp_2p):
    """Create pretty limit plot with matplotlib."""
    fig, axes = plt.subplots()

    # get input for limit plots
    data = getInput(inputFile)
    obs = data['observed']
    exp = data['expected']
    exp_1m = data['expected_1m']
    exp_1p = data['expected_1p']
    exp_2m = data['expected_2m']
    exp_2p = data['expected_2p']


    # plot expected limit contours
    axes.fill_between(exp_2m[0], 0, exp_2m[1], facecolor='yellow')
    axes.fill_between(exp_1m[0], 0, exp_1m[1], facecolor='#59D354')
    axes.fill_between(exp_1p[0], 0, exp_1p[1], facecolor='yellow')
    axes.fill_between(exp_2p[0], 0, exp_2p[1], facecolor='white')

    # plot observed and expected limits
    observedLimit, = axes.plot(obs[0], obs[1], '-', markeredgewidth=0, color='black', linewidth=3)
    expectedLimit, = axes.plot(exp[0], exp[1], '--', markeredgewidth=0, color='black', linewidth=2)


    # add legend
    yellow_patch, = plt.plot([-1], color='yellow', linewidth=20)
    green_patch, = plt.plot([-1], color='#59D354', linewidth=10)
    handles = [observedLimit, (yellow_patch, green_patch, expectedLimit)]
    names = ['Observed limit', 'Expected limit\n($\pm 1 \sigma$ and $\pm 2 \sigma$)']
    leg = plt.legend(handles, names, loc=1, bbox_to_anchor=(0.85,1.0))
    plt.setp(leg.get_title(), fontsize=16)

    # label plot
    axes.set_xlabel(r"$m_{Z'}$ [GeV]",
                    horizontalalignment="right", x=1, labelpad=14)
    axes.set_ylabel(r"Upper limit on $\mu$",
                    horizontalalignment="right", y=1, labelpad=14)
    # add text
    model1Text = "Mono-h(bb): Z'+2HDM"

    model2Text = "$m_{A}$ = 500 GeV"
    drawATLASLabel(0.05, 0.95, axes, 'prelim', energy='13 TeV', lumi=79.8, simulation=False)

    axes.text(0.05, 0.77, model1Text,
              verticalalignment='center', horizontalalignment='left',
              transform=axes.transAxes, fontsize=16)
    axes.text(0.05, 0.69, model2Text,
              verticalalignment='center', horizontalalignment='left',
              transform=axes.transAxes, fontsize=16)
    axes.set_xlim(700, 3200)
    axes.set_ylim(0.01, 16)

    return fig, axes


def main():
    """Create limit plot for the mono-h(bb) analysis with ATLAS style."""
    set_style('ATLAS', mpl=True)

    # get input
    args = getArgs()

    # plot limit
    fig, ax = plotLimit(args.inputFile)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())

    # conform to the ugly ROOT standard of having axis ticks inside of plot
    ax.get_yaxis().set_tick_params(which='both', direction='in', left='True', right='True')
    ax.get_xaxis().set_tick_params(which='both', direction='in', top='True', bottom='True')

    # save plots
    fig.savefig('{out}.pdf'.format(out=args.outputName), transparent=False, dpi=300, bbox_inches="tight")
    fig.savefig('{out}.eps'.format(out=args.outputName), transparent=False, dpi=300, bbox_inches="tight")
    fig.savefig('{out}.png'.format(out=args.outputName), transparent=False, dpi=300, bbox_inches="tight")

    
if __name__ == '__main__':
    main()
