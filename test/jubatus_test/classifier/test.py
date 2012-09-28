#!/usr/bin/env python

import unittest
from jubatus.classifier.client import classifier
from jubatus.classifier.types  import *

from jubatus_test.common import CommonUtils

host = "localhost"
port = 21001
timeout = 10

class ClassifierTest(unittest.TestCase):
  def setUp(self):
    self.srv = CommonUtils.start_server("jubaclassifier", port)
    self.cli = classifier(host, port)
    method = "AROW"
    self.converter = "{\n\"string_filter_types\":{}, \n\"string_filter_rules\":[], \n\"num_filter_types\":{}, \n\"num_filter_rules\":[], \n\"string_types\":{}, \n\"string_rules\":\n[{\"key\":\"*\", \"type\":\"space\", \n\"sample_weight\":\"bin\", \"global_weight\":\"bin\"}\n], \n\"num_types\":{}, \n\"num_rules\":[\n{\"key\":\"*\", \"type\":\"num\"}\n]\n}"
    cd = config_data(method, self.converter)
    self.cli.set_config("name", cd)

  def tearDown(self):
    CommonUtils.stop_server(self.srv)

  def test_get_config(self):
    config = self.cli.get_config("name")
    self.assertEqual(config.method, "AROW")
    self.assertEqual(config.config, self.converter)

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
