#!/usr/bin/env python

import unittest
import json

from jubatus.classifier.client import classifier
from jubatus.classifier.types  import *
from jubatus_test.test_util import TestUtil

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
            "string_rules": [{"key": "*", "type": "str",  "sample_weight": "bin", "global_weight": "bin"}],
            "num_types": {},
            "num_rules": [{"key": "*", "type": "num"}]
        },
        "parameter": {
            "regularization_weight": 1.001
        }
    }

    TestUtil.write_file('config_classifier.json', json.dumps(self.config))
    self.srv = TestUtil.fork_process('classifier', port, 'config_classifier.json')
    self.cli = classifier(host, port)

  def tearDown(self):
    TestUtil.kill_process(self.srv)

  def test_get_config(self):
    config = self.cli.get_config("name")
    self.assertEqual(json.dumps(json.loads(config), sort_keys=True), json.dumps(self.config, sort_keys=True))

  def test_train(self):
    string_values = [["key1", "val1"], ["key2", "val2"]]
    num_values = [["key1", 1.0], ["key2", 2.0]]
    d = datum(string_values, num_values)
    data = [["label", d]]
    self.assertEqual(self.cli.train("name", data), 1)

  def test_classify(self):
    string_values = [["key1", "val1"], ["key2", "val2"]]
    num_values = [["key1", 1.0], ["key2", 2.0]]
    d = datum(string_values, num_values)
    data = [d]
    result = self.cli.classify("name", data)

  def test_save(self):
    self.assertEqual(self.cli.save("name", "classifier.save_test.model"), True)

  def test_load(self):
    model_name = "classifier.load_test.model"
    self.cli.save("name", model_name)
    self.assertEqual(self.cli.load("name", model_name), True)

  def test_get_status(self):
    self.cli.get_status("name")



if __name__ == '__main__':
  test_suite = unittest.TestLoader().loadTestsFromTestCase(ClassifierTest)
  unittest.TextTestRunner().run(test_suite)
