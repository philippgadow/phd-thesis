import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser

# ATLAS style
import atlas_mpl_style as ampl
ampl.use_atlas_style()


def getArgumentParser():
    parser = ArgumentParser()
    parser.add_argument('database', default="data/CWdatabase/test/RPhiCoincidenceMap.A1.mod2a.v0025._12.db", help="Path to database file.")
    parser.add_argument('--pt', type=int, choices=[1,2,3,4,5,6], default=1, help="Pt threshold (1: L1MU4, 2: L1MU6, 3: L1MU10, 4: L1MU11, 5: L1MU15, 6: L1MU20).")
    parser.add_argument('--roi', type=int, default=0, help="Region of Interest")
    parser.add_argument('--module', type=int, default=2, help="Module")
    return parser


# hard-coded parameters about length of coincidence windows
len_dR = 31
len_dPhi = 15


class CWMap(object):
    """Implementation of coincidence window (CW) map, including methods for visualisation."""
    def __init__(self, dR_start, dR_end, dPhi_start, dPhi_end):
        self.dR_start = dR_start
        self.dR_end = dR_end
        self.dPhi_start = dPhi_start
        self.dPhi_end = dPhi_end

        # find type of CW
        self.type = None
        if (self.dR_end - self.dR_start + 1) == 31 and self.dPhi_end - self.dPhi_start + 1 == 15:
            self.type = 'HH'
        elif (self.dR_end - self.dR_start + 1) == 31 and self.dPhi_end - self.dPhi_start + 1 == 7:
            self.type = 'HL'
        elif (self.dR_end - self.dR_start + 1) == 15 and self.dPhi_end - self.dPhi_start + 1 == 15:
            self.type = 'LH'
        elif (self.dR_end - self.dR_start + 1) == 15 and self.dPhi_end - self.dPhi_start + 1 == 7:
            self.type = 'LL'

        self.map = np.zeros((len_dR, len_dPhi), dtype=np.int8)

    def fillMap(self, line):
        line = line.split()
        for i, entry in enumerate(line):
            entry = "{0:015b}".format(int(entry))
            for j, result in enumerate(entry):
                self.map[i][j] = result


class DatabaseEntry(CWMap):
    """Entry in database created from CWMap object."""
    def __init__(self, lines):
        # read lines
        line = lines[0].split()
        if not (line[0] == '#' and len(line) == 8):
            raise Exception
        # fill database entry information
        self.pt = int(line[1])
        self.ROI = int(line[2])
        self.module = int(line[3])

        # fill CW information
        dR_start = int(line[4])
        dR_end = int(line[5])
        dPhi_start = int(line[6])
        dPhi_end = int(line[7])
        super(DatabaseEntry, self).__init__(dR_start, dR_end, dPhi_start, dPhi_end)
        self.fillMap(lines[1])

    def plotMap(self):
        fig, ax = plt.subplots(figsize=(6,8))
        plot = ax.imshow(self.map, cmap='gist_gray', vmin=0., vmax=1.)
        plt.title('module {}, ROI {}, pT {}, CW: {}'.format(self.module, self.ROI, self.pt, self.type))
        plt.xlabel('$\Delta \phi$')
        plt.ylabel('$\Delta r$')
        plt.xticks(range(len_dPhi), range(-int(0.5 * len_dPhi - 0.5), int(0.5 * len_dPhi + 0.5)))
        plt.yticks(range(len_dR), range(-int(0.5 * len_dR - 0.5), int(0.5 * len_dR + 0.5)))
        cbar = plt.colorbar(plot, ticks=[0, 1])
        cbar.ax.set_yticklabels(['fail', 'pass'])

        fig.savefig('cwplot_module{module}_roi{roi}_pt{pt}_cw{cw}.pdf'.format(
            module=self.module, roi=self.ROI, pt=self.pt, cw=self.type))


class Database(object):
    """Database for L1 muon trigger coincidence windows. Must be initialised with file name holding
       database information in text format."""
    def readFile(self):
        with open(self.filename, 'r') as f:
            while True:
                line1 = f.readline().replace('\n', '')
                line2 = f.readline().replace('\n', '')
                if not line2:
                    break  # EOF

                lines = [line1, line2]
                dbEntry = DatabaseEntry(lines)
                pt = dbEntry.pt
                ROI = dbEntry.ROI
                module = dbEntry.module
                CW = dbEntry.type
                self.database[(pt, ROI, module, CW)] = dbEntry

    def __init__(self, filename):
        super(Database, self).__init__()
        self.filename = filename
        self.database = {}

        self.readFile()



def main():
    args = getArgumentParser().parse_args()
    # 'RPhiCoincidenceMap.A1.mod2a.v0028._12.db'
    db = Database(args.database)

    # arguments
    pt = args.pt
    ROI = args.roi
    module = args.module

    for CW in ['HH', 'HL', 'LH', 'LL']:
        db.database[(pt, ROI, module, CW)].plotMap()


if __name__ == '__main__':
    main()
