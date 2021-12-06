#!/usr/bin/env python
import os
import re
import numpy as np
import pandas as pd
from argparse import ArgumentParser
from ATLASlabel import drawThesisLabel

import matplotlib as mpl
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.colors import LogNorm
from matplotlib.cm import get_cmap
from matplotlib.ticker import MultipleLocator

from scipy import interpolate
from scipy.interpolate import LinearNDInterpolator, CloughTocher2DInterpolator
from scipy.stats import norm
from scipy.spatial import Delaunay

import atlas_mpl_style as ampl
ampl.use_atlas_style()
ampl.set_color_cycle(pal='ATLAS')

# This script borrows heavily from https://github.com/dguest/exclusion-interpolation/

# Input / output utils
def getArgumentParser():
    parser = ArgumentParser(description="Plot limit contour without ROOT. Just using python. Which is nice.")
    parser.add_argument('-i', '--inputFile', action='store', default='data/emulated_limits.csv', help='Input CSV file with limits.')
    parser.add_argument('-o', '--outputDir', action='store', default='plots', help='Output directory')
    parser.add_argument('-t', '--intType', action='store', default='ct', help='Type of interpolation', choices=["linear","ct"])
    parser.add_argument('--crosschecks', action='store_true', help='Add cross-check objects to plot.')
    return parser


def get_mu_limit(inputFile):
    mu_limit_exp, mu_limit_2up, mu_limit_1up, mu_limit_1do, mu_limit_2do, mu_limit_obs = {}, {}, {}, {}, {}, {}

    # scan limit points
    with open(inputFile, 'r') as limitFile:
        # skip header line
        for line in limitFile.readlines()[1:]:
            line = line.replace('\\', '')
            print(line)
            mHeavyHiggs = int(line.split(',')[0])
            mMed = int(line.split(',')[1])
            mu_limit_exp[(mMed, mHeavyHiggs)] = float(line.split(',')[4])
            mu_limit_obs[(mMed, mHeavyHiggs)] = float(line.split(',')[5])
            mu_limit_1up[(mMed, mHeavyHiggs)] = float(line.split(',')[6])
            mu_limit_1do[(mMed, mHeavyHiggs)] = float(line.split(',')[7])
            mu_limit_2up[(mMed, mHeavyHiggs)] = float(line.split(',')[8])
            mu_limit_2do[(mMed, mHeavyHiggs)] = float(line.split(',')[9])

    return mu_limit_exp, mu_limit_2up, mu_limit_1up, mu_limit_1do, mu_limit_2do, mu_limit_obs


def formatForPlot(data):
    X=data.columns.values
    Y=data.index.values
    Z=data.values
    Xi,Yi = np.meshgrid(X, Y)
    return Yi, Xi, Z


def get_xyz_arrays(grid_dict):
    xyz = {(i[0], i[1], p) for i, p in grid_dict.items()}
    x, y, z = zip(*sorted(xyz))
    return np.array(x), np.array(y), np.array(z)


# Interpolation utils
def get_grid(x, y):
    skew = 1e-9
    pts = np.vstack((x - skew*y,y)).T
    return Delaunay(pts)


def _interpolate_linear(pts, z, xp, yp):
    lin = LinearNDInterpolator(pts, z)
    interp_points = np.vstack((xp.flatten(), yp.flatten())).T
    zp = lin(interp_points).reshape(xp.shape)
    return zp

def _interpolate_CloughTocher(pts,z, xp,yp):
    ct = CloughTocher2DInterpolator(pts, z)
    interp_points = np.vstack((xp.flatten(), yp.flatten())).T
    zp = ct(interp_points).reshape(xp.shape)
    return zp

# Plotting utils
class Canvas:
    default_name = 'test.pdf'
    def __init__(self, out_path=None, figsize=(9.0,9.0*2/3), ext=None):
        self.fig = Figure(figsize)
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(1,1,1)
        self.out_path = out_path
        self.ext = ext

    def save(self, out_path=None, ext=None):
        output = out_path or self.out_path
        assert output, "an output file name is required"
        out_dir, out_file = os.path.split(output)
        if ext:
            out_file = '{}.{}'.format(out_file, ext.lstrip('.'))
        if out_dir and not os.path.isdir(out_dir):
            os.makedirs(out_dir)
        self.canvas.print_figure(output, bbox_inches='tight')

    def __enter__(self):
        if not self.out_path:
            self.out_path = self.default_name
        return self
    def __exit__(self, extype, exval, extb):
        if extype:
            return None
        self.save(self.out_path, ext=self.ext)
        return True

def get_axes():
    class Axis:
        def __init__(self, low, high, name, units):
            self.lims = (low, high)
            self.name = name
            self.units = units
        def get_pts(self):
            return np.arange(self.lims[0], self.lims[1], 1)
    return [Axis(100, 500, r"$m_{a}$", "GeV"),
            Axis(800, 1075, r"$m_{H}$", "GeV")]


def set_axes(ax, axes, tick_mult=0.7):
    def _ax_name(ax):
        nm, un = ax.name, ax.units
        return '{} [{}]'.format(nm, un) if un else nm
    _ax_size = 18
    mlx = MultipleLocator(100)
    mly = MultipleLocator(25)
    ax.set_xlim(*axes[0].lims)
    ax.set_ylim(*axes[1].lims)
    ax.get_xaxis().set_minor_locator(mlx)
    ax.get_yaxis().set_minor_locator(mly)
    ax.get_xaxis().set_ticks_position('both')
    ax.get_yaxis().set_ticks_position('both')
    ax.tick_params(labelsize=_ax_size, direction='in', which='both')
    ax.tick_params(which='minor', length=5*tick_mult, pad=2.0)
    ax.tick_params(which='major', length=10*tick_mult,pad=2.0)
    #ax.set_xlabel(_ax_name(axes[0]), x=1.0, ha='right', size=_ax_size)
    #ax.set_ylabel(_ax_name(axes[1]), y=0.98, ha='right', size=_ax_size)
    ampl.set_xlabel(_ax_name(axes[0]),ax=ax,fontsize=18)
    ampl.set_ylabel(_ax_name(axes[1]),ax=ax,fontsize=18)


