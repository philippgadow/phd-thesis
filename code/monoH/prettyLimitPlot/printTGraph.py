from argparse import ArgumentParser
from rootpy.io import root_open
from ROOT import Double
def getArgs():
    """Get arguments from command line."""
    parser = ArgumentParser()
    parser.add_argument('inputFile', help='Input ROOT file containing TGraphs.')
    parser.add_argument('-o', '--outputFile', default='output_tgraph_dump.csv', help='Name of output file')
    parser.add_argument('-n', '--name', default='expected', help='Name of TGraph you want to inspect.')
    parser.add_argument('-x', '--varX', default='m_Mediator', help='Name of the x-variable column in the output file.')
    parser.add_argument('-y', '--varY', default='m_DarkMatter', help='Name of y-variable column in the output file.')
    return parser.parse_args()


def main():
    """Print out the points of a certain TGraph in a ROOT file."""
    args = getArgs()
    points = []

    with root_open(args.inputFile) as f:
        graph = None
        try:
            graph = getattr(f, args.name)
        except Exception:
            print("Oops, something went wrong when accessing TGraph {name} in file {file}.".format(name=args.name, file=args.inputFile))

        if not graph:
            print("Oops, we did not get a graph. Exiting now without any work done.")
            return


        # parsing out the points of the TGraph. How this can be achieved is documented here: https://root.cern.ch/doc/master/classTGraph.html
        x = Double()
        y = Double()
        
        for i in range(graph.GetN()):
            graph.GetPoint(i, x, y)
            print('graph point i={i}: \tx={x}\t\ty={y}'.format(i=i, x=x, y=y))
            points.append([float(x),float(y)])


    # write to file
    with open(args.outputFile, 'w') as output:
        output.write("{varX},{varY}\n".format(varX=args.varX,varY=args.varY))

        for point in reversed(points):
            output.write("{x},{y}\n".format(x=point[0], y=point[1]))



if __name__ == '__main__':
    main()