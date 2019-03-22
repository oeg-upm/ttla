from label import SimilarityMeasures
from app import app
import unittest
import os
import commons

ENDPOINT = commons.ENDPOINT


class EasySPARQLTests(unittest.TestCase):
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

    def test_get_properties(self):
        properties = commons.get_properties(endpoint=ENDPOINT,
                                            class_uri="http://dbpedia.org/ontology/BadmintonPlayer",
                                            min_num=100)
        # print("The number of properties: %d" % len(properties))
        self.assertGreater(len(properties), 120)  # now it is 141, but can change over time depends on DBpedia.
        # The number 120 is just an approximate as it is less that 141 (in case some properties are deprecated in the
        # future) and still high to make sure the function actually works
        properties = commons.get_properties(endpoint=ENDPOINT,
                                            class_uri="http://dbpedia.org/ontology/BadmintonPlayer")
        self.assertGreater(len(properties), 120)  # now it is 141, but can change over time depends on DBpedia.

    def test_run_query(self):
        query = """
            select distinct ?Concept where {[] a ?Concept} LIMIT 100
        """
        results = commons.run_query(endpoint=ENDPOINT, query=query)
        # print("The number of classes: %d" % len(results))
        self.assertEqual(len(results), 100)