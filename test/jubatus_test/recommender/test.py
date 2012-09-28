#!/usr/bin/env python

import unittest
from jubatus.recommender.client import recommender
from jubatus.recommender.types  import *

from jubatus_test.common import CommonUtils

from math import sqrt

host = "localhost"
port = 21003
timeout = 10

class RecommenderTest(unittest.TestCase):
  def setUp(self):
    self.srv = CommonUtils.start_server("jubarecommender", port)
    self.cli = recommender(host, port)
    method = "inverted_index"
    self.converter = "{\n\"string_filter_types\":{}, \n\"string_filter_rules\":[], \n\"num_filter_types\":{}, \n\"num_filter_rules\":[], \n\"string_types\":{}, \n\"string_rules\":\n[{\"key\":\"*\", \"type\":\"str\", \n\"sample_weight\":\"bin\", \"global_weight\":\"bin\"}\n], \n\"num_types\":{}, \n\"num_rules\":[\n{\"key\":\"*\", \"type\":\"num\"}\n]\n}"
    cd = config_data(method, self.converter)
    self.cli.set_config("name", cd)

  def tearDown(self):
    CommonUtils.stop_server(self.srv)

  def test_get_config(self):
    config = self.cli.get_config("name")
    self.assertEqual(config.method, "inverted_index")
    self.assertEqual(config.converter, self.converter)

  def test_complete_row(self):
    self.cli.clear_row("name", "complete_row")
    string_values = [("key1", "val1"), ("key2", "val2")]
    num_values = [("key1", 1.0), ("key2", 2.0)]
    d = datum(string_values, num_values)
    self.cli.update_row("name", "complete_row", d)
    d1 = self.cli.complete_row_from_id("name", "complete_row")
    d2 = self.cli.complete_row_from_data("name", d)

  def test_similar_row(self):
    self.cli.clear_row("name", "similar_row")
    string_values = [("key1", "val1"), ("key2", "val2")]
    num_values = [("key1", 1.0), ("key2", 2.0)]
    d = datum(string_values, num_values)
    self.cli.update_row("name", "similar_row", d)
    s1 = self.cli.similar_row_from_id("name", "similar_row", 10)
    s2 = self.cli.similar_row_from_data("name", d, 10)

  def test_decode_row(self):
    self.cli.clear_row("name", "decode_row")
    string_values = [("key1", "val1"), ("key2", "val2")]
    num_values = [("key1", 1.0), ("key2", 2.0)]
    d = datum(string_values, num_values)
    self.cli.update_row("name", "decode_row", d)
    decoded_row = self.cli.decode_row("name", "decode_row")
    self.assertEqual(d.string_values, decoded_row.string_values)
    self.assertEqual(d.num_values, decoded_row.num_values)

  def test_get_row(self):
    self.cli.clear("name")
    string_values = [("key1", "val1"), ("key2", "val2")]
    num_values = [("key1", 1.0), ("key2", 2.0)]
    d = datum(string_values, num_values)
    self.cli.update_row("name", "get_row", d)
    row_names = self.cli.get_all_rows("name")
    self.assertEqual(row_names, ["get_row"])

  def test_clear(self):
    self.cli.clear("name")

  def test_calcs(self):
    string_values = [("key1", "val1"), ("key2", "val2")]
    num_values = [("key1", 1.0), ("key2", 2.0)]
    d = datum(string_values, num_values)
    self.assertAlmostEqual(self.cli.similarity("name", d, d), 1, 6)
    self.assertAlmostEqual(self.cli.l2norm("name", d), sqrt(1*1 + 1*1+ 1*1 + 2*2), 6)

  def test_clear(self):
    self.cli.clear("name")

  def test_save(self):
    self.assertEqual(self.cli.save("name", "classifier.save_test.model"), True)

  def test_load(self):
    model_name = "classifier.load_test.model"
    self.cli.save("name", model_name)
    self.assertEqual(self.cli.load("name", model_name), True)

  def test_get_status(self):
    self.cli.get_status("name")



if __name__ == '__main__':
  test_suite = unittest.TestLoader().loadTestsFromTestCase(RecommenderTest)
  unittest.TextTestRunner().run(test_suite)

