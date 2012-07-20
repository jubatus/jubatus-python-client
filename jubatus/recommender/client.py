
import msgpackrpc
from types import *


class recommender:
  def __init__ (self, host, port):
    address = msgpackrpc.Address(host, port)
    self.client = msgpackrpc.Client(address)

  def set_config (self, name, c):
    retval = self.client.call('set_config', name, c)
    return retval

  def get_config (self, name):
    retval = self.client.call('get_config', name)
    return config_data.from_msgpack(retval)

  def clear_row (self, name, id):
    retval = self.client.call('clear_row', name, id)
    return retval

  def update_row (self, name, id, d):
    retval = self.client.call('update_row', name, id, d)
    return retval

  def clear (self, name):
    retval = self.client.call('clear', name)
    return retval

  def complete_row_from_id (self, name, id):
    retval = self.client.call('complete_row_from_id', name, id)
    return datum.from_msgpack(retval)

  def complete_row_from_data (self, name, d):
    retval = self.client.call('complete_row_from_data', name, d)
    return datum.from_msgpack(retval)

  def similar_row_from_id (self, name, id, size):
    retval = self.client.call('similar_row_from_id', name, id, size)
    return similar_result.from_msgpack(retval)

  def similar_row_from_data (self, name, data, size):
    retval = self.client.call('similar_row_from_data', name, data, size)
    return similar_result.from_msgpack(retval)

  def decode_row (self, name, id):
    retval = self.client.call('decode_row', name, id)
    return datum.from_msgpack(retval)

  def get_all_rows (self, name):
    retval = self.client.call('get_all_rows', name)
    return [elem_retval for elem_retval in retval]

  def similarity (self, name, lhs, rhs):
    retval = self.client.call('similarity', name, lhs, rhs)
    return retval

  def l2norm (self, name, d):
    retval = self.client.call('l2norm', name, d)
    return retval

  def save (self, name, id):
    retval = self.client.call('save', name, id)
    return retval

  def load (self, name, id):
    retval = self.client.call('load', name, id)
    return retval

  def get_status (self, name):
    retval = self.client.call('get_status', name)
    return {k_retval : {k_v_retval : v_v_retval for k_v_retval,v_v_retval in v_retval.items()} for k_retval,v_retval in retval.items()}


