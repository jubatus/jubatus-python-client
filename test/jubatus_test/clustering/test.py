
#!/usr/bin/env python
import unittest

import json
from math import sqrt
import msgpackrpc

from jubatus.clustering.client import Clustering
from jubatus.clustering.types import *
from jubatus_test.test_util import TestUtil

host = "127.0.0.1"
port = 21038
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
                "compressor_method" : "compressive_kmeans",
                "backet_size" : 10000,
                "compressed_backet_size" : 1000,
                "bicriteria_base_size" : 10,
                "backet_length" : 2,
                "forgetting_factor" : 0,
                "forgetting_threshold" : 0.5
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
        TestUtil.kill_process(self.srv)

    def test_get_client(self):
        self.assertTrue(isinstance(self.cli.get_client(), msgpackrpc.client.Client))

if __name__ == '__main__':
    test_suite = unittest.TestLoader().loadTestsFromTestCase(ClusteringTest)
    unittest.TextTestRunner().run(test_suite)
