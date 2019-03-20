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
