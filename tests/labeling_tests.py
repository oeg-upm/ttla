from label import SimilarityMeasures
from app import app
import unittest
import os
import pandas as pd
import commons


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

    # def test_ks(self):
    #     bag1 = [10,20,30]
    #     bag2 = [11,21,50]
    #     sm = SimilarityMeasures.SimilarityMeasures()
    #     stat, pval = sm.KSTest(bag1, bag2)
    #     self.assertAlmostEqual(stat, 0.333, places=3)
    #     self.assertAlmostEqual(pval, 0.976, places=3)

    def test_model_contruction(self):
        from label import model_construction, classification
        model_construction.TEST = True
        class_uri = "http://dbpedia.org/ontology/BadmintonPlayer"
        # class_uri = "http://dbpedia.org/ontology/BasketballPlayer"
        model_fdir = model_construction.build_model(class_uri)
        print("model fdir: %s" % model_fdir)
        df = pd.read_csv(model_fdir, delimiter='\t', names=['property_uri', 'kind', 'features'])
        property_uri_w1 = "http://dbpedia.org/ontology/Person/weight"
        property_uri_w2 = "http://dbpedia.org/property/weight"
        property_uri_ws = [property_uri_w1, property_uri_w2]
        # property_uri = "http://dbpedia.org/ontology/Person/height"
        print("test_model_contruction> df: ")
        print(df)
        kind = commons.OTHER
        for idx, row in df.iterrows():
            if row['property_uri'] in property_uri_ws:
                self.assertEqual(kind, row[1])
                trimean, tstd = row['features'].split(',')
                trimean = float(trimean)
                tstd = float(tstd)
                # These number can change overtime depending on DBpedia
                trimean_test = 65.75
                tstd_test = 9.405536863290896

                self.assertTrue(trimean_test-10 < trimean < trimean_test+10)
                self.assertTrue(tstd_test-5 < tstd < tstd_test+5)
                # self.assertAlmostEqual(trimean, trimean_test, places=1)
                # self.assertAlmostEqual(tstd, tstd_test, places=1)
                break

        classification.TEST = True
        columns = [
            [50, 60, 70, 71, 78, 80, 81],  # Person/weight
            [170, 171, 178, 180, 181]  # Person/height
        ]
        # print label.features.compute_features(kind=commons.OTHER, nums=columns[0])
        property_uri2 = "http://dbpedia.org/ontology/Person/height"
        predictions = classification.classify(commons.OTHER, class_uri, columns)
        print("predictions")
        print(predictions)
        for pred in predictions:
            for p in pred:
                print(p)
            print("\n\n===================================")
        self.assertIn(predictions[0][0][1], property_uri_ws)
        self.assertEqual(predictions[1][0][1], property_uri2)


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

