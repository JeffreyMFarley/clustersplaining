from swatch import Swatch
from page import Page
from operator import attrgetter
from hew import KMeans, KDTree
from hew.structures.vector import distance_euclid_squared
import argparse


class Clusters(Page):
    def __init__(self, **kwargs):
        self.k = kwargs['k']
        self.nearest = kwargs['nearest']
        self.hsl = kwargs['hsl']
        self.steps = kwargs['steps']

        if self.hsl:
            self.valueAttrs = ['hue', 'saturation', 'light']
        else:
            self.valueAttrs = ['red', 'green', 'blue']

    def _toRgb(self, vector):
        import colorsys

        if self.hsl:
            h = vector[0] / 100
            s = vector[1] / 100
            v = 256 * vector[2] / 100
            vector = colorsys.hsv_to_rgb(h, s, v)

        return [int(vector[0]), int(vector[1]), int(vector[2])]

    def onCanvas(self):
        for i, members in enumerate(self.clusters.groups):
            rgb = self.palette[i].rgb
            for member in members:
                sw = Swatch(self._toRgb(member))
                self.addClustered(rgb, sw)

    def onLegend(self):
        for sw in sorted(self.palette, key=attrgetter(*self.valueAttrs)):
            self.addLegend(sw.name, sw.rgb)

    def calculate(self):
        distance_fn = distance_euclid_squared
        swatches = list(Swatch.acquire())
        ranged = self.valueAttrs
        labels = ['name']

        print('Calculating {0} clusters'.format(self.k))
        self.clusters = KMeans.fromTable(self.k, swatches, ranged, distance_fn)

        # Convert cluster centroids to palette swatches
        self.palette = []
        if self.nearest:
            print('Building nearest neighbor tree')
            tree = KDTree.fromTable(swatches, ranged, labels)

            for centroid in self.clusters.MU:
                rgb, name, _ = tree.nearest_neighbor(centroid)
                colors = self._toRgb(rgb)
                self.palette.append(Swatch(colors, name[0]))

        else:
            for centroid in self.clusters.MU:
                colors = self._toRgb(centroid)
                name = '#{0:02x}{1:02x}{2:02x}'.format(*colors)
                self.palette.append(Swatch(colors, name))

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def buildArgParser():
    description = 'Demonstrate k-Means using Behr colors'
    p = argparse.ArgumentParser(description=description)
    p.add_argument('-k', '--clusters',
                   type=int, dest='k', default=8,
                   help='the number of clusters to create (default: 8)')
    p.add_argument('-n', '--use-nearest',
                   action='store_true', dest='nearest', default=False,
                   help='cluster colors come from the input set')
    p.add_argument('-s', '--show-steps',
                   action='store_true', dest='steps', default=False,
                   help='indicate the steps in the cluster calculation')
    p.add_argument('--use-hsl',
                   action='store_true', dest='hsl', default=False,
                   help='use HSL not RGB for cluster calc')
    p.add_argument('--trial',
                   metavar='NAME', dest='trial', required=False,
                   help='identify a cluster run')

    return p


def buildPathName(args):
    fileName = 'cluster-{0}'.format(args.k)

    if args.hsl:
        fileName += '-hsl'

    if args.nearest:
        fileName += '-nearest'

    if args.trial:
        fileName += '-' + args.trial

    return 'cel/{0}.html'.format(fileName)


def buildTitle(args):
    title = '{0} color palette'.format(args.k)

    if args.nearest:
        title += ' using original colors'

    if args.hsl:
        title += ' clustered in HSL'

    return title


if __name__ == '__main__':
    parser = buildArgParser()
    args = parser.parse_args()

    pathName = buildPathName(args)
    title = buildTitle(args)

    p = Clusters(**vars(args))
    p.calculate()
    p.render(pathName, title)
