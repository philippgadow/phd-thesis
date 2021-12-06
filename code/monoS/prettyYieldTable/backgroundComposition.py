#!/bin/env python
from argparse import ArgumentParser
import csv
import matplotlib
import matplotlib.pyplot as plt


def getArgs():
    parser = ArgumentParser()
    parser.add_argument('inputFile', help="Csv file containing yields")
    return parser.parse_args()


def parseRegion(region):
    if region == 0:
        return "Region_BMin500_incFat1_Fat1_incJet1_Y2015_D0lep_T0_L0_distmWW_J1"
    if region == 1:
        return "Region_distmWW_J1_L0_T0_D0lep_Y2015_incJet1_Fat1_incFat1_BMin300_BMax500"
    if region == 2:
        return "Region_BMin200_incFat1_Fat0_incJet1_Y2015_D0lep_T0_L0_distmWW_J2"
    return ""


# def parseRegion(region):
#     if region == 0:
#         return "Region_BMin500_incFat1_Fat1_incJet1_Y2015_D1lep_T0_L1_distmWW_J1"
#     if region == 1:
#         return "Region_distmWW_J1_L1_T0_D1lep_Y2015_incJet1_Fat1_incFat1_BMin300_BMax500"
#     if region == 2:
#         return "Region_BMin200_incFat1_Fat0_incJet1_Y2015_D1lep_T0_L1_distmWW_J2"
#     return ""


# def parseRegion(region):
#     if region == 0:
#         return "Region_BMin500_incFat1_Fat1_incJet1_Y2015_D2lep_T0_L2_distmWW_J1"
#     if region == 1:
#         return "Region_distmWW_J1_L2_T0_D2lep_Y2015_incJet1_Fat1_incFat1_BMin300_BMax500"
#     if region == 2:
#         return "Region_BMin200_incFat1_Fat0_incJet1_Y2015_D2lep_T0_L2_distmWW_J2"
#     return ""


def getSumForBackgrounds(data, backgrounds, region='all'):
    """Sum different flavours for V+jets processes."""
    evt_yield = 0.
    for bg in backgrounds:
        if region == 'all':
            for i in range(0, 3):
                try:
                    evt_yield += data[bg][parseRegion(i)][0]
                except KeyError:
                    evt_yield += 0.
        else:
            try:
                evt_yield += data[bg][parseRegion(region)][0]
            except KeyError:
                evt_yield += 0.
    return evt_yield


def getSumForBackground(data, bg, region='all'):
    """Print number of events for a certain background."""
    evt_yield = 0.
    if region == 'all':
        for i in range(0, 3):
            try:
                evt_yield += data[bg][parseRegion(i)][0]
            except KeyError:
                evt_yield += 0.
    else:
        try:
            evt_yield += data[bg][parseRegion(region)][0]
        except KeyError:
            evt_yield += 0.
    return evt_yield


def readData(inputFile):
    """Read data from csv file."""
    data = {}
    with open(inputFile, 'r') as csvfile:
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


def makePlot(data):
    """Make bar graph showing background composition."""

    regions = ['all', 0, 1, 2]
    for region in regions:
        ttbar = getSumForBackgrounds(data, ['ttbar', 'stop'], region)
        diboson = getSumForBackground(data, 'diboson', region)
        stop = getSumForBackground(data, 'stop', region)
        wjets = getSumForBackground(data, 'wjets', region)
        zjets = getSumForBackground(data, 'zjets', region)
        vhbb = getSumForBackground(data, 'VHbb', region)

        # create plot
        # font size
        matplotlib.rcParams.update({'font.size': 23})
        fig, ax = plt.subplots(figsize=(8,6))
        labels = ['$W$ + jets', 'Diboson', '$Z$ + jets', '$t\overline{t}$ + t', '']
        # labels = ['$W$ + jets', 'Diboson', '', '$t\overline{t}$ + t', '']
        # labels = ['', 'Diboson', '$Z$ + jets', '', '']
        sizes = [wjets, diboson, zjets, ttbar, vhbb]

        print(sizes)

        # colors
        col_wjets = '#75fbfd'
        col_dibsoson = '#f19d38'
        col_zjets = '#fffe54'
        col_ttbar = '#75fa4c'
        col_vhbb = '#bf6ef7'
        colors = [col_wjets, col_dibsoson, col_zjets, col_ttbar, col_vhbb]

        # explosion
        explode = (0.05, 0.05, 0.05, 0.05, 0.05)

        # dynamic labelling
        def my_autopct(pct):
            return ('%1.0f%%' % pct) if pct > 3 else ''
            # return ''
        plt.pie(sizes, colors=colors, labels=labels, autopct=my_autopct, startangle=90, pctdistance=0.59, explode=explode)

        # draw circle
        # centre_circle = plt.Circle((0, 0), 0.82, fc='white')
        centre_circle = plt.Circle((0, 0), 0.4, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)

        # Equal aspect ratio ensures that pie is drawn as a circle
        ax.axis('equal')
        # plt.tight_layout()

        fig.savefig('bkg_comp_{region}.eps'.format(region=region))


def main():
    """This function creates a graphic (i.e. bar diagram) that shows the background composition of the search in all regions."""
    # get arguments from command line
    args = getArgs()

    # input file
    data = readData(args.inputFile)

    # make graph
    makePlot(data)


if __name__ == '__main__':
    main()
