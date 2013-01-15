#!/usr/bin/env python

import unittest
import json

from math import sqrt

from jubatus.stat.client import stat
from jubatus.stat.types  import *
from jubatus_test.test_util import TestUtil

host = "127.0.0.1"
port = 21004
timeout = 10

class StatTest(unittest.TestCase):
  def setUp(self):
    self.config = {
        "window_size": 10
    }

    TestUtil.write_file('config_stat.json', json.dumps(self.config))
    self.srv = TestUtil.fork_process('stat', port, 'config_stat.json')
    self.cli = stat(host, port)

  def tearDown(self):
    TestUtil.kill_process(self.srv)

  def test_get_config(self):
    config = self.cli.get_config("name")
    self.assertEqual(json.dumps(json.loads(config), sort_keys=True), json.dumps(self.config, sort_keys=True))

  def test_sum(self):
    self.cli.push("name", "sum", 1.0)
    self.cli.push("name", "sum", 2.0)
    self.cli.push("name", "sum", 3.0)
    self.cli.push("name", "sum", 4.0)
    self.cli.push("name", "sum", 5.0)
    self.assertEqual(self.cli.sum("name", "sum"), 15.0)

  def test_stddev(self):
    self.cli.push("name", "stddev", 1.0)
    self.cli.push("name", "stddev", 2.0)
    self.cli.push("name", "stddev", 3.0)
    self.cli.push("name", "stddev", 4.0)
    self.cli.push("name", "stddev", 5.0)
    self.assertEqual(self.cli.stddev("name", "stddev"), sqrt(2.0))

  def test_max(self):
    self.cli.push("name", "max", 1.0)
    self.cli.push("name", "max", 2.0)
    self.cli.push("name", "max", 3.0)
    self.cli.push("name", "max", 4.0)
    self.cli.push("name", "max", 5.0)
    self.assertEqual(self.cli.max("name", "max"), 5.0)

  def test_min(self):
    self.cli.push("name", "min", 1.0)
    self.cli.push("name", "min", 2.0)
    self.cli.push("name", "min", 3.0)
    self.cli.push("name", "min", 4.0)
    self.cli.push("name", "min", 5.0)
    self.assertEqual(self.cli.min("name", "min"), 1.0)

  def test_entropy(self):
    self.cli.push("name", "entropy", 1.0)
    self.cli.push("name", "entropy", 2.0)
    self.cli.push("name", "entropy", 3.0)
    self.cli.push("name", "entropy", 4.0)
    self.cli.push("name", "entropy", 5.0)
    self.assertEqual(self.cli.entropy("name", "entropy"), 0.0)

  def test_moment(self):
    self.cli.push("name", "moment", 1.0)
    self.cli.push("name", "moment", 2.0)
    self.cli.push("name", "moment", 3.0)
    self.cli.push("name", "moment", 4.0)
    self.cli.push("name", "moment", 5.0)
    self.assertEqual(self.cli.moment("name", "moment", 1, 1.0), 2.0)

  def test_save(self):
    self.assertEqual(self.cli.save("name", "stat.save_test.model"), True)

  def test_load(self):
    model_name = "stat.load_test.model"
    self.cli.save("name", model_name)
    self.assertEqual(self.cli.load("name", model_name), True)

  def test_get_status(self):
    self.cli.get_status("name")



if __name__ == '__main__':
  test_suite = unittest.TestLoader().loadTestsFromTestCase(StatTest)
  unittest.TextTestRunner().run(test_suite)

