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
import jubatus
import time
import unittest
from subprocess import *

class jubatusTest(unittest.TestCase):

    def setUp(self):
        self.jubatus_pid = Popen(['jubaclassifier', '--name=TEST'], stderr=PIPE)
        time.sleep(1.0)
        self.cl = jubatus.Classifier("localhost:9199", "TEST")
        self.config = {
          'converter': {
            "string_filter_types": {
            "detag": { "method": "regexp", "pattern": "<[^>]*>", "replace": "" }
            },
            "string_filter_rules":
            [
              { "key": "message", "type": "detag", "suffix": "-detagged" }
            ],
            "num_filter_types": {
              "add_1": { "method": "add", "value": "1" }
            },
            "num_filter_rules": [
              { "key": "user/age", "type": "add_1", "suffix": "_kazoe" }
            ],
            "string_types": {
#                "dic1":  { "method": "ux", "path": "../../fv_converter/test_input/keywords" }
            },
            "string_rules":
            [
              { "key": "user/name", "type": "str",
              "sample_weight": "bin", "global_weight": "bin" },
#              { "key": "message", "type": "dic1",
#                "sample_weight": "tf",  "global_weight": "bin" },
              { "key": "message-detagged", "type": "space",
                "sample_weight": "bin",  "global_weight": "bin" }
            ],
        "num_types":
        {},
        "num_rules":
        [
          { "key": "user/id",  "type": "str" },
          { "key": "user/age", "type": "num" },
          { "key": "user/income", "type": "log" },
          { "key": "user/age_kazoe", "type": "num" }
        ]
      },
      'method': 'PA',
    }

        self.config_num = {
                'converter': {
                    'string_filter_types': {},
                    'string_filter_rules': [],
                    'num_filter_types': {},
                    'num_filter_rules': [],
                    'string_types': {},
                    'string_rules': [],
                    'num_types': {},
                    'num_rules': [ { "key": "*", "type": "num" }]
                    },
                'method': "PA",
                }

        self.config_str = {
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

        self.config_null = {
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

        self.tdata_num_1 = [('001', ([], [["a", 1.0]]) , )]
        self.cdata_num_1 = [        ([], [["a", 1.0]])]

        self.tdata_str_1 = [('001', ([["a", "abc"]], []) , )]
        self.cdata_str_1 = [        ([["a", "abc"]], [])]

        self.tdata_str_2 = [('002', ([["a", "cba"]], []) , )]
        self.cdata_str_2 = [        ([["a", "cba"]], [])]



    def tearDown(self):
        self.jubatus_pid.kill()

    def isAlive(self):
        if self.jubatus_pid.poll() == None:
            return True
        else:
            return False

    def test_000_setconfig1(self):
        self.assertEqual(0 , self.cl.set_config(self.config))
        self.assertTrue(self.isAlive())        
    
    def test_000_setconfig2(self):
        self.assertEqual(0 , self.cl.set_config(self.config_num))
        self.assertTrue(self.isAlive())        

    def test_000_setconfig3(self):
        self.assertEqual(0 , self.cl.set_config(self.config_str))
        self.assertTrue(self.isAlive())        


    def test_001_getconfig1(self):
        self.cl.set_config(self.config)
        self.assertEqual(self.config, self.cl.get_config())
        self.assertTrue(self.isAlive())        

    def test_001_getconfig2(self):
        self.cl.set_config(self.config_num)
        self.assertEqual(self.config_num, self.cl.get_config())
        self.assertTrue(self.isAlive())        

    def test_001_getconfig3(self):
        self.cl.set_config(self.config_str)
        self.assertEqual(self.config_str, self.cl.get_config())
        self.assertTrue(self.isAlive())        


    def test_002_train20(self):
        self.cl.set_config(self.config_num)
        self.assertEqual(True ,self.cl.train(self.tdata_num_1))
        self.assertTrue(self.isAlive())        
        
    def test_002_train21(self):
        self.cl.set_config(self.config_num)
        self.cl.train(self.tdata_num_1)
        self.assertEqual(True ,self.cl.train(self.tdata_num_1))
        self.assertTrue(self.isAlive())        

    def test_002_train30(self):
        self.cl.set_config(self.config_str)
        self.assertEqual(True ,self.cl.train(self.tdata_str_1))
        self.assertTrue(self.isAlive())        
 
    def test_002_train30(self):
        self.cl.set_config(self.config_str)
        self.cl.train(self.tdata_str_1)
        self.assertEqual(True ,self.cl.train(self.tdata_str_1))
        self.assertTrue(self.isAlive())        

    def test_003_classify2(self):
        self.cl.set_config(self.config_num)
        self.cl.train(self.tdata_num_1)
        self.assertEqual([[('001', 1.0)]], self.cl.classify(self.cdata_num_1))
        self.assertTrue(self.isAlive())        

    def test_003_classify3(self):
        self.cl.set_config(self.config_str)
        self.assertEqual(True ,self.cl.train(self.tdata_str_1))
        self.assertEqual([[('001', 1.0)]], self.cl.classify(self.cdata_str_1))
        self.assertTrue(self.isAlive())        

    def test_004_get_status2(self):
        self.cl.set_config(self.config_num)
        self.cl.train(self.tdata_num_1)
        self.assertEqual(1 ,len(self.cl.get_status()))
        self.assertTrue(self.isAlive())        

    def test_004_get_status3(self):
        self.cl.set_config(self.config_str)
        self.cl.train(self.tdata_str_1)
        self.assertEqual(1 ,len(self.cl.get_status()))
        self.assertTrue(self.isAlive())        

    def test_004_get_status4(self):
        self.cl.set_config(self.config_str)
        self.assertEqual(1 ,len(self.cl.get_status()))
        self.assertTrue(self.isAlive())        
            
    def test_006_save1(self):
        self.cl.set_config(self.config_num)
        self.cl.train(self.tdata_num_1)
        self.assertEqual(1, self.cl.save("num"))
        self.assertTrue(self.isAlive())        

    def test_006_save2(self):
        self.cl.set_config(self.config_str)
        self.cl.train(self.tdata_str_1)
        self.assertEqual(1, self.cl.save("str"))
        self.assertTrue(self.isAlive())        

    def test_007_load1(self):
        self.assertEqual(1, self.cl.load("num"))
        self.assertTrue(self.isAlive())        

    def test_007_load2(self):
        self.assertEqual(1, self.cl.load("str"))
        self.assertTrue(self.isAlive())        

    def test_007_load3(self):
        self.cl.load("str")
        self.cl.set_config(self.config_str)
        self.assertEqual([[('001', 1.0)]], self.cl.classify(self.cdata_str_1))        
        self.assertTrue(self.isAlive())        

    def test_007_load4(self):
        self.cl.load("str")
        self.cl.set_config(self.config_str)
        self.assertEqual(True, self.cl.train(self.tdata_str_1))
        self.assertTrue(self.isAlive())        

    def test_007_load5(self):
        self.assertTrue(self.cl.load("null").find("cannot open") != -1) # not exist
        self.assertTrue(self.isAlive())        

    def test_007_load6(self):
        self.cl.set_config(self.config_str)
        self.cl.train(self.tdata_str_1)
        self.cl.save("str")
        self.cl.load("str")
        self.cl.set_config(self.config_str)
        self.assertEqual([[('001', 1.0)]], self.cl.classify(self.cdata_str_1))
        self.assertTrue(self.isAlive())        

    def test_008_load7(self):
        self.cl.set_config(self.config_str)
        self.cl.train(self.tdata_str_1)
        self.cl.save("str_t7")
        self.cl.load("str_t7")
        self.cl.set_config(self.config_str)
        self.cl.save("str_t72")
        self.assertTrue(self.isAlive())        

    def test_100_senario0(self):
        pass


    def test_901_classifiy_before_train(self):
        self.cl.set_config(self.config_str)
        self.assertEqual([[]], self.cl.classify(self.cdata_str_1))         
        self.assertTrue(self.isAlive())        


    def test_902_not_config1(self):
        self.assertEqual(self.config_null ,self.cl.get_config())
        self.assertTrue(self.isAlive())        

    def test_902_not_config2(self):
        self.assertEqual("config_not_set" ,self.cl.train(self.tdata_str_1))
        self.assertTrue(self.isAlive())        

    def test_902_not_config3(self):
        self.assertEqual("config_not_set" ,self.cl.classify(self.cdata_str_1))
        self.assertTrue(self.isAlive())        

    def test_902_not_config4(self):
        self.assertEqual(1 ,len(self.cl.get_status()))
        self.assertTrue(self.isAlive())        

    def test_902_not_config6(self):
        self.assertEqual(1 ,self.cl.save("TEST"))
        self.assertTrue(self.isAlive())        

    def test_902_not_config7(self):
        self.assertEqual(1 ,self.cl.load("TEST"))
        self.assertTrue(self.isAlive())        







    
if __name__ == '__main__':
    
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

    tdata_num_1 = [('001', ([], [["a", 1.0]]) , )]
    cdata_num_1 = [        ([], [["a", 1.0]])]

    tdata_str_1 = [('001', ([["a", "abc"]], []) , )]
    cdata_str_1 = [        ([["a", "abc"]], [])]

    tdata_str_2 = [('002', ([["a", "cba"]], []) , )]
    cdata_str_2 = [        ([["a", "cba"]], [])]

    
    test_suite = unittest.TestLoader().loadTestsFromTestCase(jubatusTest)
    unittest.TextTestRunner(verbosity=2).run(test_suite)

def suite():
    test_suite = unittest.TestLoader().loadTestsFromTestCase(jubatusTest)
    return test_suite

