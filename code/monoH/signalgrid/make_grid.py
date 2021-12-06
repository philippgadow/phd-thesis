import matplotlib.pyplot as plt
import pandas as pd
from argparse import ArgumentParser
import atlas_mpl_style as ampl


def getArgumentParser():
    """Get arguments from command line."""
    parser = ArgumentParser()
    parser.add_argument("signalgrid", help="CSV file with signal grid information.")
    parser.add_argument("-o", "--outputFile", default="signalgrid.pdf", help="Output file with signal grid plot.")
    parser.add_argument("--showInterpolation", default=False, help="Include interpolated points in signal grid.")
    return parser


def makeSignalGrid(signalgrid, outputFile, showInterpolation):
    """Produce sketch of signal grid."""
    fig, ax = plt.subplots()
    simulated = signalgrid[signalgrid['simulated'] == 1]
    interpolated = signalgrid[signalgrid['simulated'] == 0]
    ax.scatter(simulated['mzp'], simulated['mA'], color="blue", label="Generated signal model sample points")
    if showInterpolation:
        ax.scatter(interpolated['mzp'], interpolated['mA'], color="orange", label="Interpolated points")
    plt.xlabel("$m_{Z'}$ [GeV]")
    plt.ylabel("$m_{A}$ [GeV]")

    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1,
                     box.width, box.height * 0.9])

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
              frameon=False, ncol=5)
    ax.ticklabel_format(style='plain')
    ax.set_ylim([0,1000])
    fig.savefig(outputFile)


def main():
    args = getArgumentParser().parse_args()
    # set style
    ampl.use_atlas_style()

    # make plot
    signalgrid = pd.read_csv(args.signalgrid)
    makeSignalGrid(signalgrid, args.outputFile, args.showInterpolation)


if __name__ == '__main__':
    main()
