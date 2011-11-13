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

from jubatus import config
from jubatus.accessor import Accessor, MPClientFunc


class Classifier(Accessor):
    """Classifier client for jubatus."""

    def set_config(self, config):
        f = MPClientFunc(self.choose_one(), 'set_config')
        try:
            (success, retval, error) = f(self.name, Classifier.Config(config).pack())
            if not success:
                raise RuntimeError(error)
        except RuntimeError, e:
            return error
        return retval

    def get_config(self):
        f = MPClientFunc(self.choose_one(), 'get_config')
        (success, retval, error) = f(self.name)
        if not success:
            raise RuntimeError(error)

        c = {'converter': {}}
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

    def train(self, label2data):
        f = MPClientFunc(self.choose_one(), 'train')
        try:
            (success, retval, error) = f(self.name, label2data)
            if not success:
                raise RuntimeError(error)
        except RuntimeError, e:
               return error
        return retval

    def classify(self, data):
        f = MPClientFunc(self.choose_one(), 'classify')
        try:
            (success, retval, error) = f(self.name, data)
            if not success:
                raise RuntimeError(error)
        except RuntimeError, e:
               return error
        return map(lambda t: list(t), retval)

    def get_status(self):
        f = MPClientFunc(self.choose_one(), 'get_status')
        try:
            (success, retval, error) = f(self.name)
            if not success:
                  raise RuntimeError(error)
        except RuntimeError, e:
               return error
        return retval


    class Config:
        """Spec is derived from server/rpc.hpp: struct classifier_config_data"""

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
                config.pack_num_rules(converter_config)
            ]

        def pack(self):
#            print [self.method, self.converter]
            return [self.method, self.converter]
