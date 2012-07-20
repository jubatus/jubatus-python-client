
# This file is auto-generated from ../src/server/classifier.idl
# *** DO NOT EDIT ***


import sys
import msgpack


class param_t:
  @staticmethod
  def from_msgpack(arg):
    return {k_arg : v_arg for k_arg,v_arg in arg.items()}

class config_data:
  def __init__(self, method, config):
    self.method = method
    self.config = config

  def to_msgpack(self):
    return (
      self.method,
      self.config,
      )

  @staticmethod
  def from_msgpack(arg):
    return config_data(
      arg[0],
      arg[1])

class datum:
  def __init__(self, string_values, num_values):
    self.string_values = string_values
    self.num_values = num_values

  def to_msgpack(self):
    return (
      self.string_values,
      self.num_values,
      )

  @staticmethod
  def from_msgpack(arg):
    return datum(
      [ (elem_arg_0_[0], elem_arg_0_[1], )  for elem_arg_0_ in arg[0]],
      [ (elem_arg_1_[0], elem_arg_1_[1], )  for elem_arg_1_ in arg[1]])

class estimate_result:
  def __init__(self, label, prob):
    self.label = label
    self.prob = prob

  def to_msgpack(self):
    return (
      self.label,
      self.prob,
      )

  @staticmethod
  def from_msgpack(arg):
    return estimate_result(
      arg[0],
      arg[1])


