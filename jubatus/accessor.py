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

import random # FIXME: same seeds may make DoS attack to each server
import socket

import msgpack

from jubatus.error import *


MAX_CALL_ID = 65535 # should be max int supported by msgpack


class MPClientFunc:
    """Simple msgpack-rpc client. currently it connect and disconnect
    at each RPC but connection lifetime should be same as object lifetime.
    Because of RPC interface of Jubatus server, one TCP connection holds
    one server-thread and the server cannot increase threads.
    Thus the server cannot hold so many TCP connections."""

    def __init__(self, host, method, timeout=10):
        self.host = host[0]
        self.port = host[1]
        self.method = method
        self.timeout = timeout
        self.unpacker = msgpack.Unpacker()
#        print self.host, self.port, self.method

    def __call__(self, *argv):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.timeout)
        # TODO: not available in Debian...
        # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        s.connect((self.host, self.port))
        i = random.randint(0, MAX_CALL_ID)
#        print "sending: ", [0, i, self.method, argv], "to", (self.host, self.port)
        s.sendall(msgpack.packb([0, i, self.method, argv]))

        while True:
            buf = s.recv(4096)
            self.unpacker.feed(buf)
                
            for o in self.unpacker:
                # o => [1, cid, None, RetVal] or [1, cid, ErrCode, None]
                s.close()
                if len(o) != 4:
                    raise BadRPCError(o)
                elif o[0] != 1:
                    raise BadRPCError(o)
                elif o[1] != i:
                    raise BadRPCError(o)
                elif o[2] is not None:
                    if o[2] == 1:
                        raise MethodNotFoundError
                    elif o[2] == 2:
                        raise TypeMismatchError
                    else:
                        raise o[2]
                else:
                    return o[3]

class Accessor:
    """Base class for jubatus API."""

    def __init__(self, hosts, name):
        self.servers = map(lambda x: (x.split(':')[0], int(x.split(':')[1])), hosts.split(','))
        self.name = name

    def choose_one(self):
        i = random.randint(0, len(self.servers) - 1)
        return self.servers[i]

    def save(self, id_):
        f = MPClientFunc(self.choose_one(), 'save')
        retval = f(self.name, "classifier", id_)
        return retval

    def load(self, id_): 
        f = MPClientFunc(self.choose_one(), 'load')
        retval = f(self.name, "classifier", id_)
        return retval
