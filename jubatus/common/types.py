def check_type(value, typ):
    if not isinstance(value, typ):
        raise TypeError('type %s is expected, but %s is given' % (typ, type(value)))

def check_types(value, types):
    if isinstance(value, types):
        return
    t = ', '.join([str(t) for t in types])
    raise TypeError('type %s is expected, but %s is given' % (t, type(value)))

class TPrimitive(object):
    def __init__(self, types):
        self.types = types

    def from_msgpack(self, m):
        check_types(m, self.types)
        return m

    def to_msgpack(self, m):
        check_types(m, self.types)
        return m

class TInt(object):
    def __init__(self, signed, byts):
        if signed:
            self.max = (1L << (8 * byts - 1)) - 1
            self.min = - (1L << (8 * byts - 1))
        else:
            self.max = (1L << 8 * byts) - 1
            self.min = 0

    def from_msgpack(self, m):
        check_types(m, (int, long))
        if not (self.min <= m and m <= self.max):
            raise ValueError('int value must be in (%d, %d), but %d is given' % (self.min, self.max, m))
        return m

    def to_msgpack(self, m):
        check_types(m, (int, long))
        if not (self.min <= m and m <= self.max):
            raise ValueError('int value must be in (%d, %d), but %d is given' % (self.min, self.max, m))
        return m

class TFloat(TPrimitive):
    def __init__(self):
        super(TFloat, self).__init__((float,))

class TBool(TPrimitive):
    def __init__(self):
        super(TBool, self).__init__((bool,))

class TString(TPrimitive):
    def __init__(self):
        super(TString, self).__init__((str, unicode))

class TDatum(object):
    def from_msgpack(self, m):
        from datum import Datum
        return Datum.from_msgpack(m)

    def to_msgpack(self, m):
        from datum import Datum
        check_type(m, Datum)
        return m.to_msgpack()

class TRaw(TPrimitive):
    def __init__(self):
        super(TRaw, self).__init__((str,))

class TNullable(object):
    def __init__(self, type):
        self.type = type

    def from_msgpack(self, m):
        if m is None:
            return None
        else:
            return self.type.from_msgpack(m)

    def to_msgpack(self, m):
        if m is None:
            return None
        else:
            return self.type.to_msgpack(m)

class TList(object):
    def __init__(self, type):
        self.type = type

    def from_msgpack(self, m):
        check_types(m, (list, tuple))
        return map(self.type.from_msgpack, m)

    def to_msgpack(self, m):
        check_types(m, (list, tuple))
        return map(self.type.to_msgpack, m)

class TMap(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def from_msgpack(self, m):
        check_type(m, dict)
        dic = {}
        for k, v in m.iteritems():
            dic[self.key.from_msgpack(k)] = self.value.from_msgpack(v)
        return dic

    def to_msgpack(self, m):
        check_type(m, dict)
        dic = {}
        for k, v in m.items():
            dic[self.key.to_msgpack(k)] = self.value.to_msgpack(v)
        return dic

class TTuple(object):
    def __init__(self, *types):
        self.types = types

    def check_tuple(self, m):
        check_types(m, (tuple, list))
        if len(m) != len(self.types):
            raise TypeError("size of tuple is %d, but %d is expected: %s" % (len(m), len(self.types), str(m)))

    def from_msgpack(self, m):
        self.check_tuple(m)
        tpl = []
        for type, x in zip(self.types, m):
            tpl.append(type.from_msgpack(x))
        return tuple(tpl)

    def to_msgpack(self, m):
        self.check_tuple(m)
        tpl = []
        for type, x in zip(self.types, m):
            tpl.append(type.to_msgpack(x))
        return tpl
            

class TUserDef(object):
    def __init__(self, type):
        self.type = type

    def from_msgpack(self, m):
        return self.type.from_msgpack(m)

    def to_msgpack(self, m):
        if isinstance(m, self.type):
            return m.to_msgpack()
        elif isinstance(m, (list, tuple)):
            return self.type.TYPE.to_msgpack(m)
        else:
            raise TypeError('type %s or tuple/list are expected, but %s is given' % (self.type, type(m)))

class TObject(object):
    def from_msgpack(self, m):
        return m

    def to_msgpack(self, m):
        return m

class TEnum(object):
    def __init__(self, values):
        self.values = values

    def from_msgpack(self, m):
        check_types(m, (int, long))
        if m not in self.values:
            raise ValueError
        return m

    def to_msgpack(self, m):
        check_types(m, (int, long))
        if m not in self.values:
            raise ValueError
        return m
