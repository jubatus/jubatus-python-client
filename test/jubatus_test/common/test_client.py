import msgpackrpc
import unittest
import jubatus.common

class DummyFuture(object):
    def __init__(self, response, error):
        self.response = response
        self.error = error
        self.handler = None

    def attach_error_handler(self, handler):
        self.handler = handler

    def get(self):
        if self.error:
            if self.handler:
                self.handler(self.error)
            else:
                raise msgpack.rpc.error.RPCError(self.error)
        else:
            return self.response

class DummyClient(object):
    def call_async(self, method, *args):
        return self.send_request(method, args)

# When a given method is not supported, jubatus-rpc server returns error code 1
class AlwaysRaiseUnknownMethod(DummyClient):
    def send_request(self, method, args):
        return DummyFuture(None, 1)

# When given arguments cannot be parsed, jubatus-rpc server returns error code 2
class AlwaysRaiseTypeMismatch(DummyClient):
    def send_request(self, method, args):
        return DummyFuture(None, 2)

class AlwaysRaiseRemoteError(DummyClient):
    def send_request(self, method, args):
        return DummyFuture(None, "error")

class Echo(DummyClient):
    def send_request(self, method, args):
        return DummyFuture(method, None)

class AnyType(object):
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

    def test_remote_error(self):
        c = jubatus.common.Client(AlwaysRaiseRemoteError(), "name")
        self.assertRaises(msgpackrpc.error.RPCError, c.call, "test", [], None, [])

    def test_wrong_number_of_arguments(self):
        c = jubatus.common.Client(Echo(), "name")
        self.assertEqual("test", c.call("test", [], AnyType(), []))
        self.assertRaises(TypeError, c.call, "test", [1], AnyType(), [])

if __name__ == '__main__':
    unittest.main()
