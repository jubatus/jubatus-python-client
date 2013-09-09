import msgpackrpc
import unittest
import jubatus.common

# When a given method is not supported, jubatus-rpc server returns error code 1
class AlwaysRaiseUnknownMethod:
    def call(self, method, *args):
        raise msgpackrpc.error.RPCError(1)

# When given arguments cannot be parsed, jubatus-rpc server returns error code 2
class AlwaysRaiseTypeMismatch:
    def call(self, method, *args):
        raise msgpackrpc.error.RPCError(2)

class Echo:
    def call(self, method, *args):
        return method

class AnyType:
    def to_msgpack(self, v):
        return v

    def from_msgpack(self, v):
        return v

class ClientTest(unittest.TestCase):
    def test_unknown_method(self):
        c = jubatus.common.Client(AlwaysRaiseUnknownMethod(), "name")
        self.assertRaises(jubatus.common.UnknownMethod, c.call, "test", [], None, [])

    def test_type_mismatch(self):
        c = jubatus.common.Client(AlwaysRaiseTypeMismatch(), "name")
        self.assertRaises(jubatus.common.TypeMismatch, c.call, "test", [], None, [])

    def test_wrong_number_of_arguments(self):
        c = jubatus.common.Client(Echo(), "name")
        self.assertEquals("test", c.call("test", [], AnyType(), []))

if __name__ == '__main__':
    unittest.main()
