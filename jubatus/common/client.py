import msgpackrpc

class TypeMismatch(Exception):
    pass
class UnknownMethod(Exception):
    pass

def translate_error(e):
    if e.message == 1:
        raise UnknownMethod()
    elif e.message == 2:
        # TODO(unno) we cannot get which arugment is illegal
        raise TypeMismatch()
    else:
        raise e

class Client:
    def __init__(self, client):
        self.client = client

    def call(self, method, args, ret_type, args_type):
        if len(args) != len(args_type):
            # This error does not occurr if a client code is correctly generated
            message = "\"%s\" takes %d argument, but %d given" \
                % (method, len(args_type), len(args))
            raise TypeError(message)

        values = []
        for (v, t) in zip(args, args_type):
            values.append(t.to_msgpack(v))

        try:
            ret = self.client.call(method, *values)
        except msgpackrpc.error.RPCError, e:
            translate_error(e)

        if ret_type != None:
            return ret_type.from_msgpack(ret)
