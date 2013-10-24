import unittest
import json
import msgpackrpc
import jubatus.common
from jubatus_test.test_util import TestUtil

host = "127.0.0.1"
port = 21000
timeout = 10

class ErrorTest(unittest.TestCase):
    def setUp(self):
        self.config = {
            "method": "AROW",
            "converter": {
                "string_filter_types": {},
                "string_filter_rules": [],
                "num_filter_types": {},
                "num_filter_rules": [],
                "string_types": {},
                "string_rules": [],
                "num_types": {},
                "num_rules": []
                },
            "parameter": {
                "regularization_weight": 1.001
                }
            }

        TestUtil.write_file('config_for_error.json', json.dumps(self.config))
        self.srv = TestUtil.fork_process('classifier', port, 'config_for_error.json')
        try:
            address = msgpackrpc.Address(host, port)
            client = msgpackrpc.Client(address)
            self.cli = jubatus.common.Client(client, "name")
        except:
            TestUtil.kill_process(self.srv)
            raise

    def tearDown(self):
        TestUtil.kill_process(self.srv)

    def testUnknownMethod(self):
        self.assertRaises(jubatus.common.UnknownMethod, lambda:
                              self.cli.call("unknown_method", [], None, []))

    def testTypeMismatch(self):
        self.assertRaises(jubatus.common.TypeMismatch, lambda:
                              self.cli.call("train", [""], None,
                                            [jubatus.common.TString()]))
