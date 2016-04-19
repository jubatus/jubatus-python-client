#!/usr/bin/env python

import unittest
import json
import msgpackrpc

from jubatus.classifier.client import Classifier
from jubatus.classifier.types import *
from jubatus_test.test_util import TestUtil
from jubatus.common import Datum

host = "127.0.0.1"
port = 21001
timeout = 10

class ClassifierTest(unittest.TestCase):
    def setUp(self):
        self.config = {
            "method": "AROW",
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
                "regularization_weight": 1.001
                }
            }

        TestUtil.write_file('config_classifier.json', json.dumps(self.config))
        self.srv = TestUtil.fork_process('classifier', port, 'config_classifier.json')
        try:
            self.cli = Classifier(host, port, "name")
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
        data = [["label", d]]
        self.assertEqual(self.cli.train(data), 1)

    def test_classify(self):
        d = Datum({"skey1": "val1", "skey2": "val2", "nkey1": 1.0, "nkey2": 2.0})
        data = [d]
        result = self.cli.classify(data)

    def test_set_label(self):
        self.assertEqual(self.cli.set_label("label"), True)

    def test_get_labels(self):
        self.cli.set_label("label")
        self.assertEqual(self.cli.get_labels(), {"label": 0})

    def test_delete_label(self):
        self.cli.set_label("label")
        self.assertEqual(self.cli.delete_label("label"), True)

    def test_save(self):
        self.assertEqual(len(self.cli.save("classifier.save_test.model")), 1)

    def test_load(self):
        model_name = "classifier.load_test.model"
        self.cli.save(model_name)
        self.assertEqual(self.cli.load(model_name), True)

    def test_get_status(self):
        self.cli.get_status()

    def test_str(self):
        self.assertEqual("estimate_result{label: label, score: 1.0}",
                         str(EstimateResult("label", 1.0)))


if __name__ == '__main__':
    test_suite = unittest.TestLoader().loadTestsFromTestCase(ClassifierTest)
    unittest.TextTestRunner().run(test_suite)
