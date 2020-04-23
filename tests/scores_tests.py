from app import app
import unittest
import os
import pandas as pd
import experiments

DATA_HOME = os.path.join(os.path.abspath("tests"), 'data')


class ScoresTests(unittest.TestCase):
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

    def test_precision_recall_t2dv2(self):
        headers = ['fname',	'column_id', 'k', 'property_uri', 'kind', 'sub_kind']
        data = [
            ['AAA', 0, 1, 'p', 'ratio-interval', 'other'],
            ['BBB', 0, 1, 'p', 'ratio-interval', 'other'],
            ['BBA', 0, 1, 'p', 'ratio-interval', 'other'],
            ['CCC', 0, 3, 'p', 'ratio-interval', 'other'],
            ['DDD', 0, 2, 'p', 'ratio-interval', 'other'],
            ['EEE', 0, 0, 'p', 'ratio-interval', 'other'],
            ['FFF', 0, 1, 'p', 'ratio-interval', 'count'],
            ['GGG', 0, 2, 'p', 'ratio-interval', 'count'],
            ['HHH', 0, 0, 'p', 'ratio-interval', 'count'],
        ]
        df = pd.DataFrame(data, columns=headers)
        scores = experiments.web_commons_v2.compute_score_from_df("other", df, True, 1)
        self.assertEqual(str(3.0/5), scores['precision'])
        self.assertEqual(str(3.0/4), scores['recall'])
        scores = experiments.web_commons_v2.compute_score_from_df("other", df, True, 2)
        self.assertEqual(str(4.0/5), scores['precision'])
        self.assertEqual(str(4.0/5), scores['recall'])
        scores = experiments.web_commons_v2.compute_score_from_df("other", df, True, 3)
        self.assertEqual(str(5.0/5), scores['precision'])
        self.assertEqual(str(round(5.0/6, 3)), scores['recall'])
        scores = experiments.web_commons_v2.compute_score_from_df("count", df, True, 1)
        self.assertEqual(str(1.0/2), scores['precision'])
        self.assertEqual(str(1.0/2), scores['recall'])
        scores = experiments.web_commons_v2.compute_score_from_df("count", df, True, 2)
        self.assertEqual(str(2.0/2), scores['precision'])
        self.assertEqual(str(round(2.0/3, 3)), scores['recall'])
