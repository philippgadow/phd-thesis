#!/bin/env python
import csv
import math
from argparse import ArgumentParser


def getArgs():
    """Get arguments from command line."""
    parser = ArgumentParser()
    parser.add_argument("inputFilePostFit")
    parser.add_argument("inputFilePreFit")

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


def getSumForBackgrounds(data, backgrounds, regions):
    """Sum different flavours for V+jets processes."""
    evt_yield = 0.
    for bg in backgrounds:
        for r in regions:
            evt_yield += data[bg][r][0]
    return evt_yield


def main():
    """For a group of background physics processes iterate over specified histograms in ROOT input file and print out LaTeX table with yield and statistical uncertainty."""

    args = getArgs()
    data_postfit = readData(args.inputFilePostFit)
    data_prefit = readData(args.inputFilePreFit)

    r = ""

    regions = [
        "Region_BMax200_BMin150_incFat1_Fat0_incJet1_J2_T2_L0_Y2015_distmBB_DSR",
        "Region_BMax350_BMin200_incFat1_Fat0_incJet1_J2_T2_L0_Y2015_distmBB_DSR",
        "Region_BMax500_BMin350_incFat1_Fat0_incJet1_J2_T2_L0_Y2015_distmBB_DSR",
        "Region_BMin500_incFat1_Fat1_incJet1_J0_T2_L0_Y2015_distmBB_DSR"
        # "Region_BMax200_BMin150_incFat1_Fat0_incJet1_J2_T2_L1_Y2015_distCharge_DCR1",
        # "Region_BMax350_BMin200_incFat1_Fat0_incJet1_J2_T2_L1_Y2015_distCharge_DCR1",
        # "Region_BMax500_BMin350_incFat1_Fat0_incJet1_J2_T2_L1_Y2015_distCharge_DCR1",
        # "Region_BMin500_incFat1_Fat1_incJet1_J0_T2_L1_Y2015_distCharge_DCR1",
        # "Region_BMax200_BMin150_incFat1_Fat0_incJet1_J2_T2_L2_Y2015_distmBB_DCR2",
        # "Region_BMax350_BMin200_incFat1_Fat0_incJet1_J2_T2_L2_Y2015_distmBB_DCR2",
        # "Region_BMax500_BMin350_incFat1_Fat0_incJet1_J2_T2_L2_Y2015_distmBB_DCR2",
        # "Region_BMin500_incFat1_Fat1_incJet1_J0_T2_L2_Y2015_distmBB_DCR2"
    ]

    backgrounds = [
        ['ttbar + single top', ['ttbar', 'stop']],
        ['diboson', ['diboson']],
        ['W + jets', ['Wl', 'Wcl', 'Whf']],
        ['Z + jets', ['Zl', 'Zcl', 'Zhf']],
        ['VHbb', ['VHbb']]
    ]

    for name, background in backgrounds:
        ratio = 0.
        summedyield_prefit = 0.
        summedyield_postfit = 0.
        for region in regions:
            y_prefit = getSumForBackgrounds(data_prefit, background, [region])
            summedyield_prefit += y_prefit

            y_postfit = getSumForBackgrounds(data_postfit, background, [region])
            summedyield_postfit += y_postfit
            ratio_in_region = -1.
            try:
                ratio_in_region = y_postfit / y_prefit
            except Exception:
                print("no prefit")
            print("{name}: {region} -> {ratio:.2f}  (postfit: {postfit:.2f} / prefit: {prefit:.2f})".format(name=name, region=region, ratio=ratio_in_region, postfit=y_postfit, prefit=y_prefit))

        if summedyield_prefit == 0:
            continue

        ratio = summedyield_postfit / summedyield_prefit
        print("{name}: {ratio:.2f}  (postfit in \sum_all regions: {postfit:.2f} / prefit in \sum_SR: {prefit:.2f})".format(name=name, ratio=ratio, postfit=summedyield_postfit, prefit=summedyield_prefit))
        # print("{name}: {ratio:.2f}  (postfit in \sum_CR: {postfit:.2f} / prefit in \sum_CR: {prefit:.2f})".format(name=name, ratio=ratio, postfit=summedyield_postfit, prefit=summedyield_prefit))


if __name__ == '__main__':
    main()
