#!/bin/env python

import ROOT
import math
from argparse import ArgumentParser


def getArgs():
    """Get arguments from command line."""
    parser = ArgumentParser()
    parser.add_argument("inputFile")
    return parser.parse_args()


def getBackground(f, histname):
    try:
        h = f.Get(histname)
        e = ROOT.Double()
        y = h.IntegralAndError(h.GetXaxis().GetFirst() + 500, h.GetXaxis().GetLast(), e)
    except AttributeError:
        y = 0.
        e = 0.
    return y, e


def getSummedBackground(f, backgrounds, region, var):
    y_total = 0.
    e_total = 0.
    for bg in backgrounds:
        y, e = getBackground(f, bg + '_' + region + '_' + var)
        y_total += y
        e_total += e * e
    e_total = math.sqrt(e_total)
    return y_total, e_total


def parseRegion(region):
    if region == "0tag1pfat0pjet_0ptv_0lep_SR_SubstrPassMassPass":
        return "merged 0 tag high purity signal region"
    elif region == "0tag1pfat0pjet_0ptv_0lep_SR_SubstrFailMassPass":
        return "merged 0 tag low purity signal region"
    elif region == "1tag1pfat0pjet_0ptv_0lep_SR_SubstrPassMassPass":
        return "merged 1 tag high purity signal region"
    elif region == "1tag1pfat0pjet_0ptv_0lep_SR_SubstrFailMassPass":
        return "merged 1 tag low purity signal region"
    elif region == "2tag1pfat0pjet_0ptv_0lep_SR_MassPass":
        return "merged 2 tag signal region"
    elif region == "0tag0pfat0pjet_0ptv_0lep_SR_MassPass":
        return "resolved 0 tag signal region"
    elif region == "1tag0pfat0pjet_0ptv_0lep_SR_MassPass":
        return "resolved 1 tag signal region"
    elif region == "2tag0pfat0pjet_0ptv_0lep_SR_MassPass":
        return "resolved 2 tag signal region"
    return region


def main():
    """For a group of background physics processes iterate over specified histograms in ROOT input file and print out LaTeX table with yield and statistical uncertainty."""

    args = getArgs()
    f = ROOT.TFile.Open(args.inputFile, "R")

    var = "MET"
    regions = [
        "0tag1pfat0pjet_0ptv_0lep_SR_SubstrPassMassPass",
        "0tag1pfat0pjet_0ptv_0lep_SR_SubstrFailMassPass",
        "1tag1pfat0pjet_0ptv_0lep_SR_SubstrPassMassPass",
        "1tag1pfat0pjet_0ptv_0lep_SR_SubstrFailMassPass",
        "2tag1pfat0pjet_0ptv_0lep_SR_MassPass",
        "0tag0pfat0pjet_0ptv_0lep_SR_MassPass",
        "1tag0pfat0pjet_0ptv_0lep_SR_MassPass",
        "2tag0pfat0pjet_0ptv_0lep_SR_MassPass"
    ]

    backgrounds = [
        ['data', ['data']],
        # ['dmVhadDM1MM10', ['dmVWhadDM1MM10', 'dmVZhadDM1MM10']],
        # ['dmVhadDM1MM100', ['dmVWhadDM1MM100', 'dmVZhadDM1MM100']],
        # ['dmVhadDM1MM200', ['dmVWhadDM1MM200', 'dmVZhadDM1MM200']],
        # ['dmVhadDM1MM300', ['dmVWhadDM1MM300', 'dmVZhadDM1MM300']],
        # ['dmVhadDM50MM300', ['dmVWhadDM50MM300', 'dmVZhadDM50MM300']],
        # ['dmVhadDM1MM400', ['dmVWhadDM1MM400', 'dmVZhadDM1MM400']],
        # ['dmVhadDM1MM500', ['dmVWhadDM1MM500', 'dmVZhadDM1MM500']],
        # ['dmVhadDM1MM600', ['dmVWhadDM1MM600', 'dmVZhadDM1MM600']],
        # ['dmVhadDM1MM700', ['dmVWhadDM1MM700', 'dmVZhadDM1MM700']],
        # ['dmVhadDM1MM800', ['dmVWhadDM1MM800', 'dmVZhadDM1MM800']],
        # ['dmVhadDM1MM900', ['dmVWhadDM1MM900', 'dmVZhadDM1MM900']],
        # ['dmVhadDM1MM1000', ['dmVWhadDM1MM1000', 'dmVZhadDM1MM1000']],
        # ['dmVhadDM1MM2000', ['dmVWhadDM1MM2000', 'dmVZhadDM1MM2000']],
        ['ttbar', ['ttbar']],
        ['diboson', ['WW', 'WZ', 'ZZ']],
        ['single top', ['stops', 'stopt', 'stopWt']],
        ['multijet', ['multijet0resolvedMassPass']],
        ['W + jets', ['Wl', 'Wcl', 'Wcc', 'Wbb', 'Wbl', 'Wbc']],
        ['Z + jets', ['Zl', 'Zcl', 'Zcc', 'Zbb', 'Zbl', 'Zbc']]
    ]

    for region in regions:
        print("\\begin{\\table}[!h]")
        print("\caption{{Expected event yields and statistical uncertainty for simulated samples in {region}.}}".format(region=parseRegion(region)))
        print("\\begin{\\tabular}{lrr}")
        print("\\toprule")
        print("sample & event yield & statistical uncertainty")
        print("\\mediumrule")
        for name, bg in backgrounds:
            y, e = getSummedBackground(f, bg, region, var)
            print("{name} & {events:.2f} \pm {error:.2f}".format(name=name, events=y, error=e))
        print("\\bottomrule")
        print("\end{tabular}")
        print("\end{table}\n")

 
if __name__ == '__main__':
    main()
