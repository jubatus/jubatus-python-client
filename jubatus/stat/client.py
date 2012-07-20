
import msgpackrpc
from types import *


class stat:
  def __init__ (self, host, port):
    address = msgpackrpc.Address(host, port)
    self.client = msgpackrpc.Client(address)

  def set_config (self, name, c):
    retval = self.client.call('set_config', name, c)
    return retval

  def get_config (self, name):
    retval = self.client.call('get_config', name)
    return config_data.from_msgpack(retval)

  def push (self, name, key, val):
    retval = self.client.call('push', name, key, val)
    return retval

  def sum (self, name, key):
    retval = self.client.call('sum', name, key)
    return retval

  def stddev (self, name, key):
    retval = self.client.call('stddev', name, key)
    return retval

  def max (self, name, key):
    retval = self.client.call('max', name, key)
    return retval

  def min (self, name, key):
    retval = self.client.call('min', name, key)
    return retval

  def entropy (self, name, key):
    retval = self.client.call('entropy', name, key)
    return retval

  def moment (self, name, key, n, c):
    retval = self.client.call('moment', name, key, n, c)
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


