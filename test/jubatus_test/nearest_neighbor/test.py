#!/usr/bin/env python

import unittest

import json
from math import sqrt
import msgpackrpc

from jubatus.nearest_neighbor.client import NearestNeighbor
from jubatus.nearest_neighbor.types  import *
from jubatus_test.test_util import TestUtil
from jubatus.common import Datum

host = "127.0.0.1"
port = 21007
timeout = 10

class NearestNeighborTest(unittest.TestCase):
    def setUp(self):
        self.config = {
            "method": "lsh",
            "converter": {
                "string_filter_types": {},
                "string_filter_rules": [],
                "num_filter_types": {},
                "num_filter_rules": [],
                "string_types": {},
                "string_rules": [{"key": "*", "type": "str",  "sample_weight": "bin", "global_weight": "bin"}],
                "num_types": {},
                "num_rules": [{"key": "*", "type": "num"}]
                },
            "parameter": {
                "hash_num": 64
                }
            }

        TestUtil.write_file('config_nearest_neighbor.json', json.dumps(self.config))
        self.srv = TestUtil.fork_process('nearest_neighbor', port, 'config_nearest_neighbor.json')
        try:
            self.cli = NearestNeighbor(host, port, "name")
        except:
            TestUtil.kill_process(self.srv)
            raise

    def tearDown(self):
        if self.cli:
            self.cli.get_client().close()
        TestUtil.kill_process(self.srv)

    def test_get_client(self):
        self.assertTrue(isinstance(self.cli.get_client(), msgpackrpc.client.Client))

    def test_get_config(self):
        config = self.cli.get_config()
        self.assertEqual(json.dumps(json.loads(config), sort_keys=True), json.dumps(self.config, sort_keys=True))

    def test_neighbor_row(self):
        self.cli.clear()
        d = Datum({"skey1": "val1", "skey2": "val2", "nkey1": 1.0, "nkey2": 2.0})
        self.cli.set_row("neighbor_row", d)
        d1 = self.cli.neighbor_row_from_id("neighbor_row", 10)
        d2 = self.cli.neighbor_row_from_datum(d, 10)

    def test_similar_row(self):
        self.cli.clear()
        d = Datum({"skey1": "val1", "skey2": "val2", "nkey1": 1.0, "nkey2": 2.0})
        self.cli.set_row("similar_row", d)
        s1 = self.cli.similar_row_from_id("similar_row", 10)
        s2 = self.cli.similar_row_from_datum(d, 10)

    def test_clear(self):
        self.cli.clear()

    def test_save(self):
        self.assertEqual(len(self.cli.save("nearest_neighbor.save_test.model")), True)

    def test_load(self):
        model_name = "nearest_neighbor.load_test.model"
        self.cli.save(model_name)
        self.assertTrue(self.cli.load(model_name))

    def test_get_status(self):
        self.cli.get_status()

if __name__ == '__main__':
    test_suite = unittest.TestLoader().loadTestsFromTestCase(NearestNeighborTest)
    unittest.TextTestRunner().run(test_suite)
    
