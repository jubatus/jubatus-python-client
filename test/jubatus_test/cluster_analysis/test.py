#!/usr/bin/env python
import unittest

import json
from math import sqrt
import msgpackrpc

from jubatus.cluster_analysis.client import ClusterAnalysis
from jubatus.cluster_analysis.types import *
from jubatus_test.test_util import TestUtil
from jubatus.common import Datum

host = "127.0.0.1"
port = 21008
timeout = 10

class ClusterAnalysisTest(unittest.TestCase):
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
                "backet_size" : 1,
                "compressed_backet_size" : 1,
                "bicriteria_base_size" : 10,
                "backet_length" : 1,
                "forgetting_factor" : 0,
                "forgetting_threshold" : 0.5
                } 
            }

        TestUtil.write_file('config_cluster_analysis.json', json.dumps(self.config))
        self.srv = TestUtil.fork_process('cluster_analysis', port, 'config_cluster_analysis.json')
        try:
            self.cli = ClusterAnalysis(host, port, "name")
        except:
            TestUtil.kill_process(self.srv)
            raise

    def tearDown(self):
        TestUtil.kill_process(self.srv)

    def test_get_client(self):
        self.assertTrue(isinstance(self.cli.get_client(), msgpackrpc.client.Client))

    def test_add_snapshot(self):
        self.assertTrue(self.cli.add_snapshot("snap"))
        self.assertTrue(False)

    def test_get_histoty(self):
        self.cli.add_snapshot("snap1")
        self.cli.add_snapshot("snap2")
        self.cli.add_snapshot("snap3")
        res = self.clie.get_history()
        self.assertEqual(len(res), 2)
        self.assertTrue(isinstance(res[0], ChangeGraph))
        self.assertEqual(res[0].snapshot_name1, "snap1")
        self.assertEqual(res[0].snapshot.name2, "snap2")
        self.assertEqual(res[1].snapshot_name1, "snap2")
        self.assertEqual(res[1].snapshot.name2, "snap3")

    def test_get_snapshots(self):
        self.cli.add_snapshot("snap1")
        self.cli.add_snapshot("snap2")
        res = self.clie.get_snapshos()
        self.assertEqual(len(res), 2)
        self.assertTrue(isinstance(res[0], ClusteringSnapshot))
        self.assertEqual(res[0].name, "snap1")
        self.assertEqual(res[1].name, "snap2")


if __name__ == '__main__':
    test_suite = unittest.TestLoader().loadTestsFromTestCase(ClusterAnalysisTest)
    unittest.TextTestRunner().run(test_suite)
