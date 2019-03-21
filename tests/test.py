from __future__ import print_function
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# added this to import app.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sample_tests import SampleTest
from detection_tests import DetectionTests
from labeling_tests import LabelingTests
from commons_tests import EasySPARQLTests
import unittest


sample_cases = unittest.TestLoader().loadTestsFromTestCase(SampleTest)
detect_cases = unittest.TestLoader().loadTestsFromTestCase(DetectionTests)
labeling_cases = unittest.TestLoader().loadTestsFromTestCase(LabelingTests)
commons_cases = unittest.TestLoader().loadTestsFromTestCase(EasySPARQLTests)
suite = unittest.TestSuite([sample_cases, detect_cases, labeling_cases, commons_cases])
result = unittest.TextTestRunner().run(suite)
sys.exit(not result.wasSuccessful())