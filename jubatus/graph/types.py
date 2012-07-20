
# This file is auto-generated from ../src/server/graph.idl
# *** DO NOT EDIT ***


import sys
import msgpack


class property:
  @staticmethod
  def from_msgpack(arg):
    return {k_arg : v_arg for k_arg,v_arg in arg.items()}

class node_info:
  def __init__(self, p, in_edges, out_edges):
    self.p = p
    self.in_edges = in_edges
    self.out_edges = out_edges

  def to_msgpack(self):
    return (
      self.p,
      self.in_edges,
      self.out_edges,
      )

  @staticmethod
  def from_msgpack(arg):
    return node_info(
      property.from_msgpack(arg[0]),
      [elem_arg_1_ for elem_arg_1_ in arg[1]],
      [elem_arg_2_ for elem_arg_2_ in arg[2]])

class preset_query:
  def __init__(self, edge_query, node_query):
    self.edge_query = edge_query
    self.node_query = node_query

  def to_msgpack(self):
    return (
      self.edge_query,
      self.node_query,
      )

  @staticmethod
  def from_msgpack(arg):
    return preset_query(
      [ (elem_arg_0_[0], elem_arg_0_[1], )  for elem_arg_0_ in arg[0]],
      [ (elem_arg_1_[0], elem_arg_1_[1], )  for elem_arg_1_ in arg[1]])

class edge_info:
  def __init__(self, p, src, tgt):
    self.p = p
    self.src = src
    self.tgt = tgt

  def to_msgpack(self):
    return (
      self.p,
      self.src,
      self.tgt,
      )

  @staticmethod
  def from_msgpack(arg):
    return edge_info(
      property.from_msgpack(arg[0]),
      arg[1],
      arg[2])

class shortest_path_req:
  def __init__(self, src, tgt, max_hop, q):
    self.src = src
    self.tgt = tgt
    self.max_hop = max_hop
    self.q = q

  def to_msgpack(self):
    return (
      self.src,
      self.tgt,
      self.max_hop,
      self.q,
      )

  @staticmethod
  def from_msgpack(arg):
    return shortest_path_req(
      arg[0],
      arg[1],
      arg[2],
      preset_query.from_msgpack(arg[3]))


