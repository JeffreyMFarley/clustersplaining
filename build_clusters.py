from swatch import Swatch

# -----------------------------------------------------------------------------
# vector -> vector
# -----------------------------------------------------------------------------


def quantize(vector):
    return [int(x) for x in vector]


def toRgb(vector):
    import colorsys

    h = vector[0] / 100
    s = vector[1] / 100
    v = 256 * vector[2] / 100
    return quantize(colorsys.hsv_to_rgb(h, s, v))

# -----------------------------------------------------------------------------
# vector[] -> vector[]
# -----------------------------------------------------------------------------


def selectRandomCentroids(vectors, k):
    import random
    return random.sample(set(vectors), k)


def selectSatisfactoryCentroids(vectors, k, distance_fn):
    from hew.clusters.k_means import kmeans_plus_plus
    return kmeans_plus_plus(vectors, k, distance_fn)

# -----------------------------------------------------------------------------
# vector -> Swatch
# -----------------------------------------------------------------------------


def rgbToSwatch(vector):
    rgb = quantize(vector)
    name = '#{0:02x}{1:02x}{2:02x}'.format(*rgb)
    return Swatch(rgb, name)


def hslToSwatch(vector):
    rgb = toRgb(vector)
    name = '#{0:02x}{1:02x}{2:02x}'.format(*rgb)
    return Swatch(rgb, name)


def useNearest(swatches, tree):
    kvp = {sw.name: sw for sw in swatches}

    def curry(vector):
        _, name, _ = tree.nearest_neighbor(vector)
        return kvp[name[0]]
    return curry

# -----------------------------------------------------------------------------
# args -> string
# -----------------------------------------------------------------------------


def buildPathName(args):
    fileName = 'cluster-{0}'.format(args.k)

    if args.random:
        fileName += '-random'

    if args.hsl:
        fileName += '-hsl'

    if args.nearest:
        fileName += '-nearest'

    if args.trial:
        fileName += '-' + args.trial

    return 'cel/{0}.html'.format(fileName)


def buildTitle(args):
    title = '{0} color palette'.format(args.k)

    if args.random:
        title += ' random start'

    if args.nearest:
        title += ' using original colors'

    if args.hsl:
        title += ' clustered in HSL'

    return title

# -----------------------------------------------------------------------------
# Process
# -----------------------------------------------------------------------------


def run(args):
    from operator import attrgetter
    from display_clusters import Clusters
    from hew import KDTree, distance_fn
    from hew.clusters.k_means import lloyds_algorithm
    from hew.structures.vector import extractFloatVectors

    # get the swatches
    swatches = Swatch.orderedList()

    # extract the vectors
    if args.hsl:
        valueFields = ['hue', 'saturation', 'light']
    else:
        valueFields = ['red', 'green', 'blue']
    vectors = extractFloatVectors(swatches, valueFields)

    if args.nearest:
        print('Build nearest neighbor tree')
        tree = KDTree.fromTable(swatches, valueFields, ['name'])

    # determine the palette processing function
    toPalette = None
    if args.nearest:
        toPalette = useNearest(swatches, tree)
    elif args.hsl:
        toPalette = hslToSwatch
    else:
        toPalette = rgbToSwatch

    print('Select initial centroids')
    if args.random:
        MU0 = selectRandomCentroids(vectors, args.k)
    else:
        MU0 = selectSatisfactoryCentroids(vectors, args.k, distance_fn)

    print('Find the clusters')
    MU, clusterIndex, _ = lloyds_algorithm(vectors, MU0, distance_fn)

    print('Process the centroids')
    palette = list(map(toPalette, MU))

    print('Write HTML')
    pathName = buildPathName(args)
    title = buildTitle(args)
    page = Clusters(swatches, palette, clusterIndex)
    page.render(pathName, title)

# -----------------------------------------------------------------------------
# Command Line
# -----------------------------------------------------------------------------


def buildArgParser():
    import argparse

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
    p.add_argument('-r', '--random',
                   action='store_true', dest='random', default=False,
                   help='start with random centroids')
    p.add_argument('--use-hsl',
                   action='store_true', dest='hsl', default=False,
                   help='use HSL not RGB for cluster calc')
    p.add_argument('--trial',
                   metavar='NAME', dest='trial', required=False,
                   help='identify a cluster run')

    return p


if __name__ == '__main__':
    parser = buildArgParser()
    args = parser.parse_args()

    run(args)
