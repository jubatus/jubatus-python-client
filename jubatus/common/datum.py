from message_string_generator import MessageStringGenerator
from types import *

class Datum:
    TYPE = TTuple(TList(TTuple(TString(), TString())),
                  TList(TTuple(TString(), TFloat())),
                  TList(TTuple(TString(), TRaw())))

    def __init__(self, values = {}):
        self.string_values = []
        self.num_values = []
        self.binary_values = []

        for (k, v) in values.iteritems():
            if not isinstance(k, (str, unicode)):
                raise TypeError

            if isinstance(v, (str, unicode)):
                self.string_values.append([k, v])
            elif isinstance(v, float):
                self.num_values.append([k, v])
            elif isinstance(v, int):
                self.num_values.append([k, float(v)])
            else:
                raise TypeError

    def add_string(self, key, value):
        if not isinstance(key, (str, unicode)):
            raise TypeError
        if isinstance(value, (str, unicode)):
            self.string_values.append([key, value])
        else:
            raise TypeError

    def add_number(self, key, value):
        if not isinstance(key, (str, unicode)):
            raise TypeError
        if isinstance(value, float):
            self.num_values.append([key, value])
        elif isinstance(value, int):
            self.num_values.append([key, float(value)])
        else:
            raise TypeError

    def add_binary(self, key, value):
        if not isinstance(key, (str, unicode)):
            raise TypeError
        if isinstance(value, str):
            self.binary_values.append([key, value])
        else:
            raise TypeError

    def to_msgpack(self):
        return (
            self.string_values,
            self.num_values,
            self.binary_values,
            )

    @staticmethod
    def from_msgpack(arg):
        val = Datum.TYPE.from_msgpack(arg)
        d = Datum()
        d.string_values = val[0]
        d.num_values = val[1]
        d.binary_values = val[2]
        return d

    def __str__(self):
        gen = MessageStringGenerator()
        gen.open("datum")
        gen.add("string_values", self.string_values)
        gen.add("num_values", self.num_values)
        gen.add("binary_values", self.binary_values)
        gen.close()
        return gen.to_string()
