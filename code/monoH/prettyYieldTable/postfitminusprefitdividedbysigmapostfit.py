#!/bin/env python

import ROOT
import csv
import math
from argparse import ArgumentParser


def getArgs():
    """Get arguments from command line."""
    parser = ArgumentParser()
    parser.add_argument("inputFile")
    parser.add_argument("inputCSV")

    return parser.parse_args()


def readData(inputFile):
    """Read data from csv file."""
    data = {}
    with open(inputFile, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        # structure of row: region,sample,yield,uncertainty
        for row in reader:
            if row[1] not in data:
                data[row[1]] = {}
            try:
                data[row[1]][row[0]] = [float(row[2]), float(row[3])]
            except Exception:
                data[row[1]][row[0]] = [float(0.), float(0.)]
    return data


def getBackground(f, histname):
    try:
        h = f.Get(histname)
        e = ROOT.Double()
        y = h.IntegralAndError(h.GetXaxis().GetFirst(), h.GetXaxis().GetLast(), e)
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
        return "Zero lepton 0 tag merged D2 passed signal region"
    elif region == "0tag1pfat0pjet_0ptv_0lep_SR_SubstrFailMassPass":
        return "Zero lepton 0 tag merged D2 failed signal region"
    elif region == "1tag1pfat0pjet_0ptv_0lep_SR_SubstrPassMassPass":
        return "Zero lepton 1 tag merged D2 passed signal region"
    elif region == "1tag1pfat0pjet_0ptv_0lep_SR_SubstrFailMassPass":
        return "Zero lepton 1 tag merged D2 failed signal region"
    elif region == "2tag1pfat0pjet_0ptv_0lep_SR_MassPass":
        return "Zero lepton 2 tag merged signal region"
    elif region == "0tag0pfat0pjet_0ptv_0lep_SR_MassPass":
        return "Zero lepton 0 tag resolved signal region"
    elif region == "1tag0pfat0pjet_0ptv_0lep_SR_MassPass":
        return "Zero lepton 1 tag resolved signal region"
    elif region == "2tag0pfat0pjet_0ptv_0lep_SR_MassPass":
        return "Zero lepton 2 tag resolved signal region"
    elif region == "0tag1pfat0pjet_0ptv_0lep_SR_SubstrPassMassFailHigh":
        return "Zero lepton 0 tag merged D2 passed upper side-band"
    elif region == "0tag1pfat0pjet_0ptv_0lep_SR_SubstrFailMassFailHigh":
        return "Zero lepton 0 tag merged D2 failed upper side-band"
    elif region == "1tag1pfat0pjet_0ptv_0lep_SR_SubstrPassMassFailHigh":
        return "Zero lepton 1 tag merged D2 passed upper side-band"
    elif region == "1tag1pfat0pjet_0ptv_0lep_SR_SubstrFailMassFailHigh":
        return "Zero lepton 1 tag merged D2 failed upper side-band"
    elif region == "2tag1pfat0pjet_0ptv_0lep_SR_MassFailHigh":
        return "Zero lepton 2 tag merged upper side-band"
    elif region == "0tag0pfat0pjet_0ptv_0lep_SR_MassFailHigh":
        return "Zero lepton 0 tag resolved upper side-band"
    elif region == "1tag0pfat0pjet_0ptv_0lep_SR_MassFailHigh":
        return "Zero lepton 1 tag resolved upper side-band"
    elif region == "2tag0pfat0pjet_0ptv_0lep_SR_MassFailHigh":
        return "Zero lepton 2 tag resolved upper side-band"
    elif region == "0tag1pfat0pjet_0ptv_1lep_CR_MassPass":
        return "One lepton 0 tag merged control region"
    elif region == "1tag1pfat0pjet_0ptv_1lep_CR_MassPass":
        return "One lepton 1 tag merged control region"
    elif region == "2tag1pfat0pjet_0ptv_1lep_CR_MassPass":
        return "One lepton 2 tag merged control region"
    elif region == "0tag0pfat0pjet_0ptv_1lep_CR_MassPass":
        return "One lepton 0 tag resolved control region"
    elif region == "1tag0pfat0pjet_0ptv_1lep_CR_MassPass":
        return "One lepton 1 tag resolved control region"
    elif region == "2tag0pfat0pjet_0ptv_1lep_CR_MassPass":
        return "One lepton 2 tag resolved control region"
    elif region == "0tag1pfat0pjet_0ptv_1lep_CR_MassFailHigh":
        return "One lepton 0 tag merged upper side-band"
    elif region == "1tag1pfat0pjet_0ptv_1lep_CR_MassFailHigh":
        return "One lepton 1 tag merged upper side-band"
    elif region == "2tag1pfat0pjet_0ptv_1lep_CR_MassFailHigh":
        return "One lepton 2 tag merged upper side-band"
    elif region == "0tag0pfat0pjet_0ptv_1lep_CR_MassFailHigh":
        return "One lepton 0 tag resolved upper side-band"
    elif region == "1tag0pfat0pjet_0ptv_1lep_CR_MassFailHigh":
        return "One lepton 1 tag resolved upper side-band"
    elif region == "2tag0pfat0pjet_0ptv_1lep_CR_MassFailHigh":
        return "One lepton 2 tag resolved upper side-band"
    elif region == "0tag1pfat0pjet_0ptv_2lep_CR_MassPass":
        return "Two lepton 0 tag merged control region"
    elif region == "1tag1pfat0pjet_0ptv_2lep_CR_MassPass":
        return "Two lepton 1 tag merged control region"
    elif region == "2tag1pfat0pjet_0ptv_2lep_CR_MassPass":
        return "Two lepton 2 tag merged control region"
    elif region == "0tag0pfat0pjet_0ptv_2lep_CR_MassPass":
        return "Two lepton 0 tag resolved control region"
    elif region == "1tag0pfat0pjet_0ptv_2lep_CR_MassPass":
        return "Two lepton 1 tag resolved control region"
    elif region == "2tag0pfat0pjet_0ptv_2lep_CR_MassPass":
        return "Two lepton 2 tag resolved control region"
    elif region == "0tag1pfat0pjet_0ptv_2lep_CR_MassFailHigh":
        return "Two lepton 0 tag merged upper side-band"
    elif region == "1tag1pfat0pjet_0ptv_2lep_CR_MassFailHigh":
        return "Two lepton 1 tag merged upper side-band"
    elif region == "2tag1pfat0pjet_0ptv_2lep_CR_MassFailHigh":
        return "Two lepton 2 tag merged upper side-band"
    elif region == "0tag0pfat0pjet_0ptv_2lep_CR_MassFailHigh":
        return "Two lepton 0 tag resolved upper side-band"
    elif region == "1tag0pfat0pjet_0ptv_2lep_CR_MassFailHigh":
        return "Two lepton 1 tag resolved upper side-band"
    elif region == "2tag0pfat0pjet_0ptv_2lep_CR_MassFailHigh":
        return "Two lepton 2 tag resolved upper side-band"
    return region


def getSumForBackgrounds(data, backgrounds, regions):
    """Sum different flavours for grouped processes."""
    evt_yield = 0.
    sigma_evt_yield = 0.
    for bg in backgrounds:
        for r in regions:
            evt_yield += data[bg][parseRegion(r)][0]
            sigma_evt_yield += data[bg][parseRegion(r)][1] * data[bg][parseRegion(r)][1]
    sigma_evt_yield = math.sqrt(sigma_evt_yield)
    return evt_yield, sigma_evt_yield


def main():
    """For a group of background physics processes iterate over specified histograms in ROOT input file and print out LaTeX table with yield and statistical uncertainty."""

    args = getArgs()
    f = ROOT.TFile.Open(args.inputFile, "R")
    data = readData(args.inputCSV)

    # 0 lepton
    # var = "MET"
    # regions = [
    #     "0tag1pfat0pjet_0ptv_0lep_SR_SubstrPassMassPass",
    #     "0tag1pfat0pjet_0ptv_0lep_SR_SubstrFailMassPass",
    #     "1tag1pfat0pjet_0ptv_0lep_SR_SubstrPassMassPass",
    #     "1tag1pfat0pjet_0ptv_0lep_SR_SubstrFailMassPass",
    #     "2tag1pfat0pjet_0ptv_0lep_SR_MassPass",
    #     "0tag0pfat0pjet_0ptv_0lep_SR_MassPass",
    #     "1tag0pfat0pjet_0ptv_0lep_SR_MassPass",
    #     "2tag0pfat0pjet_0ptv_0lep_SR_MassPass"
    # ]

    # regions = [
    #     "0tag1pfat0pjet_0ptv_0lep_SR_SubstrPassMassFailHigh",
    #     "0tag1pfat0pjet_0ptv_0lep_SR_SubstrFailMassFailHigh",
    #     "1tag1pfat0pjet_0ptv_0lep_SR_SubstrPassMassFailHigh",
    #     "1tag1pfat0pjet_0ptv_0lep_SR_SubstrFailMassFailHigh",
    #     "2tag1pfat0pjet_0ptv_0lep_SR_MassFailHigh",
    #     "0tag0pfat0pjet_0ptv_0lep_SR_MassFailHigh",
    #     "1tag0pfat0pjet_0ptv_0lep_SR_MassFailHigh",
    #     "2tag0pfat0pjet_0ptv_0lep_SR_MassFailHigh"
    # ]

    # 1 lepton
    # var = "MU_METMod"
    # regions = [
    #     "0tag1pfat0pjet_0ptv_1lep_CR_MassPass",
    #     "1tag1pfat0pjet_0ptv_1lep_CR_MassPass",
    #     "2tag1pfat0pjet_0ptv_1lep_CR_MassPass",
    #     "0tag0pfat0pjet_0ptv_1lep_CR_MassPass",
    #     "1tag0pfat0pjet_0ptv_1lep_CR_MassPass",
    #     "2tag0pfat0pjet_0ptv_1lep_CR_MassPass"
    # ]

    # regions = [
    #     "0tag1pfat0pjet_0ptv_1lep_CR_MassFailHigh",
    #     "1tag1pfat0pjet_0ptv_1lep_CR_MassFailHigh",
    #     "2tag1pfat0pjet_0ptv_1lep_CR_MassFailHigh",
    #     "0tag0pfat0pjet_0ptv_1lep_CR_MassFailHigh",
    #     "1tag0pfat0pjet_0ptv_1lep_CR_MassFailHigh",
    #     "2tag0pfat0pjet_0ptv_1lep_CR_MassFailHigh"
    # ]

    # 2 lepton
    var = "METMod"
    # regions = [
    #     "0tag1pfat0pjet_0ptv_2lep_CR_MassPass",
    #     "1tag1pfat0pjet_0ptv_2lep_CR_MassPass",
    #     "2tag1pfat0pjet_0ptv_2lep_CR_MassPass",
    #     "0tag0pfat0pjet_0ptv_2lep_CR_MassPass",
    #     "1tag0pfat0pjet_0ptv_2lep_CR_MassPass",
    #     "2tag0pfat0pjet_0ptv_2lep_CR_MassPass"
    # ]

    regions = [
        "0tag1pfat0pjet_0ptv_2lep_CR_MassFailHigh",
        "1tag1pfat0pjet_0ptv_2lep_CR_MassFailHigh",
        "2tag1pfat0pjet_0ptv_2lep_CR_MassFailHigh",
        "0tag0pfat0pjet_0ptv_2lep_CR_MassFailHigh",
        "1tag0pfat0pjet_0ptv_2lep_CR_MassFailHigh",
        "2tag0pfat0pjet_0ptv_2lep_CR_MassFailHigh"
    ]

    backgrounds = [
        ['ttbar', ['ttbar']],
        ['diboson', ['WW', 'WZ', 'ZZ']],
        ['single top', ['stops', 'stopt', 'stopWt']],
        ['multijet', ['multijet0mergedMassPass', 'multijet1mergedMassPass', 'multijet2mergedMassPass', 'multijet0resolvedMassPass', 'multijet1resolvedMassPass', 'multijet2resolvedMassPass', 'multijet0mergedMassFail', 'multijet1mergedMassFail', 'multijet2mergedMassFail', 'multijet0resolvedMassFail', 'multijet1resolvedMassFail', 'multijet2resolvedMassFail']],
        ['W + jets', ['Wl', 'Wcl', 'Wcc', 'Wbb', 'Wbl', 'Wbc']],
        ['Z + jets', ['Zl', 'Zcl', 'Zcc', 'Zbb', 'Zbl', 'Zbc']]
    ]

    for name, background in backgrounds:
        ratio = 0.
        summedyield_prefit = 0.
        summedyield_postfit = 0.
        summedsigma_postfit = 0.
        for region in regions:
            y_prefit, e = getSummedBackground(f, background, region, var)
            summedyield_prefit += y_prefit

            # no multijet in control regions
            if 'multijet' in name and 'CR' in region:
                continue

            # is this shitty and hacky code? without a doubt yes.
            bg = background
            if background == ['WW', 'WZ', 'ZZ']:
                bg = ['diboson']
            if background == ['stops', 'stopt', 'stopWt']:
                bg = ['stop']
            if name == 'multijet':
                bg = ['multijet']
            if background == ['Wl', 'Wcl', 'Wcc', 'Wbb', 'Wbl', 'Wbc']:
                bg = ['Wl', 'Wcl', 'Whf']
            if background == ['Zl', 'Zcl', 'Zcc', 'Zbb', 'Zbl', 'Zbc']:
                bg = ['Zl', 'Zcl', 'Zhf']

            y_postfit, e_postfit = getSumForBackgrounds(data, bg, [region])
            summedyield_postfit += y_postfit
            summedsigma_postfit += e_postfit * e_postfit
            ratio_in_region = -1.
            try:
                ratio_in_region = (y_postfit - y_prefit) / e_postfit
            except Exception:
                print("no prefit")
            print("{name}: {region} -> {ratio:.2f}  \n\t((postfit: {postfit:.2f} - prefit: {prefit:.2f}) / sigma_postfit: {sigma:.2f})".format(name=name, region=region, ratio=ratio_in_region, postfit=y_postfit, prefit=y_prefit, sigma=e_postfit))

        if summedsigma_postfit == 0:
            continue
        summedsigma_postfit = math.sqrt(summedsigma_postfit)
        ratio = (summedyield_postfit - summedyield_prefit) / summedsigma_postfit
        print("{name}: sum of regions: {ratio:.2f}  \n\t((postfit: {postfit:.2f} - prefit: {prefit:.2f}) / sigma_postfit: {sigma:.2f})\n".format(name=name, ratio=ratio, postfit=summedyield_postfit, prefit=summedyield_prefit, sigma=summedsigma_postfit))


if __name__ == '__main__':
    main()
