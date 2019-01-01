from __future__ import print_function
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# added this to import app.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sample_tests import SampleTest
from detection_tests import DetectionTests
import unittest


sample_cases = unittest.TestLoader().loadTestsFromTestCase(SampleTest)
detect_cases = unittest.TestLoader().loadTestsFromTestCase(DetectionTests)
suite = unittest.TestSuite([sample_cases, detect_cases])
result = unittest.TextTestRunner().run(suite)
sys.exit(not result.wasSuccessful())