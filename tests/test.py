from __future__ import print_function
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# added this to import app.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sample_tests import SampleTest
import unittest

tests_cases = unittest.TestLoader().loadTestsFromTestCase(SampleTest)
suite = unittest.TestSuite([tests_cases,])
unittest.TextTestRunner().run(suite)