def main():
    # get arguments
    args = getArgumentParser().parse_args()

    # get the cross section limits
    mu_limit_exp, mu_limit_2up, mu_limit_1up, mu_limit_1do, mu_limit_2do, mu_limit_obs = get_mu_limit(args.inputFile)

    # limit contour ingredients
    bdict = {}
    bands = [('exp', mu_limit_exp),
             ('up1', mu_limit_1up),
             ('dn1', mu_limit_1do),
             ('up2', mu_limit_2up),
             ('dn2', mu_limit_2do),
             ('obs', mu_limit_obs)]
    for name, band in bands:
        bdict[name] = get_xyz_arrays(band)[2]

    # create the axes and grid for interpolation
    x, y, _ = get_xyz_arrays(mu_limit_obs)
    xax, yax = get_axes()
    axes = [xax, yax]
    xx, yy = np.meshgrid(xax.get_pts(), yax.get_pts())
    grid = get_grid(x, y)

    # define output directory
    if not os.path.isdir(args.outputDir):
        os.mkdir(args.outputDir)

    # plot the grid used for interpolation (just as a cross-check)
    if args.crosschecks:
        with Canvas('{outputDir}/grid_structure.pdf'.format(outputDir=args.outputDir)) as can:
            set_axes(can.ax, axes)
            can.ax.triplot(x, y, grid.simplices.copy())

    # interpolate "z-axis" (i.e. limits on signal strength)
    z_grids = {}
    for name, z_vals in bdict.items():
        if args.intType == 'linear':
            interp = _interpolate_linear(grid, z_vals, xx, yy)
        elif args.intType == 'ct':
            interp = _interpolate_CloughTocher(grid, z_vals, xx, yy)

        z_grids[name] = interp

    # plot the exclusion contour
    with Canvas('{outputDir}/limit_contour_monoZ.pdf'.format(outputDir=args.outputDir)) as can:
        mpl.rc('font',**{'family':'sans-serif','sans-serif':['helvetica']})

        set_axes(can.ax, axes)
        zp2 = np.maximum( (z_grids['dn2'] - 1), -(z_grids['up2'] - 1))
        zp1 = np.maximum( (z_grids['dn1'] - 1), -(z_grids['up1'] - 1))
        can.ax.contourf(xx, yy, zp2, [-1, 0],
                        colors=['yellow'], zorder=0)
        can.ax.contourf(xx, yy, zp1, [-1, 0],
                        colors=['#59D354'], zorder=0)
        expectedLimit = can.ax.contour(xx, yy, z_grids['exp'], [1], colors=['k'],
                    linestyles=['--'], linewidths=[2])
        observedLimit = can.ax.contour(xx, yy, z_grids['obs'], [1], colors=['black'],
                    linestyles=['-'], linewidths=[3])

        if args.crosschecks:
            # draw borders of exclusion contours: only for cross-checks
            can.ax.contour(xx, yy, z_grids['dn1'], [1], colors=['green'],
                        linestyles=['--'])
            can.ax.contour(xx, yy, z_grids['up1'], [1], colors=['green'],
                        linestyles=['--'])
            can.ax.contour(xx, yy, z_grids['dn2'], [1], colors=['orange'],
                        linestyles=['--'])
            can.ax.contour(xx, yy, z_grids['up2'], [1], colors=['orange'],
                        linestyles=['--'])

            # draw points used for drawing the contours
            can.ax.plot(x, y, '.')


        # draw ATLAS label
        drawThesisLabel(0.6, 0.95, ax=can.ax, energy='13 TeV', lumi=36.1)

        # draw descriptions
        description = '$E_{T}^{miss}$ + Z(qq):\n$a$-2HDM, Dirac DM\n$m_{\chi} = 10\,$GeV, $g_{\chi} = 1$,\n$\sin \\theta = 0.35$, $\\tan \\beta = 1$\n $m_{A} = m_{H^{\pm}} = m_{H}$'
        can.ax.text(0.65, 0.77, description, verticalalignment='top', horizontalalignment='left', transform=can.ax.transAxes, fontsize=18)


        # add legend (note: the first four objects are plotted outside the visible range and serve
        # as proxy artists for the contour plots, which don't go well with legends)
        line_exp, = can.ax.plot([-1], color='k', linestyle='--', linewidth=2)
        line_obs, = can.ax.plot([-1], color='black', linestyle='-', linewidth=3)
        yellow_patch, = can.ax.plot([-1], color='yellow', linewidth=20)
        green_patch, = can.ax.plot([-1], color='#59D354', linewidth=10)

        handles = [line_obs, (yellow_patch, green_patch, line_exp)]
        names = ['Observed limit', 'Expected limit\n($\pm 1 \sigma$ and $\pm 2 \sigma$)']
        leg = can.ax.legend(handles, names, loc='upper right', bbox_to_anchor=(1.0, 0.4), frameon=False, fontsize=18)

        # enforce the label tick styling in a most ugly way
        can.ax.set_yticks([850, 900, 950, 1000, 1050])

if __name__ == '__main__':
    main()
