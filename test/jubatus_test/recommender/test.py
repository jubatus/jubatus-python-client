#!/usr/bin/env python

import unittest

import json
from math import sqrt
import msgpackrpc

from jubatus.recommender.client import Recommender
from jubatus.recommender.types import *
from jubatus_test.test_util import TestUtil
from jubatus.common import Datum

host = "127.0.0.1"
port = 21003
timeout = 10

class RecommenderTest(unittest.TestCase):
    def setUp(self):
        self.config = {
            "method": "inverted_index",
            "converter": {
                "string_filter_types": {},
                "string_filter_rules": [],
                "num_filter_types": {},
                "num_filter_rules": [],
                "string_types": {},
                "string_rules": [{"key": "*", "type": "str", "sample_weight": "bin", "global_weight": "bin"}],
                "num_types": {},
                "num_rules": [{"key": "*", "type": "num"}]
                },
            "parameter": {}
            }

        TestUtil.write_file('config_recommender.json', json.dumps(self.config))
        self.srv = TestUtil.fork_process('recommender', port, 'config_recommender.json')
        try:
            self.cli = Recommender(host, port, "name")
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

    def test_complete_row(self):
        self.cli.clear_row("complete_row")
        d = Datum({"skey1": "val1", "skey2": "val2", "nkey1": 1.0, "nkey2": 2.0})
        self.cli.update_row("complete_row", d)
        d1 = self.cli.complete_row_from_id("complete_row")
        d2 = self.cli.complete_row_from_datum(d)

    def test_similar_row(self):
        self.cli.clear_row("similar_row")
        d = Datum({"skey1": "val1", "skey2": "val2", "nkey1": 1.0, "nkey2": 2.0})
        self.cli.update_row("similar_row", d)
        s1 = self.cli.similar_row_from_id("similar_row", 10)
        s2 = self.cli.similar_row_from_datum(d, 10)

    def test_decode_row(self):
        self.cli.clear_row("decode_row")
        d = Datum({"skey1": "val1", "skey2": "val2", "nkey1": 1.0, "nkey2": 2.0})
        self.cli.update_row("decode_row", d)
        decoded_row = self.cli.decode_row("decode_row")
        self.assertEqual(json.dumps(d.string_values), json.dumps(decoded_row.string_values))
        self.assertEqual(json.dumps(d.num_values), json.dumps(decoded_row.num_values))

    def test_get_row(self):
        self.cli.clear()
        d = Datum({"skey1": "val1", "skey2": "val2", "nkey1": 1.0, "nkey2": 2.0})
        self.cli.update_row("get_row", d)
        row_names = self.cli.get_all_rows()
        self.assertEqual(row_names, ["get_row"])

    def test_clear(self):
        self.cli.clear()

    def test_calcs(self):
        d = Datum({"skey1": "val1", "skey2": "val2", "nkey1": 1.0, "nkey2": 2.0})
        self.assertAlmostEqual(self.cli.calc_similarity(d, d), 1, 6)
        self.assertAlmostEqual(self.cli.calc_l2norm(d), sqrt(1*1 + 1*1+ 1*1 + 2*2), 6)

    def test_clear(self):
        self.cli.clear()

    def test_save(self):
        self.assertEqual(len(self.cli.save("recommender.save_test.model")), 1)

    def test_load(self):
        model_name = "recommender.load_test.model"
        self.cli.save(model_name)
        self.assertEqual(self.cli.load(model_name), True)

    def test_get_status(self):
        self.cli.get_status()

if __name__ == '__main__':
    test_suite = unittest.TestLoader().loadTestsFromTestCase(RecommenderTest)
    unittest.TextTestRunner().run(test_suite)

