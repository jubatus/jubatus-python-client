
# This file is auto-generated from ../src/server/stat.idl
# *** DO NOT EDIT ***


import sys
import msgpack


class config_data:
  def __init__(self, window_size):
    self.window_size = window_size

  def to_msgpack(self):
    return (
      self.window_size,
      )

  @staticmethod
  def from_msgpack(arg):
    return config_data(
      arg[0])


