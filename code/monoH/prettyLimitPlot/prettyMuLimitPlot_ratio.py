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
    parser.add_argument('inputFile_reference', help='Text file containing upper cross-section limits for the reference')
    parser.add_argument('-o', '--outputName', default='monoHbb-expmulimitratio', help='Name of output file (+.png, .pdf, .eps)')
    parser.add_argument('--tag12', action='store_true', help='Style plot for comparison against 1+2 tag')
    return parser.parse_args()


def getInput(inputFile):
    """Get all graphs from file as numpy arrays and convert from CSV structure.
       Assumed input structure: # mzp + mA + str(exp)+"  "+str(obs)+"  "+str(err1p)+"  "+str(err1m)+"  "+str(err2p)+"  "+str(err2m)
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
            row = re.sub("\s+", ",", row.strip())
            if row.startswith('#') or row.startswith('file'):
                continue
            row = row.split(',')
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


def plotLimit(inputFile, inputFile_reference, tag12):  # exp, exp_1m, exp_1p, exp_2m, exp_2p):
    """Create pretty limit plot with matplotlib."""
    fig, axes_list = plt.subplots(2, 1, sharex=True, gridspec_kw = {'height_ratios':[4, 1]})
    plt.subplots_adjust(hspace=0)

    axes= axes_list[0]
    axes_ratio = axes_list[1]

    axes.xaxis.set_minor_locator(AutoMinorLocator())
    axes.yaxis.set_minor_locator(AutoMinorLocator())
    axes_ratio.xaxis.set_minor_locator(AutoMinorLocator())
    axes_ratio.yaxis.set_minor_locator(AutoMinorLocator())

    # conform to the ugly ROOT standard of having axis ticks inside of plot
    axes.get_yaxis().set_tick_params(which='both', direction='in', left='True', right='True')
    axes.get_xaxis().set_tick_params(which='both', direction='in', top='True', bottom='True')
    axes_ratio.get_yaxis().set_tick_params(which='both', direction='in', left='True', right='True')
    axes_ratio.get_xaxis().set_tick_params(which='both', direction='in', top='True', bottom='True')

    # get input for limit plots
    data = getInput(inputFile)
    data_reference = getInput(inputFile_reference)
    obs = data['observed']
    exp = data['expected']
    exp_1m = data['expected_1m']
    exp_1p = data['expected_1p']
    exp_2m = data['expected_2m']
    exp_2p = data['expected_2p']

    exp_reference = data_reference['expected']

    # plot expected limit contours
    axes.fill_between(exp_2m[0], 0, exp_2m[1], facecolor='yellow')
    axes.fill_between(exp_1m[0], 0, exp_1m[1], facecolor='#59D354')
    axes.fill_between(exp_1p[0], 0, exp_1p[1], facecolor='yellow')
    axes.fill_between(exp_2p[0], 0, exp_2p[1], facecolor='white')

    # plot observed and expected limits
    # observedLimit, = axes.plot(obs[0], obs[1], '-', markeredgewidth=0, color='black', linewidth=2)
    expectedLimit, = axes.plot(exp[0], exp[1], '--', markeredgewidth=0, color='black', linewidth=3)


    # plot reference
    expectedLimitReference, = axes.plot(exp_reference[0], exp_reference[1], '-.', markeredgewidth=0, color='#d35459', linewidth=3)

    # line at 1
    oneLine_up, = axes.plot(exp[0], np.ones(len(exp[0])), '-', markeredgewidth=0, color='#999999', linewidth=1)

    # add legend
    yellow_patch, = plt.plot([-1], color='yellow', linewidth=20)
    green_patch, = plt.plot([-1], color='#59D354', linewidth=10)
    handles = [(yellow_patch, green_patch, expectedLimit), expectedLimitReference]
    names = ['VR track jets 2b\n($\pm 1 \sigma$ and $\pm 2 \sigma$)', 'FR track jets {placeholder}\n(scaled)'.format(placeholder='1+2b' if tag12 else '2b')]
    leg = axes.legend(handles, names, loc=1, bbox_to_anchor=(0.9,1.0))
    plt.setp(leg.get_title(), fontsize=16)

    # label plot
    axes_ratio.set_xlabel(r"$m_{Z'}$ [GeV]",
                    horizontalalignment="right", x=1, labelpad=14)
    axes.set_ylabel("Expected upper limit\non $\\mu$ (95\\% CL)",
                    horizontalalignment="right", y=1, labelpad=14)
    # add text
    mA = inputFile.split('/')[-1][2:-4] #data/mulimits/release20p8.79p8.12b/fixed_mA/data/mA500.dat
    model1Text = "h(bb) + $E_{T}^{miss}$: Z'+2HDM simplified model"
    model2Text = "$\\tan \\beta$ = 1, $g_{{Z}}$ = 0.8, $m_{{\\chi}}$ = 100 GeV, $m_{{A}}$ = {mA} GeV".format(mA=mA) # $m_{H} = m_{H^{\pm}}$ = 300 GeV, 

    drawATLASLabel(0.05, 0.89, axes, 'prelim', energy='13 TeV', lumi=79.8, simulation=False)

    axes.text(0.05, 0.55, model1Text,
              verticalalignment='center', horizontalalignment='left',
              transform=axes.transAxes, fontsize=16)
    axes.text(0.05, 0.46, model2Text,
              verticalalignment='center', horizontalalignment='left',
              transform=axes.transAxes, fontsize=16)
    axes.set_xlim(800, 3000)
    axes.set_ylim(-.5, 12)

    # ratio plot
    exp_ratio = [exp[0], exp_reference[1] / exp[1]]
    expectedLimitRatio, = axes_ratio.plot(exp_ratio[0], exp_ratio[1], '-', markeredgewidth=0, color='black', linewidth=3)
    oneLine, = axes_ratio.plot(exp_ratio[0], np.ones(len(exp_ratio[0])), '-', markeredgewidth=0, color='#999999', linewidth=1)
    axes_ratio.set_ylabel("$\mu$ limit\nFR / VR",
                          horizontalalignment="right", y=1, labelpad=14)
    axes_ratio.set_ylim(0.6, 1.8 if tag12 else 3.4) 

    return fig, axes


def main():
    """Create limit plot for the mono-h(bb) analysis with ATLAS style."""
    set_style('ATLAS', mpl=True)

    # get input
    args = getArgs()

    # plot limit
    fig, ax = plotLimit(args.inputFile, args.inputFile_reference, args.tag12)
    
    # save plots
    fig.savefig('{out}.pdf'.format(out=args.outputName), transparent=False, dpi=300, bbox_inches="tight")
    fig.savefig('{out}.eps'.format(out=args.outputName), transparent=False, dpi=300, bbox_inches="tight")
    fig.savefig('{out}.png'.format(out=args.outputName), transparent=False, dpi=300, bbox_inches="tight")

    
if __name__ == '__main__':
    main()
