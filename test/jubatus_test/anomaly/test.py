#!/usr/bin/env python

import unittest

import json
from math import sqrt

from jubatus.anomaly.client import anomaly
from jubatus.anomaly.types  import *
from jubatus_test.test_util import TestUtil

host = "127.0.0.1"
port = 21006
timeout = 10

class anomalyTest(unittest.TestCase):
  def setUp(self):
    self.config = {
     "method": "lof",
     "converter" : {
       "string_filter_types" : {},
       "string_filter_rules" : [],
       "num_filter_types" : {},
       "num_filter_rules" : [],
       "string_types" : {},
       "string_rules" : [{"key" : "*", "type" : "space", "sample_weight" : "bin", "global_weight" : "bin"}],
       "num_types" : {},
       "num_rules" : [{"key" : "*","type" : "num"}]
     },
     "parameter": {
       "nearest_neighbor_num": 10,
       "reverse_nearest_neighbor_num": 30,
       "method": "euclid_lsh",
       "parameter": {
         "lsh_num": 8,
         "table_num": 16,
         "probe_num": 64,
         "bin_width": 10.0,
         "seed": 1091,
         "retain_projection": False
       }
     }
    }

    TestUtil.write_file('config_anomaly.json', json.dumps(self.config))
    self.srv = TestUtil.fork_process('anomaly', port, 'config_anomaly.json')
    self.cli = anomaly(host, port)

  def tearDown(self):
    TestUtil.kill_process(self.srv)

  def test_clear_row(self):
    d = datum([], [])
    (row_id, score) = self.cli.add("name", d)
    self.assertEqual(self.cli.clear_row("name", row_id), True)
    # TODO: return true when non existent id ..
    # self.assertEqual(self.cli.clear_row("name", "non-existent-id"), False)

  def test_add(self):
    d = datum([], [])
    (row_id, score) = self.cli.add("name", d)

  def test_update(self):
    d = datum([], [])
    (row_id, score) = self.cli.add("name", d)
    d = datum([], [('val', 3.1)])
    score = self.cli.update("name", row_id, d)

  def test_clear(self):
    self.assertEqual(self.cli.clear("name"), True)

  def test_calc_score(self):
    d = datum([], [('val', 1.1)])
    (row_id, score) = self.cli.add("name", d)
    d = datum([], [('val', 3.1)])
    score = self.cli.calc_score("name", d)

  def test_get_all_rows(self):
    self.cli.get_all_rows("name")

  def test_get_config(self):
    config = self.cli.get_config("name")
    self.assertEqual(json.dumps(json.loads(config), sort_keys=True), json.dumps(self.config, sort_keys=True))

  def test_save(self):
    self.assertEqual(self.cli.save("name", "anomaly.save_test.model"), True)

  def test_load(self):
    model_name = "anomaly.load_test.model"
    self.cli.save("name", model_name)
    self.assertEqual(self.cli.load("name", model_name), True)

  def test_get_status(self):
    self.cli.get_status("name")

if __name__ == '__main__':
  test_suite = unittest.TestLoader().loadTestsFromTestCase(anomalyTest)
  unittest.TextTestRunner().run(test_suite)

