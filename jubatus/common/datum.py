class Datum:
  def __init__(self, values = {}):
    self.string_values = []
    self.num_values = []
    self.binary_values = []

    for (k, v) in values.iteritems():
      if not (isinstance(k, str) or isinstance(k, unicode)):
        raise TypeError

      if isinstance(v, str) or isinstance(v, unicode):
        self.string_values.append([k, v])
      elif isinstance(v, float):
        self.num_values.append([k, v])
      elif isinstance(v, int):
        self.num_values.append([k, float(v)])
      else:
        raise TypeError

  def add_string(self, key, value):
    if not (isinstance(key, str) or isinstance(key, unicode)):
      raise TypeError
    if isinstance(value, str) or isinstance(value, unicode):
      self.string_values.append([key, value])
    else:
      raise TypeError

  def add_number(self, key, value):
    if not (isinstance(key, str) or isinstance(key, unicode)):
      raise TypeError
    if isinstance(value, float):
      self.num_values.append([key, value])
    elif isinstance(value, int):
      self.num_values.append([key, float(value)])
    else:
      raise TypeError

  def add_binary(self, key, value):
    if not (isinstance(key, str) or isinstance(key, unicode)):
      raise TypeError
    if isinstance(value, str):
      self.binary_values.append([key, value])
    else:
      raise TypeError

  def to_msgpack (self):
    return (
      self.string_values,
      self.num_values,
      self.binary_values,
      )

  @staticmethod
  def from_msgpack (arg):
    d = Datum()
    d.string_values = list(arg[0])
    d.num_values = list(arg[1])
    d.binary_values = list(arg[2])
    return d

  def __str__(self):
    gen = jubatus.common.MessageStringGenerator()
    gen.open("datum")
    gen.add("string_values", self.string_values)
    gen.add("num_values", self.num_values)
    gen.add("binary_values", self.binary_values)
    gen.close()
    return gen.to_string()
