#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Jubatus: Online machine learning framework for distributed environment
# Copyright (C) 2011 Preferred Infrastracture and Nippon Telegraph and Telephone Corporation.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

import sys
import time
import unittest
from subprocess import *

import jubatus


class jubatusTest(unittest.TestCase):
    def setUp(self):
        pass
#        self.jubatus0_pid = Popen(['jubatus_classifier_server', '--name=TESTM --http-port=8090 --rpc-port=9190 --storage=local_mixture --zookeeper=localhost:2181'], stderr=PIPE)
#        self.jubatus1_pid = Popen(['jubatus_classifier_server', '--name=TESTM --http-port=8091 --rpc-port=9191 --storage=local_mixture --zookeeper=localhost:2181'], stderr=PIPE)
#        time.sleep(0.3)

    def tearDown(self):
        pass
 #       self.jubatus0_pid.kill()
 #       self.jubatus1_pid.kill()
 #       time.sleep(1)

    def isAlive(self):
        if self.jubatus_pid.poll() is None:
            return True
        else:
            return False

    def test_000_setconfig1(self):
        pass
#        FIXME
#        self.assertEqual(2 , cl.set_config(config_str))
#        self.assertEqual(True, self.isAlive())

    
if __name__ == '__main__':
    zk_pid = Popen(['zkServer.sh', 'start'], stderr=PIPE)
    time.sleep(1)
    semimaster_pid = Popen(['semimaster', '--zookeeper=localhost:2181'])

    cl = jubatus.Classifier("localhost:9198", "TESTM", True)

    config_str = {
        'converter': {
            'string_filter_types': {},
            'string_filter_rules': [],
            'num_filter_types': {},
            'num_filter_rules': [],
            'string_types': {},
            'string_rules': [
                {'key':'*','type':'space','sample_weight':'bin','global_weight':'bin'}
            ],
            'num_types': {},
            'num_rules': []
        },
        'method': "PA",
    }

    config_null = {
        'converter': {
            'string_filter_types': {},
            'string_filter_rules': [],
            'num_filter_types': {},
            'num_filter_rules': [],
            'string_types': {},
            'string_rules': [],
            'num_types': {},
            'num_rules': []
        },
        'method': "",
    }

    tdata_str_1 = [('001', ([["a", "abc"]], ), )]
    cdata_str_1 = [        ([["a", "abc"]], )]

    test_suite = unittest.TestLoader().loadTestsFromTestCase(jubatusTest)
    unittest.TextTestRunner(verbosity=2).run(test_suite)

    semimaster_pid.kill()
    zk_pid = Popen(['zkServer.sh', 'stop'], stderr=PIPE)                                                                                               
