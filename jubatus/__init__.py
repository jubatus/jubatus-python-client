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
import msgpack
import socket
import random # FIXME: same seeds may make DoS attack to each server

import config

MAX_CALL_ID = 65535 # should be max int supported by msgpack

class MethodNotFound(Exception): pass
class TypeMismatch(Exception): pass
class BadRPC(Exception): pass

class MPClientFunc:
    ''' simple msgpack-rpc client. currently it connect and disconnect
    at each RPC but connection lifetime should be same as object lifetime.
    Because of RPC interface of Jubatus server, one TCP connection holds
    one server-thread and the server cannot increase threads.
    Thus the server cannot hold so many TCP connections.  '''
    def __init__(self, host, meth, timeout = 10):
        self.host = host[0]
        self.port = host[1]
        self.meth = meth
        self.timeout = timeout
        self.unpacker = msgpack.Unpacker()
#        print self.host, self.port, self.meth

    def __call__(self, *argv):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.timeout)
        # TODO: not available in Debian...
        # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        s.connect((self.host, self.port))
        i = random.randint(0, MAX_CALL_ID)
#        print "sending: ", [0,i,self.meth,argv], "to", (self.host, self.port)
        s.sendall(msgpack.packb([0, i, self.meth, argv]))
        buf = s.recv(4096)
        s.close()
#        print len(buf), buf, ":\n"
        self.unpacker.feed(buf)
        for o in self.unpacker: # o => [1, cid, None, RetVal] or [1, cid, ErrCode, None]
            if len(o) != 4: raise BadRPC(o)
            elif o[0] != 1: raise BadRPC(o)
            elif o[1] != i: raise BadRPC(o)
            elif o[2] != None:
                if o[2] == 1:   raise MethodNotFound
                elif o[2] == 2:
                    print "recvd: ", o 
                    raise TypeMismatch
                else:           raise o[2]
            else: return o[3]

class Accessor:
    def __init__(self, hosts, name):
        self.servers = map(lambda x: (x.split(':')[0], int(x.split(':')[1])), hosts.split(','))
        self.name = name

    def choose_one(self):
        i = random.randint(0, len(self.servers)-1)
        return self.servers[i]

    def save(self, id_):
        srv = self.choose_one()
        try:
            f = MPClientFunc(srv, 'save')
            (success, retval, error) = f(self.name, "classifier", id_)
            if (not success) :
                raise RuntimeError(error)
        except RuntimeError, e:
            return error
        return success

    def load(self, id_): 
        srv = self.choose_one()
        try:
            f = MPClientFunc(srv, 'load')
            (success, retval, error) = f(self.name, "classifier", id_)
            if (not success) :
                raise RuntimeError(error)
        except RuntimeError, e:
            return error
        return success

class Classifier(Accessor):
    def set_config(self,config):
        srv = self.choose_one()
        try:
            f = MPClientFunc(srv, 'set_config')
            (success, retval, error) = f( self.name, Classifier.Config(config).pack() )
            if (not success) :
                raise RuntimeError(error)
        except RuntimeError, e:
            return error
        return retval

    def get_config(self):
        f = MPClientFunc(self.choose_one(), 'get_config')
        (success, retval, error) = f( self.name )
        if (not success) :
            raise RuntimeError(error)
        c = {'converter':{}}
        c['method'] = retval[0]
        config.unpack_string_filter_types(retval[1][0], c['converter'])
        config.unpack_string_filter_rules(retval[1][1], c['converter'])
        config.unpack_num_filter_types(retval[1][2], c['converter'])
        config.unpack_num_filter_rules(retval[1][3], c['converter'])
        config.unpack_string_types(retval[1][4], c['converter'])
        config.unpack_string_rules(retval[1][5], c['converter'])
        config.unpack_num_types(retval[1][6], c['converter'])
        config.unpack_num_rules(retval[1][7], c['converter'])
        return c

    def train(self,label2data):
        f = MPClientFunc(self.choose_one(), 'train')
        try:
            (success, retval, error) = f(self.name, label2data)
            if (not success) :
                raise RuntimeError(error)
        except RuntimeError, e:
               return error
        return retval

    def classify(self,data):
        f = MPClientFunc(self.choose_one(), 'classify')
        try:
            (success, retval, error) = f(self.name, data)
            if (not success) :
                raise RuntimeError(error)
        except RuntimeError, e:
               return error
        return map(lambda t: list(t), retval)

    def get_status(self):
        srv = self.choose_one()
        try:
            f = MPClientFunc(srv, 'get_status')
            (success, retval, error) = f()
            if (not success):
                  raise RuntimeError(error)
        except RuntimeError, e:
               return error
        return retval

    class Config:
        ''' spec is derived from server/rpc.hpp: struct classifier_config_data '''
        def __init__(self, dict_config):
            self.method = dict_config['method']
            converter_config = dict_config['converter']
            self.converter = [
                config.pack_string_filter_types(converter_config),
                config.pack_string_filter_rules(converter_config),
                config.pack_num_filter_types(converter_config),
                config.pack_num_filter_rules(converter_config),
                config.pack_string_types(converter_config),
                config.pack_string_rules(converter_config),
                config.pack_num_types(converter_config),
                config.pack_num_rules(converter_config),
                ]

        def pack(self):
#            print [self.method, self.converter]
            return [self.method, self.converter] 
