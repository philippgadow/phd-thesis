#!/bin/env python
from __future__ import unicode_literals

import numpy as np
import pandas as pd
from argparse import ArgumentParser

import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from ATLASlabel import drawThesisLabel

import atlas_mpl_style as ampl


def getArgs():
    """Get arguments from command line."""
    parser = ArgumentParser()
    parser.add_argument('-i', '--inputFile', default='data/limits_sintheta.csv', help='CSV file with limits')
    parser.add_argument('-o', '--outputName', default='monoZ_PS2HDM', help='Name of output file (+.png, .pdf, .eps)')
    parser.add_argument('-x', '--xSecFile', default='data/XSections_13TeV.txt', help='Name of file containing cross-sections.')
    parser.add_argument('-H', '--heavyHiggsMass', default=600, help='Mass of heavy Higgs boson')
    parser.add_argument('-m', '--medMass', default=200, help='Mass of mediator')
    parser.add_argument('--doDMScan', action='store_true', help='Produce scan of DM mass instead')
    return parser.parse_args()


# def getXsection(xSecFile, TanBeta, HeavyHiggsMass, MedMass, DarkMatterMass):
#     """Get cross-section from file."""
#     df = pd.read_csv(xSecFile, header=None, delim_whitespace=True, names=['dsid', 'xsec', 'kfactor', 'filter', 'name', 'longname'])
#     df = df.iloc[:, [1, 3, 4]]

#     if TanBeta == 1.0:
#         TanBeta = '1p0'
#     elif TanBeta == 3.0:
#         TanBeta = '3p0'
#     elif TanBeta == 0.5:
#         TanBeta = '0p5'
#     elif TanBeta == 0.3:
#         TanBeta = '0p3'
#     name = 'PS2HDMtanb' + TanBeta + 'mA' + str(HeavyHiggsMass) + 'ma' + str(MedMass)

#     df = df.loc[(df['name'] == name)]
#     xsec = 0.
#     filtertotal = 0.
#     for index, row in df.iterrows():
#         xsec += float(row['filter']) * float(row['xsec'])
#         filtertotal += float(row['filter'])
#     xsec /= filtertotal

#     return xsec


