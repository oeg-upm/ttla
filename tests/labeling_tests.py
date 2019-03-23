from label import SimilarityMeasures
from app import app
import unittest
import os

DATA_HOME = os.path.join(os.path.abspath("tests"), 'data')


class LabelingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def tearDown(self):
        pass

    def test_ks(self):
        bag1 = [10,20,30]
        bag2 = [11,21,50]
        sm = SimilarityMeasures.SimilarityMeasures()
        stat, pval = sm.KSTest(bag1, bag2)
        self.assertAlmostEqual(stat, 0.333, places=3)
        self.assertAlmostEqual(pval, 0.976, places=3)

    def test_model_contruction(self):
        from label import model_construction
        model_construction.TEST = True
        class_uri = "http://dbpedia.org/ontology/BadmintonPlayer"
        model_construction.build_model(class_uri)

    # This is just to check the difference
    # def test_model_contruction_threadings_test(self):
    #     from label import model_construction
    #     import time
    #     model_construction.TEST = True
    #     class_uri = "http://dbpedia.org/ontology/BadmintonPlayer"
    #     start = time.time()
    #     model_construction.build_model(class_uri, multi_threading=False)
    #     end = time.time()
    #     print("time for the single thread: %s" % str(end-start))
    #     start = time.time()
    #     model_construction.build_model(class_uri, multi_threading=True)
    #     end = time.time()
    #     print("time for the multi threading: %s" % str(end-start))
