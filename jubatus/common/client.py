import msgpackrpc
from .types import *

class InterfaceMismatch(Exception):
    pass
class TypeMismatch(InterfaceMismatch):
    pass
class UnknownMethod(InterfaceMismatch):
    pass

def error_handler(e):
    if e == 1:
        raise UnknownMethod()
    elif e == 2:
        # TODO(unno) we cannot get which arugment is illegal
        raise TypeMismatch()
    else:
        raise msgpackrpc.error.RPCError(e)

class Client(object):
    def __init__(self, client, name):
        self.client = client
        self.name = name

    def call(self, method, args, ret_type, args_type):
        if len(args) != len(args_type):
            # This error does not occurr if a client code is correctly generated
            message = "\"%s\" takes %d argument, but %d given" \
                % (method, len(args_type), len(args))
            raise TypeError(message)

        values = [self.name]
        for (v, t) in zip(args, args_type):
            values.append(t.to_msgpack(v))

        future = self.client.call_async(method, *values)
        future.attach_error_handler(error_handler)
        ret = future.get()

        if ret_type != None:
            return ret_type.from_msgpack(ret)

class ClientBase(object):
    """
    Notes regarding MessagePack coding:
    - Data sent via RPC may contain both Unicode string (unicode in Py2, str in Py3)
      and Bytes (str in Py2, bytes in Py3.)
    - MessagePack spec does not distinguish these two (both are RAW.)
    - When packing, we let MessagePack library to encode all Unicode as RAW bytes
      in UTF-8 representation. (`pack_encoding='utf-8'`)
    - When unpacking, we cannot let MessagePack library to decode RAW bytes,
      as MessagePack library cannot tell whether it is a Unicode or a Bytes.
      We manually decode RAW data into Unicode or Bytes in type conversion.
      (`unpack_encoding=None`)
    """
    def __init__(self, host, port, name, timeout=10):
        address = msgpackrpc.Address(host, port)
        self.client = msgpackrpc.Client(address, timeout=timeout, pack_encoding='utf-8', unpack_encoding=None)
        self.jubatus_client = Client(self.client, name)

    def get_client(self):
        return self.client

    def get_name(self):
        return self.jubatus_client.name

    def set_name(self, name):
        self.jubatus_client.name = name

    def save(self, id):
        return self.jubatus_client.call("save", [id], TMap(TString(), TString()), [TString()])

    def load(self, id):
      return self.jubatus_client.call("load", [id], TBool(), [TString()])

    def do_mix(self):
        return self.jubatus_client.call("do_mix", [], TBool(), [])

    def get_config(self):
        return self.jubatus_client.call("get_config", [], TString(), [])

    def get_status(self):
        return self.jubatus_client.call(
            "get_status",
            [],
            TMap(TString(), TMap(TString(), TString())),
            [])

    def get_proxy_status(self):
        return self.jubatus_client.call(
            "get_proxy_status",
            [],
            TMap(TString(), TMap(TString(), TString())),
            [])
