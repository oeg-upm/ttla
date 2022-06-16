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
from t2dv2_tests import T2Dv2Tests
from scores_tests import ScoresTests
import unittest


if __name__ == "__main__":
    sample_cases = unittest.TestLoader().loadTestsFromTestCase(SampleTest)
    detect_cases = unittest.TestLoader().loadTestsFromTestCase(DetectionTests)
    labeling_cases = unittest.TestLoader().loadTestsFromTestCase(LabelingTests)
    commons_cases = unittest.TestLoader().loadTestsFromTestCase(EasySPARQLTests)
    scores_cases = unittest.TestLoader().loadTestsFromTestCase(ScoresTests)

    cases = [
        scores_cases,
        sample_cases,
        detect_cases,
        labeling_cases,
        commons_cases
    ]

    if len(sys.argv) == 2:
        if sys.argv[1] == "t2dv2":
            t2dv2_cases = unittest.TestLoader().loadTestsFromTestCase(T2Dv2Tests)
            cases.append(t2dv2_cases)
        else:
            print("ERROR: wrong test parameter")

    suite = unittest.TestSuite(cases)
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())
