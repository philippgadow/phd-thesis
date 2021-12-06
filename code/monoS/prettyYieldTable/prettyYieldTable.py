#!/bin/env python
from argparse import ArgumentParser
import csv
import numpy as np


def getArgs():
    parser = ArgumentParser()
    parser.add_argument('inputFile', help="Csv file containing yields")
    parser.add_argument('--outputFile', default="yield_table.tex", help="path to output file")
    parser.add_argument('-r', '--region', default="SR", help="Choose SR, CR1, CR2")
    return parser.parse_args()


def printHeader(outFile, region="signal region"):
    """Print the header of the table."""
    header = r"""\begin{table*}[h]
{
\caption{
Numbers of expected background events for each background process after the profile likelihood fit, the sum of all background components after the fit, and observed data yields for events with two $b$-tags in the resolved and merged channels for each \MET region. The multijet background in the two highest-\MET regions is negligible and not included in the fit.  Statistical and systematic uncertainties are combined. The uncertainties in the total background take into account the correlation of systematic uncertainties among different background processes. The uncertainties on the total background can be smaller than those on individual components due to anti-correlations of nuisance parameters. The expected signal for a \zhdm model with $(\mZp,\mA)=(1.4~\TeV,0.6~\TeV)$  for $\tan{\beta} = 1$, \gZp$=0.8$, and $\mchi=100\,\gev$, assuming a production cross-section of \sxsec~fb, is also shown.
\label{tab:yields_2tag}
}
%\footnotesize
\begin{center}
\begin{tabular}{l%
S[table-format=5.1, table-number-alignment=right, round-mode=figures, round-precision=3]@{$\,\pm\,$}
S[table-format=3.1, table-number-alignment=right, round-mode=figures, round-precision=2]@{\quad}
S[table-format=5.1, table-number-alignment=right, round-mode=figures, round-precision=3]@{$\,\pm\,$}
S[table-format=3.1, table-number-alignment=right, round-mode=figures, round-precision=2]@{}
S[table-format=4.1, table-number-alignment=right, round-mode=figures, round-precision=3]@{$\,\pm\,$}
S[table-format=3.1, table-number-alignment=right, round-mode=figures, round-precision=2]@{\quad}
S[table-format=3.2, table-number-alignment=right, round-mode=figures, round-precision=3]@{$\,\pm\,$}
S[table-format=3.2, table-number-alignment=right, round-mode=figures, round-precision=2]@{\quad}}
\hline
\hline
\multirow{2}{*}{Category} & \multicolumn{8}{c}{Range in \met [GeV]} \\ \cline{2-9}
& \multicolumn{2}{c}{$[150,200)$} & \multicolumn{2}{c}{$[200,350)$} & \multicolumn{2}{c}{$[350,500)$} & \multicolumn{2}{c}{$[500,\infty)$}\\
\hline
"""
    print(header)
    outFile.write(header)


def printFooter(outFile):
    """Print the footer of the table."""
    footer = r"""% Signal event yield per bin (2 b-tags):
% 0.308869 5.77574 17.7472 16.4493
% old numbers
% 0.39 7.30 22.43 20.079
\hline
\hline
\end{tabular}
\end{center}
}
\end{table*}

"""
    print(footer)
    outFile.write(footer)


def parseRegion(region, analysisregion='SR'):
    if analysisregion == 'SR':
        if region == 0:
            return "Region_BMax200_BMin150_incFat1_Fat0_incJet1_J2_T2_L0_Y2015_distmBB_DSR"
        if region == 1:
            return "Region_BMax350_BMin200_incFat1_Fat0_incJet1_J2_T2_L0_Y2015_distmBB_DSR"
        if region == 2:
            return "Region_BMax500_BMin350_incFat1_Fat0_incJet1_J2_T2_L0_Y2015_distmBB_DSR"
        if region == 3:
            return "Region_BMin500_incFat1_Fat1_incJet1_J0_T2_L0_Y2015_distmBB_DSR"
    elif analysisregion == 'CR1':
        if region == 0:
            return "Region_BMax200_BMin150_incFat1_Fat0_incJet1_J2_T2_L1_Y2015_distCharge_DCR1"
        if region == 1:
            return "Region_BMax350_BMin200_incFat1_Fat0_incJet1_J2_T2_L1_Y2015_distCharge_DCR1"
        if region == 2:
            return "Region_BMax500_BMin350_incFat1_Fat0_incJet1_J2_T2_L1_Y2015_distCharge_DCR1"
        if region == 3:
            return "Region_BMin500_incFat1_Fat1_incJet1_J0_T2_L1_Y2015_distCharge_DCR1"
    elif analysisregion == 'CR2':
        if region == 0:
            return "Region_BMax200_BMin150_incFat1_Fat0_incJet1_J2_T2_L2_Y2015_distmBB_DCR2"
        if region == 1:
            return "Region_BMax350_BMin200_incFat1_Fat0_incJet1_J2_T2_L2_Y2015_distmBB_DCR2"
        if region == 2:
            return "Region_BMax500_BMin350_incFat1_Fat0_incJet1_J2_T2_L2_Y2015_distmBB_DCR2"
        if region == 3:
            return "Region_BMin500_incFat1_Fat1_incJet1_J0_T2_L2_Y2015_distmBB_DCR2"
    return ""


