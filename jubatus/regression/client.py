
import msgpackrpc
from types import *


class regression:
  def __init__ (self, host, port):
    address = msgpackrpc.Address(host, port)
    self.client = msgpackrpc.Client(address)

  def set_config (self, name, c):
    retval = self.client.call('set_config', name, c)
    return retval

  def get_config (self, name):
    retval = self.client.call('get_config', name)
    return config_data.from_msgpack(retval)

  def train (self, name, train_data):
    retval = self.client.call('train', name, train_data)
    return retval

  def estimate (self, name, estimate_data):
    retval = self.client.call('estimate', name, estimate_data)
    return [elem_retval for elem_retval in retval]

  def save (self, name, arg1):
    retval = self.client.call('save', name, arg1)
    return retval

  def load (self, name, arg1):
    retval = self.client.call('load', name, arg1)
    return retval

  def get_status (self, name):
    retval = self.client.call('get_status', name)
    return {k_retval : {k_v_retval : v_v_retval for k_v_retval,v_v_retval in v_retval.items()} for k_retval,v_retval in retval.items()}


