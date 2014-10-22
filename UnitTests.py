import unittest
import Closest_Pairs
from Cluster import Cluster
import urllib2


DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"


class TestClusters(unittest.TestCase):

    def setUp(self):

        """created small static cluster lists to determine if methods were returning correct values. I
        did this by calculating by hand. Obviously if I had done this on larger datasets It would of taken forever.
        so a couple of small cluster lists will suffice for now. """


        cluster1 = Cluster(01101, float(720.281573781), float(440.436162917), int(223510), float(5.7e-05))
        cluster2 = Cluster(01117, float(709.193528999), float(417.394467797), int(143293), float(5.6e-05))

        cluster3 = Cluster(01101, float(4), float(4), int(223510), float(5.7e-05))
        cluster4 = Cluster(01117, float(2), float(2), int(143293), float(5.6e-05))
        cluster5 = Cluster(01101, float(720.281573781), float(440.436162917), int(223510), float(5.7e-05))
        cluster6= Cluster(01117, float(709.193528999), float(417.394467797), int(143293), float(5.6e-05))


        self.test_list_small = [cluster1, cluster2]  #small test clusters
        self.test_list_small2 =[cluster3, cluster4, cluster5, cluster6]

        #create type cluster !! above

        self.data111 = Closest_Pairs.CreateClusterList(DATA_111_URL)
        self.data290 = Closest_Pairs.CreateClusterList(DATA_290_URL)


    def test_smallest_distance(self):

       testset = Closest_Pairs.slow_cluster_pairs(self.test_list_small)
       tup = testset.pop()
       self.assertEquals(round(tup[0], 4), 25.5708)
       self.assertEquals(tup[1],0)
       self.assertEquals(tup[2],1)


    def test_second_cluster_list(self):

        testset = Closest_Pairs.slow_cluster_pairs(self.test_list_small2)
        testfast = Closest_Pairs.fast_closest_pairs(self.test_list_small2)

        tup = testset.pop()
        self.assertEquals(round(tup[0], 2), 2.83)
        self.assertEqual(round(testfast[0], 2), 2.83)
        self.assertEquals(tup[1], 0)
        self.assertEquals(tup[2], 1)


    def test_data111(self):

        testset = Closest_Pairs.slow_cluster_pairs(self.data111)#
        self.assertGreaterEqual(len(testset), 0, "not greater than 0 !!!!???")
        tup = testset.pop()
        self.assertGreater(tup[2], tup[1])


    def test_getHorizIndices(self):

        indiceslist = Closest_Pairs.getHorizIndices(self.test_list_small2)
        self.assertEqual([1, 0, 3, 2], indiceslist)


    def test_getVertIndices(self):


        yindiceslist = Closest_Pairs.getVertIndices(self.test_list_small2)
        yindiceslistsmall = Closest_Pairs.getVertIndices(self.test_list_small)
        self.assertEqual([1, 0, 3, 2], yindiceslist)
        self.assertEqual([1, 0], yindiceslistsmall)

    def test_getMidpoint(self):


        dist = Closest_Pairs.getMidpoint(self.test_list_small, 1, 0)
        dist2 = Closest_Pairs.getMidpoint(self.test_list_small2, 0, 3)
        self.assertEqual(round(dist, 2), 714.74)
        self.assertEqual(round(dist2, 2), 356.60)

    def test_range(self):

        myrange = [2, 4, 6, 8, 10, 12, 14]
        midpoint = len(myrange) / 2
        print midpoint
        print myrange[0: midpoint]
        print myrange[midpoint: len(myrange)]


    def test_CopyToVert(self):

       test_list = Closest_Pairs.copyToVertical([1, 2, 3], [1, 2, 3, 4, 5, 6, 7, 8])
       self.assertEqual([1, 2, 3], test_list)
      

    def test_CreateMergeSet(self):


        mergelist = Closest_Pairs.createMergeSet(2,200 , self.test_list_small2,[0, 1, 2, 3])
        self.assertEqual([0,1],mergelist)







































