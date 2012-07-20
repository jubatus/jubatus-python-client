
import msgpackrpc
from types import *


class graph:
  def __init__ (self, host, port):
    address = msgpackrpc.Address(host, port)
    self.client = msgpackrpc.Client(address)

  def create_node (self, name):
    retval = self.client.call('create_node', name)
    return retval

  def remove_node (self, name, nid):
    retval = self.client.call('remove_node', name, nid)
    return retval

  def update_node (self, name, nid, p):
    retval = self.client.call('update_node', name, nid, p)
    return retval

  def create_edge (self, name, nid, ei):
    retval = self.client.call('create_edge', name, nid, ei)
    return retval

  def update_edge (self, name, nid, eid, ei):
    retval = self.client.call('update_edge', name, nid, eid, ei)
    return retval

  def remove_edge (self, name, nid, e):
    retval = self.client.call('remove_edge', name, nid, e)
    return retval

  def centrality (self, name, nid, ct, q):
    retval = self.client.call('centrality', name, nid, ct, q)
    return retval

  def add_centrality_query (self, name, q):
    retval = self.client.call('add_centrality_query', name, q)
    return retval

  def add_shortest_path_query (self, name, q):
    retval = self.client.call('add_shortest_path_query', name, q)
    return retval

  def remove_centrality_query (self, name, q):
    retval = self.client.call('remove_centrality_query', name, q)
    return retval

  def remove_shortest_path_query (self, name, q):
    retval = self.client.call('remove_shortest_path_query', name, q)
    return retval

  def shortest_path (self, name, r):
    retval = self.client.call('shortest_path', name, r)
    return [elem_retval for elem_retval in retval]

  def update_index (self, name):
    retval = self.client.call('update_index', name)
    return retval

  def clear (self, name):
    retval = self.client.call('clear', name)
    return retval

  def get_node (self, name, nid):
    retval = self.client.call('get_node', name, nid)
    return node_info.from_msgpack(retval)

  def get_edge (self, name, nid, e):
    retval = self.client.call('get_edge', name, nid, e)
    return edge_info.from_msgpack(retval)

  def save (self, name, arg1):
    retval = self.client.call('save', name, arg1)
    return retval

  def load (self, name, arg1):
    retval = self.client.call('load', name, arg1)
    return retval

  def get_status (self, name):
    retval = self.client.call('get_status', name)
    return {k_retval : {k_v_retval : v_v_retval for k_v_retval,v_v_retval in v_retval.items()} for k_retval,v_retval in retval.items()}

  def create_node_here (self, name, nid):
    retval = self.client.call('create_node_here', name, nid)
    return retval

  def create_global_node (self, name, nid):
    retval = self.client.call('create_global_node', name, nid)
    return retval

  def remove_global_node (self, name, nid):
    retval = self.client.call('remove_global_node', name, nid)
    return retval

  def create_edge_here (self, name, eid, ei):
    retval = self.client.call('create_edge_here', name, eid, ei)
    return retval