def parseName(name):
    if name == 'ttbar':
        return '$t\\bar{t}$'
    elif name == 'diboson':
        return 'Diboson'
    elif name == 'stop':
        return 'Single top-quark'
    elif name == 'Signal':
        return 'Vector model, \\\\$m_{\chi}=$1~GeV, \\\\$m_{\\textrm{med}}=$600~GeV'
    return name.capitalize()


def sumBackgrounds(data, backgrounds, name, region):
    """Sum different flavours for V+jets processes."""
    values = np.array([0., 0., 0., 0.])
    errors = np.array([0., 0., 0., 0.])
    for bg in backgrounds:
        values += np.array([data[bg][parseRegion(i, region)][0] for i in range(0, 4)])
        errors += np.array([(data[bg][parseRegion(i, region)][1]**2) for i in range(0, 4)])
    errors = np.sqrt(errors)

    if True:
        line = "{name} & {v_r150200} & {e_r150200} & {v_r200350} & {e_r200350} & {v_r350500} & {e_r350500} & {v_m500} & {e_m500} \\\\\n".format(
               name=name,
               v_r150200=round(values[0], 2), e_r150200=round(errors[0], 2),
               v_r200350=round(values[1], 2), e_r200350=round(errors[1], 2),
               v_r350500=round(values[2], 2), e_r350500=round(errors[2], 2),
               v_m500=round(values[3], 2), e_m500=round(errors[3], 2))

    return line

def printBody(outFile, data, region='SR'):
    """Print individual line of the table."""
    line = ""

    # separator
    line += '\midrule\\\\\n'

    # sum W+jets
    line += sumBackgrounds(data, ['Wl', 'Wcl', 'Whf'], '$W$+jets', region)

    # sum Z+jets
    line += sumBackgrounds(data, ['Zl', 'Zcl', 'Zhf'], '$Z$+jets', region)

     # ttbar and single top
    line += sumBackgrounds(data, ['ttbar', 'stop'], '$t\\bar{t}$ + single top quark', region)

    # other backgrounds
    for bg in ['diboson', 'VHbb']:
        if True:
            line += "{name} & {v_r150200} & {e_r150200} & {v_r200350} & {e_r200350} & {v_r350500} & {e_r350500} & {v_m500} & {e_m500} \\\\\n".format(
                name=parseName(bg),
                v_r150200=round(data[bg][parseRegion(0, region)][0], 2), e_r150200=round(data[bg][parseRegion(0, region)][1], 2),
                v_r200350=round(data[bg][parseRegion(1, region)][0], 2), e_r200350=round(data[bg][parseRegion(1, region)][1], 2),
                v_r350500=round(data[bg][parseRegion(2, region)][0], 2), e_r350500=round(data[bg][parseRegion(2, region)][1], 2),
                v_m500=round(data[bg][parseRegion(3, region)][0], 2), e_m500=round(data[bg][parseRegion(3, region)][1], 2))

    # separator
    line += '\midrule\\\\\n'

    # summed background
    for item in ['Bkg']:
        if True:
            line += "{name} & {v_r150200} & {e_r150200} & {v_r200350} & {e_r200350} & {v_r350500} & {e_r350500} & {v_m500} & {e_m500} \\\\\n".format(
                name=parseName(item),
                v_r150200=round(data[item][parseRegion(0, region)][0], 2), e_r150200=round(data[item][parseRegion(0, region)][1], 2),
                v_r200350=round(data[item][parseRegion(1, region)][0], 2), e_r200350=round(data[item][parseRegion(1, region)][1], 2),
                v_r350500=round(data[item][parseRegion(2, region)][0], 2), e_r350500=round(data[item][parseRegion(2, region)][1], 2),
                v_m500=round(data[item][parseRegion(3, region)][0], 2), e_m500=round(data[item][parseRegion(3, region)][1], 2))

    # data
    for item in ['data']:
        if True:
            line += "{name} & {v_r150200} &  & {v_r200350} &  & {v_r350500} &  & {v_m500} &  \\\\\n".format(
                name=parseName(item),
                v_r150200=round(data[item][parseRegion(0, region)][0], 2),
                v_r200350=round(data[item][parseRegion(1, region)][0], 2),
                v_r350500=round(data[item][parseRegion(2, region)][0], 2),
                v_m500=round(data[item][parseRegion(3, region)][0], 2))


    print(line)
    outFile.write(line)


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


def main():
    """This function prints out a beatiful LaTeX table with background+signal yields and data both to the screen and to a file."""
    args = getArgs()

    # input file
    data = readData(args.inputFile)

    # output file
    outFile = open(args.outputFile, 'w')

    # create table
    printHeader(outFile)
    printBody(outFile, data, args.region)
    printFooter(outFile)

    outFile.close()


if __name__ == '__main__':
    main()
