#!/usr/bin/env python
import unittest

import json
from math import sqrt
import msgpackrpc

from jubatus.clustering.client import Clustering
from jubatus.clustering.types import *
from jubatus_test.test_util import TestUtil
from jubatus.common import Datum

host = "127.0.0.1"
port = 21008
timeout = 10

class ClusteringTest(unittest.TestCase):
    def setUp(self):
        self.config = {
            "method" : "kmeans",
            "converter" : {
                "string_filter_types" : {},
                "string_filter_rules" : [],
                "num_filter_types" : {},
                "num_filter_rules" : [],
                "string_types" : {},
                "string_rules" : [
                    { "key" : "*", "type" : "str", "sample_weight" : "bin", "global_weight" : "bin" }
                    ],
                "num_types" : {},
                "num_rules" : [
                    { "key" : "*", "type" : "num" }
                    ]
                },
            "parameter" : {
                "k" : 10,
                "compressor_method" : "simple",
                "bucket_size" : 3,
                "compressed_bucket_size" : 2,
                "bicriteria_base_size" : 1,
                "bucket_length" : 2,
                "forgetting_factor" : 0,
                "forgetting_threshold" : 0.5,
                "seed": 0,
                } 
            }

        TestUtil.write_file('config_clustering.json', json.dumps(self.config))
        self.srv = TestUtil.fork_process('clustering', port, 'config_clustering.json')
        try:
            self.cli = Clustering(host, port, "name")
        except:
            TestUtil.kill_process(self.srv)
            raise

    def tearDown(self):
        if self.cli:
            self.cli.get_client().close()
        TestUtil.kill_process(self.srv)

    def test_get_client(self):
        self.assertTrue(isinstance(self.cli.get_client(), msgpackrpc.client.Client))

    def test_push(self):
        d = Datum()
        self.assertTrue(self.cli.push([d]))
 
    def test_get_revision(self):
        res = self.cli.get_revision()
        self.assertTrue(isinstance(res, int))

    def test_get_core_members(self):
        for i in range(0, 100):
            d = Datum({"nkey1": i, "nkey2": -i})
            self.cli.push([d])
        res = self.cli.get_core_members()
        self.assertEqual(len(res), 10)
        self.assertTrue(isinstance(res[0][0], WeightedDatum))

    def test_get_k_center(self):
        for i in range(0, 100):
            d = Datum({"nkey1": i, "nkey2": -i})
            self.cli.push([d])
        res = self.cli.get_k_center()
        self.assertEqual(len(res), 10)
        self.assertTrue(isinstance(res[0], Datum))

    def test_get_nearest_center(self):
        for i in range(0, 100):
            d = Datum({"nkey1": i, "nkey2": -i})
            self.cli.push([d])
        q = Datum({"nkey1": 2.0, "nkey2": 1.0})
        res = self.cli.get_nearest_center(q)
        self.assertTrue(isinstance(res, Datum))

    def test_get_nearest_members(self):
        for i in range(0, 100):
            d = Datum({"nkey1": i, "nkey2": -i})
            self.cli.push([d])
        q = Datum({"nkey1": 2.0, "nkey2": 1.0})
        res = self.cli.get_nearest_members(q)
        self.assertTrue(isinstance(res[0], WeightedDatum))

if __name__ == '__main__':
    test_suite = unittest.TestLoader().loadTestsFromTestCase(ClusteringTest)
    unittest.TextTestRunner().run(test_suite)
