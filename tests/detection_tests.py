import ttla.detect
from app import app
import unittest
import os
from ttla.detect.Detection import Detection
from ttla.detect import testDetection
from ttla.commons import CATEGORICAL, ORDINAL, SEQUENTIAL, HIERARCHICAL, COUNTS, OTHER

DATA_HOME = os.path.join(os.path.abspath("tests"), 'data')


class DetectionTests(unittest.TestCase):

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

    # def test_home_assert(self):
    #     # sends HTTP GET request to the application
    #     # on the specified path
    #     self.assertTrue(False)

    # def test_detect_categorical_binary(self):
    #     categ_file = os.path.join(DATA_HOME, 'categorical_binary.csv')
    #     # print("categorical file path: "+str(categ_file))
    #     types = detect.detect_column_types(categ_file)
    #     self.assertEqual(types, [detect.UNKNOWN, detect.CATEGORICAL, detect.UNKNOWN])

    def test_ordinal(self):
        detect = Detection([1, 2, 3, 4, 5])  # ordinal
        self.assertEqual(detect.type, ORDINAL)

    def test_detect_ordinal(self):
        detect = Detection()  # ordinal
        self.assertEqual(detect.detect([1, 2, 3, 4, 5]), ORDINAL)

    def test_categorical(self):
        # Otherwise, things like weight will be as a categorical
        # detect = Detection([1, 1, 3, 3, 3, 3, 3, 5])
        # self.assertEqual(detect.type, CATEGORICAL)
        detect = Detection([1, 1, 1, 1, 3, 3, 3, 3, 3, 5, 5, 5, 5])
        self.assertEqual(detect.type, CATEGORICAL)
        img_size = [220, 200, 220, 200, 200, 200, 220, 270, 250, 200, 220, 200, 250, 200, 200, 250, 200, 220, 200, 220,
                    220, 250, 220, 200, 220, 250, 200, 200, 200, 100, 200]
        detect = Detection(img_size)
        self.assertEqual(detect.type, CATEGORICAL)
        neg_cat = [220, 200, 220, 200, 200, 200, 220, -270, 250, 200, 220, 200, -250, 200, 200, 250, 200, -220, 200,
                   -220,
                   220, 250, 220, 200, 220, 250, 200, 200, 200, 100, 200]
        detect = Detection(neg_cat)
        self.assertNotEqual(detect.type, CATEGORICAL)
        float_cat = [220.0, 200.1, 220.1, 200.2, 200.3, 200.5, 220, 270, 250, 200, 220, 200, 250, 200, 200, 250, -200,
                     220, 200, 220,
                     220, 250, 220, 200, 220, 250, 200, -200, 200, 100, -200]
        detect = Detection(float_cat)
        self.assertNotEqual(detect.type, CATEGORICAL)

    def test_sequential(self):
        detect = Detection([2, 4, 6, 8, 10])
        self.assertEqual(detect.type, SEQUENTIAL)
        detect = Detection([2, 5, 6, 8, 10])
        self.assertEqual(detect.type, SEQUENTIAL)
        detect = Detection([0, 2, 4, 6, 9, 12, 15])
        self.assertEqual(detect.type, SEQUENTIAL)

    def test_hierarchical(self):
        detect = Detection([12312, 12327, 12339, 12347, 12358])
        self.assertEqual(detect.type, HIERARCHICAL)

    def test_counts(self):
        detect = Detection([28, 456, 2, 18, 12358])
        self.assertEqual(detect.type, COUNTS)

    def test_other(self):
        detect = Detection([28, 456, 2, 18, 200])
        self.assertEqual(detect.type, OTHER)

    # def test_detection_score(self):
    #     results = testDetection.type_evaluation()
    #     correct_results = {'ordinal': {'recall': '1.0', 'precision': '0.8', 'f1': '0.889'},
    #                        'count': {'recall': '0.809', 'precision': '0.792', 'f1': '0.8'},
    #                        'categorical': {'recall': '0.0', 'precision': '-', 'f1': '-'},
    #                        'random': {'recall': '-', 'precision': '-', 'f1': '-'},
    #                        'sequential': {'recall': '0.0', 'precision': '0.0', 'f1': 'N/A'},
    #                        'year': {'recall': '1.0', 'precision': '0.8', 'f1': '0.889'},
    #                        'hierarchical': {'recall': '-', 'precision': '-', 'f1': '-'},
    #                        'other': {'recall': '0.516', 'precision': '0.552', 'f1': '0.533'}}
    #     self.assertDictEqual(results, correct_results)
