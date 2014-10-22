from Cluster import Cluster
import math
import urllib2



DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
MAP_URL = DIRECTORY + "data_clustering/USA_Counties.png"
DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"

def slow_cluster_pairs(cluster_list):

    """
    this is the brute force implementation to find the two closest points on a graph
    code is also not written in OO format as the autograger for the course would not accept
    the object oriented version
    """

    distance = float("inf")
    index1 = -1
    index2 = -1
    distances = set()
    tup = (distance, index1, index2)

    #each pair is represented by a tuple return a set of all equal distances

    for cluindex1 in xrange(0, len(cluster_list) -1):
        for cluindex2 in xrange(cluindex1 + 1, len(cluster_list)):

            euclid = cluster_list[cluindex1].distance(cluster_list[cluindex2])

            if euclid < distance:
                distance = euclid
                tup = (distance, cluindex1, cluindex2)
            elif euclid == distance:
                equaltup = (distance, cluindex1, cluindex2)
                distances.add(equaltup)

    distances.add(tup)

    return distances

def CreateClusterList(csvlocation):

    response = urllib2.urlopen(csvlocation)
    htmldata = response.read()
    lines = htmldata.split("\n")
    data_tokens = [line.split(',') for line in lines]
    return [Cluster(tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])) for tokens in data_tokens]




def fast_closest_pairs(cluster_list):

    """fast_losest_pairs does the same but is a more refined algorithm and In theory should run faster"""

    horiz_order = getHorizIndices(cluster_list)
    vert_order = getVertIndices(cluster_list)

    def fast_helper( cluster_list, horiz_order, vert_order):

        if len(horiz_order) <= 3:
            return slow_cluster_pairs([cluster_list[x] for x in horiz_order])

        else:

            #DIVIDE

            numpoints = len(horiz_order) / 2
            midpoint = getMidpoint(cluster_list, horiz_order[numpoints - 1], horiz_order[numpoints])
            hleft = horiz_order[0: numpoints]
            hright = horiz_order[numpoints: len(horiz_order)]
            vleft = copyToVertical(hleft, vert_order)
            vright = copyToVertical(hright, vert_order)
            leftmindata = fast_helper(cluster_list, hleft, vleft)
            rightmindata = fast_helper(cluster_list, hright, vright)
            combinedmindata = min(leftmindata, rightmindata)

            #MERGE

            combinedmindata = combinedmindata.pop()
            smallestsdist = combinedmindata[0]
            mergeset = createMergeSet(smallestsdist, midpoint,cluster_list, vert_order)
            numelements = len(mergeset)

            for indexu in range(numelements - 2):
                for indexv in range(indexu + 1, min(indexu + 3, numelements - 1)):

                     comparison = cluster_list[mergeset[indexu]].distance(cluster_list[mergeset[indexv]])
                     combinedmindata = min(combinedmindata.pop(), comparison)

        return combinedmindata

    combinedmindata = fast_helper(cluster_list, horiz_order, vert_order)
    return combinedmindata


def createMergeSet(smallestdist,midpoint,cluster_list, vert_order):   #below are helper methods

    return [index for index in vert_order if (cluster_list[index].horiz_center() - midpoint) < smallestdist]


def copyToVertical(hlist, vert_order):

    return [item for item in vert_order if item in hlist]


def getHorizIndices(cluster_list):

    orderedlist = [(cluster_list[x].horiz_center(), x) for x in range(len(cluster_list))]
    orderedlist.sort()
    return [orderedlist[x][1] for x in range(len(orderedlist))]


def getVertIndices(cluster_list):

    orderedlistycoords = [(cluster_list[yindex].vert_center(), yindex) for yindex in range(len(cluster_list))]
    orderedlistycoords.sort()
    return [orderedlistycoords[index][1] for index in range(len(orderedlistycoords))]


def getMidpoint(cluster_list, index1, index2):
    return 0.5 * (cluster_list[index1].horiz_center() + cluster_list[index2].horiz_center())