def getInput(inputFile, xSecFile, heavyHiggsMass, medMass, doDMScan):
    """Get all graphs from file as numpy arrays and convert from CSV structure.
       Assumed input structure: x, observed, expected, expected1m, expected1p, expected2m, expected2p.
       Output structure: content dictionary with entries
                         observed, expected, expected_1m, expected_1p, expected_2m, expected_2p"""
    content = {}

    darkMatterMass = 10.
    tanBeta = 1.

    df = pd.read_csv(inputFile)
    df.HeavyHiggsMass = df.HeavyHiggsMass.astype(float).fillna(0.0)
    df.MedMass = df.MedMass.astype(float).fillna(0.0)
    df.TanBeta = df.TanBeta.astype(float).fillna(0.0)
    if not doDMScan: df.SinTheta = df.SinTheta.astype(float).fillna(0.0)
    df.DarkMatterMass = df.DarkMatterMass.astype(float).fillna(0.0)
    df.ObsLimit = df.ObsLimit.astype(float).fillna(0.0)
    df.ExpLimit = df.ExpLimit.astype(float).fillna(0.0)
    df.Sigma1Minus = df.Sigma1Minus.astype(float).fillna(0.0)
    df.Sigma1Plus = df.Sigma1Plus.astype(float).fillna(0.0)
    df.Sigma2Minus = df.Sigma2Minus.astype(float).fillna(0.0)
    df.Sigma2Plus = df.Sigma2Plus.astype(float).fillna(0.0)
    if doDMScan:
        df = df.sort_values(['HeavyHiggsMass', 'MedMass', 'DarkMatterMass', 'TanBeta'])
        heavyHiggsMass = 600.
        medMass = 250.
        df = df.loc[(df['HeavyHiggsMass'] == float(heavyHiggsMass)) & (df['MedMass'] == float(medMass)) & (df['TanBeta'] == tanBeta)]
        x = df['DarkMatterMass']
    else:
        df = df.sort_values(['HeavyHiggsMass', 'MedMass', 'DarkMatterMass', 'TanBeta', 'SinTheta'])
        df = df.loc[(df['HeavyHiggsMass'] == float(heavyHiggsMass)) & (df['MedMass'] == float(medMass)) & (df['DarkMatterMass'] == darkMatterMass) & (df['TanBeta'] == tanBeta)]
        x = df['SinTheta']

    observed = df['ObsLimit']
    expected = df['ExpLimit']
    expected1p = df['Sigma1Minus']
    expected1m = df['Sigma1Plus']
    expected2p = df['Sigma2Minus']
    expected2m = df['Sigma2Plus']

    x_arr = np.array(x, copy=True)
    observed_arr = np.array(observed, copy=True)
    expected_arr = np.array(expected, copy=True)
    expected1m_arr = np.array(expected1m, copy=True)
    expected1p_arr = np.array(expected1p, copy=True)
    expected2m_arr = np.array(expected2m, copy=True)
    expected2p_arr = np.array(expected2p, copy=True)

    # for i, x in enumerate(x_arr):
    #     observed_arr[i] *= getXsection(xSecFile, x, HeavyHiggsMass, medMass, DarkMatterMass)
    #     expected_arr[i] *= getXsection(xSecFile, x, HeavyHiggsMass, medMass, DarkMatterMass)
    #     expected1m_arr[i] *= getXsection(xSecFile, x, HeavyHiggsMass, medMass, DarkMatterMass)
    #     expected1p_arr[i] *= getXsection(xSecFile, x, HeavyHiggsMass, medMass, DarkMatterMass)
    #     expected2m_arr[i] *= getXsection(xSecFile, x, HeavyHiggsMass, medMass, DarkMatterMass)
    #     expected2p_arr[i] *= getXsection(xSecFile, x, HeavyHiggsMass, medMass, DarkMatterMass)

    content['observed'] = [x_arr, observed_arr]
    content['expected'] = [x_arr, expected_arr]
    content['expected_1m'] = [x_arr, expected1m_arr]
    content['expected_1p'] = [x_arr, expected1p_arr]
    content['expected_2m'] = [x_arr, expected2m_arr]
    content['expected_2p'] = [x_arr, expected2p_arr]

    return content


