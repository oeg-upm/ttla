import ttla.detect
from app import app
import unittest
import os
from ttla.detect.Detection import Detection
from ttla.detect import testDetection
from ttla.commons import CATEGORICAL, ORDINAL, SEQUENTIAL, HIERARCHICAL, COUNTS, OTHER
from experiments import web_commons_v2
DATA_HOME = os.path.join(os.path.abspath("tests"), 'data')


class T2Dv2Tests(unittest.TestCase):

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

    def test_detection_score(self):
        results = testDetection.type_evaluation()
        correct_results = {'ordinal': {'recall': '1.0', 'precision': '0.8', 'f1': '0.889'},
                           'count': {'recall': '0.809', 'precision': '0.792', 'f1': '0.8'},
                           'categorical': {'recall': '0.0', 'precision': '-', 'f1': '-'},
                           'random': {'recall': '-', 'precision': '-', 'f1': '-'},
                           'sequential': {'recall': '0.0', 'precision': '0.0', 'f1': 'N/A'},
                           'year': {'recall': '1.0', 'precision': '0.8', 'f1': '0.889'},
                           'hierarchical': {'recall': '-', 'precision': '-', 'f1': '-'},
                           'other': {'recall': '0.516', 'precision': '0.552', 'f1': '0.533'}}
        self.assertDictEqual(results, correct_results)

    def test_labeling_scores(self):
        web_commons_v2.label_experiment()
        web_commons_v2.add_kind_to_results()
        scores = self.web_commons_v2.show_scores_from_results()
        # d = {1: {'all': {'f1': '0.776', 'precision': '0.687', 'recall': '0.892'},
        #          'categorical': {'f1': 'N/A', 'precision': 'N/A', 'recall': 'N/A'},
        #          'count': {'f1': '0.889', 'precision': '0.83', 'recall': '0.957'},
        #          'hierarchical': {'f1': 'N/A', 'precision': 'N/A', 'recall': 'N/A'},
        #          'ordinal': {'f1': 'N/A', 'precision': 'N/A', 'recall': 'N/A'},
        #          'other': {'f1': '0.604', 'precision': '0.486', 'recall': '0.8'},
        #          'sequential': {'f1': '1.0', 'precision': '1.0', 'recall': '1.0'}},
        #      3: {'all': {'f1': '0.915', 'precision': '0.94', 'recall': '0.892'},
        #          'categorical': {'f1': 'N/A', 'precision': 'N/A', 'recall': 'N/A'},
        #          'count': {'f1': '0.957', 'precision': '0.957', 'recall': '0.957'},
        #          'hierarchical': {'f1': 'N/A', 'precision': 'N/A', 'recall': 'N/A'},
        #          'ordinal': {'f1': 'N/A', 'precision': 'N/A', 'recall': 'N/A'},
        #          'other': {'f1': '0.853', 'precision': '0.914', 'recall': '0.8'},
        #          'sequential': {'f1': '1.0', 'precision': '1.0', 'recall': '1.0'}},
        #      5: {'all': {'f1': '0.932', 'precision': '0.976', 'recall': '0.892'},
        #          'categorical': {'f1': 'N/A', 'precision': 'N/A', 'recall': 'N/A'},
        #          'count': {'f1': '0.978', 'precision': '1.0', 'recall': '0.957'},
        #          'hierarchical': {'f1': 'N/A', 'precision': 'N/A', 'recall': 'N/A'},
        #          'ordinal': {'f1': 'N/A', 'precision': 'N/A', 'recall': 'N/A'},
        #          'other': {'f1': '0.866', 'precision': '0.943', 'recall': '0.8'},
        #          'sequential': {'f1': '1.0', 'precision': '1.0', 'recall': '1.0'}},
        #      10: {'all': {'f1': '0.943', 'precision': '1.0', 'recall': '0.892'},
        #           'categorical': {'f1': 'N/A', 'precision': 'N/A', 'recall': 'N/A'},
        #           'count': {'f1': '0.978', 'precision': '1.0', 'recall': '0.957'},
        #           'hierarchical': {'f1': 'N/A', 'precision': 'N/A', 'recall': 'N/A'},
        #           'ordinal': {'f1': 'N/A', 'precision': 'N/A', 'recall': 'N/A'},
        #           'other': {'f1': '0.889', 'precision': '1.0', 'recall': '0.8'},
        #           'sequential': {'f1': '1.0', 'precision': '1.0', 'recall': '1.0'}}}
        d = {1: {'all': {'f1': '0.733', 'precision': '0.649', 'recall': '0.842'},
             'categorical': {'f1': 'N/A', 'precision': 'N/A', 'recall': 'N/A'},
             'count': {'f1': '0.881', 'precision': '0.822', 'recall': '0.949'},
             'hierarchical': {'f1': 'N/A', 'precision': 'N/A', 'recall': 'N/A'},
             'ordinal': {'f1': 'N/A', 'precision': 'N/A', 'recall': 'N/A'},
             'other': {'f1': '0.444', 'precision': '0.357', 'recall': '0.588'},
             'sequential': {'f1': '1.0', 'precision': '1.0', 'recall': '1.0'}},
         3: {'all': {'f1': '0.908', 'precision': '0.932', 'recall': '0.885'},
             'categorical': {'f1': 'N/A', 'precision': 'N/A', 'recall': 'N/A'},
             'count': {'f1': '0.956', 'precision': '0.956', 'recall': '0.956'},
             'hierarchical': {'f1': 'N/A', 'precision': 'N/A', 'recall': 'N/A'},
             'ordinal': {'f1': 'N/A', 'precision': 'N/A', 'recall': 'N/A'},
             'other': {'f1': '0.833', 'precision': '0.893', 'recall': '0.781'},
             'sequential': {'f1': '1.0', 'precision': '1.0', 'recall': '1.0'}},
         5: {'all': {'f1': '0.929', 'precision': '0.973', 'recall': '0.889'},
             'categorical': {'f1': 'N/A', 'precision': 'N/A', 'recall': 'N/A'},
             'count': {'f1': '0.978', 'precision': '1.0', 'recall': '0.957'},
             'hierarchical': {'f1': 'N/A', 'precision': 'N/A', 'recall': 'N/A'},
             'ordinal': {'f1': 'N/A', 'precision': 'N/A', 'recall': 'N/A'},
             'other': {'f1': '0.852', 'precision': '0.929', 'recall': '0.788'},
             'sequential': {'f1': '1.0', 'precision': '1.0', 'recall': '1.0'}},
         10: {'all': {'f1': '0.943', 'precision': '1.0', 'recall': '0.892'},
              'categorical': {'f1': 'N/A', 'precision': 'N/A', 'recall': 'N/A'},
              'count': {'f1': '0.978', 'precision': '1.0', 'recall': '0.957'},
              'hierarchical': {'f1': 'N/A', 'precision': 'N/A', 'recall': 'N/A'},
              'ordinal': {'f1': 'N/A', 'precision': 'N/A', 'recall': 'N/A'},
              'other': {'f1': '0.889', 'precision': '1.0', 'recall': '0.8'},
              'sequential': {'f1': '1.0', 'precision': '1.0', 'recall': '1.0'}}}

        self.assertDictEqual(d, scores)
