#!/usr/bin/env python

import unittest
import json
import msgpackrpc

from math import sqrt

from jubatus.stat.client import Stat
from jubatus.stat.types import *
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
        try:
            self.cli = Stat(host, port, 'name')
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

    def test_sum(self):
        self.cli.push("sum", 1.0)
        self.cli.push("sum", 2.0)
        self.cli.push("sum", 3.0)
        self.cli.push("sum", 4.0)
        self.cli.push("sum", 5.0)
        self.assertEqual(self.cli.sum("sum"), 15.0)

    def test_stddev(self):
        self.cli.push("stddev", 1.0)
        self.cli.push("stddev", 2.0)
        self.cli.push("stddev", 3.0)
        self.cli.push("stddev", 4.0)
        self.cli.push("stddev", 5.0)
        self.assertEqual(self.cli.stddev("stddev"), sqrt(2.0))

    def test_max(self):
        self.cli.push("max", 1.0)
        self.cli.push("max", 2.0)
        self.cli.push("max", 3.0)
        self.cli.push("max", 4.0)
        self.cli.push("max", 5.0)
        self.assertEqual(self.cli.max("max"), 5.0)

    def test_min(self):
        self.cli.push("min", 1.0)
        self.cli.push("min", 2.0)
        self.cli.push("min", 3.0)
        self.cli.push("min", 4.0)
        self.cli.push("min", 5.0)
        self.assertEqual(self.cli.min("min"), 1.0)

    def test_entropy(self):
        self.cli.push("entropy", 1.0)
        self.cli.push("entropy", 2.0)
        self.cli.push("entropy", 3.0)
        self.cli.push("entropy", 4.0)
        self.cli.push("entropy", 5.0)
        self.assertEqual(self.cli.entropy("entropy"), 0.0)

    def test_moment(self):
        self.cli.push("moment", 1.0)
        self.cli.push("moment", 2.0)
        self.cli.push("moment", 3.0)
        self.cli.push("moment", 4.0)
        self.cli.push("moment", 5.0)
        self.assertEqual(self.cli.moment("moment", 1, 1.0), 2.0)

    def test_save(self):
        self.assertEqual(len(self.cli.save("stat.save_test.model")), 1)

    def test_load(self):
        model_name = "stat.load_test.model"
        self.cli.save(model_name)
        self.assertEqual(self.cli.load(model_name), True)

    def test_get_status(self):
        self.cli.get_status()

if __name__ == '__main__':
    test_suite = unittest.TestLoader().loadTestsFromTestCase(StatTest)
    unittest.TextTestRunner().run(test_suite)

