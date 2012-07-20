
import msgpackrpc
from types import *


class classifier:
  def __init__ (self, host, port):
    address = msgpackrpc.Address(host, port)
    self.client = msgpackrpc.Client(address)

  def set_config (self, name, c):
    retval = self.client.call('set_config', name, c)
    return retval

  def get_config (self, name):
    retval = self.client.call('get_config', name)
    return config_data.from_msgpack(retval)

  def train (self, name, data):
    retval = self.client.call('train', name, data)
    return retval

  def classify (self, name, data):
    retval = self.client.call('classify', name, data)
    return [[estimate_result.from_msgpack(elem_elem_retval) for elem_elem_retval in elem_retval] for elem_retval in retval]

  def save (self, name, id):
    retval = self.client.call('save', name, id)
    return retval

  def load (self, name, id):
    retval = self.client.call('load', name, id)
    return retval

  def get_status (self, name):
    retval = self.client.call('get_status', name)
    return {k_retval : {k_v_retval : v_v_retval for k_v_retval,v_v_retval in v_retval.items()} for k_retval,v_retval in retval.items()}


