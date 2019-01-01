import detect
from app import app
import unittest
import os

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

    def test_detect_categorical_binary(self):
        categ_file = os.path.join(DATA_HOME, 'categorical_binary.csv')
        # print("categorical file path: "+str(categ_file))
        types = detect.detect_column_types(categ_file)
        self.assertEqual(types, [detect.UNKNOWN, detect.CATEGORICAL, detect.UNKNOWN])