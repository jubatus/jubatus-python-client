#!/usr/bin/env python

import unittest
import json
import msgpackrpc

from jubatus.regression.client import Regression
from jubatus.regression.types import *
from jubatus_test.test_util import TestUtil
from jubatus.common import Datum

host = "127.0.0.1"
port = 21002
timeout = 10

class RegressionTest(unittest.TestCase):
    def setUp(self):
        self.config = {
            "method": "PA",
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
            "parameter": {
                "sensitivity" : 0.1,
                "regularization_weight" : 3.402823e+38
                }
            }

        TestUtil.write_file('config_regression.json', json.dumps(self.config))
        self.srv = TestUtil.fork_process('regression', port, 'config_regression.json')
        try:
            self.cli = Regression(host, port, "name")
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

    def test_train(self):
        d = Datum({"skey1": "val1", "skey2": "val2", "nkey1": 1.0, "nkey2": 2.0})
        data = [[1.0, d]]
        self.assertEqual(self.cli.train(data), 1)

    def test_estimate(self):
        d = Datum({"skey1": "val1", "skey2": "val2", "nkey1": 1.0, "nkey2": 2.0})
        data = [d]
        result = self.cli.estimate(data)

    def test_save(self):
        self.assertEqual(len(self.cli.save("regression.save_test.model")), 1)

    def test_load(self):
        model_name = "regression.load_test.model"
        self.cli.save(model_name)
        self.assertEqual(self.cli.load(model_name), True)

    def test_get_status(self):
        self.cli.get_status()

if __name__ == '__main__':
    test_suite = unittest.TestLoader().loadTestsFromTestCase(RegressionTest)
    unittest.TextTestRunner().run(test_suite)