def plotLimit(inputFile, xSecFile, heavyHiggsMass, medMass, doDMScan=False):
    """Create pretty limit plot with matplotlib."""
    fig, ax = plt.subplots()

    # get input for limit plots
    data = getInput(inputFile, xSecFile, heavyHiggsMass, medMass, doDMScan)
    obs = data['observed']
    exp = data['expected']
    exp_1m = data['expected_1m']
    exp_1p = data['expected_1p']
    exp_2m = data['expected_2m']
    exp_2p = data['expected_2p']

    # plot expected limit contours
    ax.fill_between(exp_2m[0], 0, exp_2m[1], facecolor='yellow')
    ax.fill_between(exp_1m[0], 0, exp_1m[1], facecolor='#59D354')
    ax.fill_between(exp_1p[0], 0, exp_1p[1], facecolor='yellow')
    ax.fill_between(exp_2p[0], 0, exp_2p[1], facecolor='white')

    # plot observed and expected limits
    observedLimit, = ax.plot(obs[0], obs[1], '-', markeredgewidth=0, color='black', linewidth=3)
    expectedLimit, = ax.plot(exp[0], exp[1], '--', markeredgewidth=0, color='black', linewidth=2)

    # plot vertical line at 1
    x = np.linspace(0, 1)
    y = np.ones_like(x)
    ax.plot(x, y, 'k--', color='#999999')

    # add legend
    yellow_patch, = plt.plot([-1], color='yellow', linewidth=20)
    green_patch, = plt.plot([-1], color='#59D354', linewidth=10)
    handles = [observedLimit, (yellow_patch, green_patch, expectedLimit)]
    names = ['Observed limit', 'Expected limit\n($\pm 1 \sigma$ and $\pm 2 \sigma$)']
    leg = plt.legend(handles, names, loc=1, frameon=False)
    plt.setp(leg.get_title(), fontsize=16)

    # label plot
    xlabel = r"$m_{\chi}$ [GeV]" if doDMScan else r"$\sin \theta$"
    ax.set_xlabel(xlabel,
                    horizontalalignment="right", x=1, labelpad=20)
    # ax.set_ylabel(r"Cross-section ($\sigma$) [pb]",
    #                 horizontalalignment="right", y=1, labelpad=32)
    ax.set_ylabel(r"$\sigma / \sigma_{\textsf{theory}}$",
                    horizontalalignment="right", y=1, labelpad=32)
    # add text
    if doDMScan:
        model1Text = "$E_{T}^{miss}$ + Z(qq):\n$a$-2HDM, Dirac DM"
        model2Text = "$m_{H} = 600$\,GeV,\n$m_{a} = 250$\,GeV,\n$\\sin \\theta = 0.35$,\n$\\tan \\beta = 1$"
        ax.text(0.65, 0.61, model1Text,
              verticalalignment='center', horizontalalignment='left',
              transform=ax.transAxes, fontsize=16)
        ax.text(0.65, 0.42, model2Text,
              verticalalignment='center', horizontalalignment='left',
              transform=ax.transAxes, fontsize=16)
    else:
        model1Text = "$E_{T}^{miss}$ + Z(qq): $a$-2HDM, Dirac DM"
        model2Text = "$m_{{H}} = {heavyHiggsMass}$\,GeV, $m_{{a}} = {medMass}$\,GeV, $m_{{\chi}} = 10$\,GeV, $\\tan \\beta = 1$".format(heavyHiggsMass=heavyHiggsMass, medMass=medMass)
        ax.text(0.04, 0.81, model1Text,
              verticalalignment='center', horizontalalignment='left',
              transform=ax.transAxes, fontsize=16)
        ax.text(0.04, 0.72, model2Text,
              verticalalignment='center', horizontalalignment='left',
              transform=ax.transAxes, fontsize=16)
    drawThesisLabel(0.04, 0.95, ax, energy='13 TeV', lumi=36.1)

    if doDMScan:
        ax.set_xlim(10, 210)
        plt.yscale('log')
        ax.set_ylim(0.55, 30)
    else:
        ax.set_xlim(0.1, 0.9)
        plt.yscale('log')
        ax.set_ylim(0.2, 390)

    return fig, ax


def main():
    """Create limit plot for the mono-V analysis with ATLAS style."""
    ampl.use_atlas_style()

    # get input
    args = getArgs()

    # plot limit
    fig, ax = plotLimit(args.inputFile, args.xSecFile, args.heavyHiggsMass, args.medMass, args.doDMScan)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    # ax.yaxis.set_minor_locator(AutoMinorLocator())

    # conform to the ugly ROOT standard of having axis ticks inside of plot
    ax.get_yaxis().set_tick_params(which='both', direction='in')
    ax.get_xaxis().set_tick_params(which='both', direction='in')

    # save plots
    if args.doDMScan:
        fig.savefig('{out}_dmScan.pdf'.format(out=args.outputName), transparent=False, dpi=300, bbox_inches="tight")
    else:
        fig.savefig('{out}_massHeavyHiggs{heavyHiggsMass}_massMed{medMass}.pdf'.format(out=args.outputName, heavyHiggsMass=args.heavyHiggsMass, medMass=args.medMass), transparent=False, dpi=300, bbox_inches="tight")

if __name__ == '__main__':
    main()
