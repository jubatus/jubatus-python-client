class Datum:
  def __init__(self, values = {}):
    self.string_values = []
    self.num_values = []

    for (k, v) in values.iteritems():
      if not (isinstance(k, str) or isinstance(k, unicode)):
        raise TypeError

      if isinstance(v, str) or isinstance(v, unicode):
        self.string_values.append((k, v))
      elif isinstance(v, float):
        self.num_values.append((k, v))
      elif isinstance(v, int):
        self.num_values.append((k, float(v)))
      else:
        raise TypeError

  def to_msgpack (self):
    return (
      self.string_values,
      self.num_values,
      )

  @staticmethod
  def from_msgpack (arg):
    d = Datum()
    d.string_values = list(arg[0])
    d.num_values = list(arg[1])
    return d

  def __str__(self):
    gen = jubatus.common.MessageStringGenerator()
    gen.open("datum")
    gen.add("string_values", self.string_values)
    gen.add("num_values", self.num_values)
    gen.close()
    return gen.to_string()
