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

"""
config.py convert json-style config to msgpack-API compatible data structure
need metaprogramming: we'll have much better way with schema or IDL
"""

# "filter_types" : { string : { string : string } } ->  { string : { string : string } } 
def pack_string_filter_types(c_config):
    return c_config['string_filter_types'] if 'string_filter_types' in c_config else {}

def pack_num_filter_types(c_config):
    return c_config['num_filter_types'] if 'num_filter_types' in c_config else {}

def unpack_string_filter_types(config, c_config):
    c_config['string_filter_types'] = config

def unpack_num_filter_types(config, c_config):
    c_config['num_filter_types'] = config

# "filter_rules" : [ {"key": key, "type":type, "suffix", suffix} ] -> [ [key,type,suffix] ]
def pack_string_filter_rules(c_config):
    return map(lambda rule: [rule['key'], rule['type'], rule['suffix']], c_config['string_filter_rules']) if 'string_filter_rules' in c_config else []

def pack_num_filter_rules(c_config):
    return map(lambda rule: [rule['key'], rule['type'], rule['suffix']], c_config['num_filter_rules']) if 'num_filter_rules' in c_config else []

def unpack_string_filter_rules(config, c_config):
    c_config['string_filter_rules'] = map(lambda rule: {'key': rule[0], 'type': rule[1], 'suffix': rule[2]}, list(config))

def unpack_num_filter_rules(config, c_config):
    c_config['num_filter_rules'] = map(lambda rule: {'key': rule[0], 'type': rule[1], 'suffix': rule[2]}, list(config))

# "string_types" : { string : { string : string } } ->  { string : { string : string } } 
def pack_string_types(c_config):
    return c_config['string_types'] if 'string_types' in c_config else {}

def unpack_string_types(config, c_config):
    c_config['string_types'] = config

# [{'key': '*', 'type': 'str', 'sample_weight': 'bin', 'global_weight': 'bin'}] -> [ ['*', 'str', 'bin', 'bin'] , ... ]
def pack_string_rules(c_config):
    return map(lambda rule: [rule['key'], rule['type'], rule['sample_weight'], rule['global_weight']], c_config['string_rules']) if 'string_rules' in c_config else []

def unpack_string_rules(config, c_config):
    c_config['string_rules'] = map(lambda rule: {'key': rule[0], 'type': rule[1], 'sample_weight': rule[2], 'global_weight': rule[3]}, list(config))

# "num_types" : { string : { string : string } } ->  { string : { string : string } }         
def pack_num_types(c_config):
    return c_config['num_types'] if 'num_types' in c_config else {}

def unpack_num_types(config, c_config):
    c_config['num_types'] = config

# [{'key': '*', 'type': 'str'] -> [ ['*', 'str'] , ... ]
def pack_num_rules(c_config):
    return map(lambda rule: [rule['key'], rule['type']], c_config['num_rules']) if 'num_rules' in c_config else []

def unpack_num_rules(config, c_config):
    c_config['num_rules'] = map(lambda rule: {'key': rule[0], 'type': rule[1]}, list(config))
