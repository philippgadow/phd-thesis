import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
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
    simulated = simulated[simulated.mzp != 10000]

    ax.scatter(simulated['mzp'], simulated['mdm'], color="blue", label="Generated signal model sample points")
    if showInterpolation:
        ax.scatter(interpolated['mzp'], interpolated['mdm'], color="orange", label="Interpolated points")
    plt.xlabel("$m_{Z'}$ [GeV]")
    plt.ylabel("$m_{\\chi}$ [GeV]")

    # plot mass diagonal
    x = np.linspace(0, 2200, 2)
    y = 0.5 * x
    ax.plot(x, y, 'k-.', color='#999999')
    ax.text(0.45, 0.515, "$m_{Z'}$ = $2 \cdot m_{\chi}$",
              verticalalignment='center', horizontalalignment='center',
              transform=ax.transAxes, color='#999999', rotation=35, fontsize=16)

    ax.text(0.7, 0.25, "on-shell",
              verticalalignment='center', horizontalalignment='center',
              transform=ax.transAxes, color='#999999', fontsize=16)

    ax.text(0.25, 0.7, "off-shell",
              verticalalignment='center', horizontalalignment='center',
              transform=ax.transAxes, color='#999999', fontsize=16)

    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1,
                     box.width, box.height * 0.9])

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15),
              frameon=False, ncol=5)
    ax.ticklabel_format(style='plain')
    # ax.set_xscale('log')
    ax.set_xlim([-50,2200])
    ax.set_ylim([-25,1100])

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
