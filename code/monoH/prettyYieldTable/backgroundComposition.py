#!/bin/env python
from argparse import ArgumentParser
import csv
import matplotlib
import matplotlib.pyplot as plt
# from rootpy.plotting.style import set_style


def getArgs():
    parser = ArgumentParser()
    parser.add_argument('inputFile', help="Csv file containing yields")
    return parser.parse_args()


def parseRegion(region):
    if region == 0:
        return "Region_BMax200_BMin150_incFat1_Fat0_incJet1_J2_T2_L0_Y2015_distmBB_DSR"
    if region == 1:
        return "Region_BMax350_BMin200_incFat1_Fat0_incJet1_J2_T2_L0_Y2015_distmBB_DSR"
    if region == 2:
        return "Region_BMax500_BMin350_incFat1_Fat0_incJet1_J2_T2_L0_Y2015_distmBB_DSR"
    if region == 3:
        return "Region_BMin500_incFat1_Fat1_incJet1_J0_T2_L0_Y2015_distmBB_DSR"
    return ""


# def parseRegion(region):
#     if region == 0:
#         return "Region_BMax200_BMin150_incFat1_Fat0_incJet1_J2_T2_L1_Y2015_distCharge_DCR1"
#     if region == 1:
#         return "Region_BMax350_BMin200_incFat1_Fat0_incJet1_J2_T2_L1_Y2015_distCharge_DCR1"
#     if region == 2:
#         return "Region_BMax500_BMin350_incFat1_Fat0_incJet1_J2_T2_L1_Y2015_distCharge_DCR1"
#     if region == 3:
#         return "Region_BMin500_incFat1_Fat1_incJet1_J0_T2_L1_Y2015_distCharge_DCR1"
#     return ""


# def parseRegion(region):
#     if region == 0:
#         return "Region_BMax200_BMin150_incFat1_Fat0_incJet1_J2_T2_L2_Y2015_distmBB_DCR2"
#     if region == 1:
#         return "Region_BMax350_BMin200_incFat1_Fat0_incJet1_J2_T2_L2_Y2015_distmBB_DCR2"
#     if region == 2:
#         return "Region_BMax500_BMin350_incFat1_Fat0_incJet1_J2_T2_L2_Y2015_distmBB_DCR2"
#     if region == 3:
#         return "Region_BMin500_incFat1_Fat1_incJet1_J0_T2_L2_Y2015_distmBB_DCR2"
#     return ""

def getSumForBackgrounds(data, backgrounds, region='all'):
    """Sum different flavours for V+jets processes."""
    evt_yield = 0.
    for bg in backgrounds:
        if region == 'all':
            for i in range(0, 4):
                evt_yield += data[bg][parseRegion(i)][0]
        else:
            evt_yield += data[bg][parseRegion(region)][0]
    return evt_yield


def getSumForBackground(data, bg, region='all'):
    """Print number of events for a certain background."""
    evt_yield = 0.
    if region == 'all':
        for i in range(0, 4):
            evt_yield += data[bg][parseRegion(i)][0]
    else:
        evt_yield += data[bg][parseRegion(region)][0]
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

    regions = ['all', 0, 1, 2, 3]
    for region in regions:
        ttbar = getSumForBackgrounds(data, ['ttbar', 'stop'], region)
        diboson = getSumForBackground(data, 'diboson', region)
        stop = getSumForBackground(data, 'stop', region)
        wjets = getSumForBackgrounds(data, ['Wl', 'Wcl', 'Whf'], region)
        zjets = getSumForBackgrounds(data, ['Zl', 'Zcl', 'Zhf'], region)
        vhbb = getSumForBackground(data, 'VHbb', region)

        # create plot
        # font size
        matplotlib.rcParams.update({'font.size': 23})
        fig, ax = plt.subplots(figsize=(8,6))
        labels = ['$W$ + jets', 'Diboson', '$Z$ + jets', '$t\overline{t}$ + t', '$Vh$(bb)']

        # labels = ['$W$ + jets', '', '', '$t\overline{t}$ + t', '']
        # labels = ['$W$ + jets', 'Diboson', '', '$t\overline{t}$ + t', '$Vh$(bb)']

        # labels = ['', 'Diboson', '$Z$ + jets', '$t\overline{t}$ + t', '']
        # labels = ['', 'Diboson', '$Z$ + jets', '', '$Vh$(bb)']

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
            return ('%1.0f%%' % pct) if pct > 6 else ''
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
        fig.savefig('bkg_comp_{region}.eps'.format(region=region))


def main():
    """This function creates a graphic (i.e. bar diagram) that shows the background composition of the search in all regions."""
    # get arguments from command line
    args = getArgs()

    # plotting style
    # set_style('ATLAS', mpl=True)

    # input file
    data = readData(args.inputFile)

    # make graph
    makePlot(data)


if __name__ == '__main__':
    main()
