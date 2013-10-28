from jubatus.common import *
import unittest

class TypeCheckTest(unittest.TestCase):
    def assertTypeOf(self, type, value):
        self.assertEquals(value, type.from_msgpack(value))
        self.assertEquals(value, type.to_msgpack(value))

    def assertTypeError(self, type, value):
        self.assertRaises(TypeError, lambda: type.from_msgpack(value))
        self.assertRaises(TypeError, lambda: type.to_msgpack(value))

    def assertValueError(self, type, value):
        self.assertRaises(ValueError, lambda: type.from_msgpack(value))
        self.assertRaises(ValueError, lambda: type.to_msgpack(value))

    def testInt(self):
        self.assertTypeOf(TInt(True, 1), 1)
        self.assertTypeError(TInt(True, 1), None)
        self.assertTypeError(TInt(True, 1), "")
        self.assertValueError(TInt(True, 1), 128)
        self.assertValueError(TInt(True, 1), -129)
        self.assertValueError(TInt(False, 1), 256)
        self.assertValueError(TInt(False, 1), -1)

    def testFloat(self):
        self.assertTypeOf(TFloat(), 1.3)
        self.assertTypeError(TFloat(), None)
        self.assertTypeError(TFloat(), 1)

    def testBool(self):
        self.assertTypeOf(TBool(), True)
        self.assertTypeError(TBool(), None)
        self.assertTypeError(TBool(), 1)

    def testString(self):
        self.assertTypeOf(TString(), "test")
        self.assertTypeOf(TString(), u"test")
        self.assertTypeError(TString(), 1)

    def testRaw(self):
        self.assertTypeOf(TRaw(), "test")
        self.assertTypeError(TRaw(), u"test")
        self.assertTypeError(TRaw(), 1)

    def testNullable(self):
        self.assertTypeOf(TNullable(TBool()), None)
        self.assertTypeOf(TNullable(TBool()), True)
        self.assertTypeError(TNullable(TBool()), 1)

    def testList(self):
        self.assertTypeOf(TList(TInt(True, 8)), [1, 2, 3])
        self.assertTypeOf(TList(TList(TInt(True, 8))), [[1, 2], [], [2, 3]])
        self.assertTypeError(TList(TInt(True, 8)), None)

    def testMap(self):
        self.assertTypeOf(TMap(TString(), TBool()), {"true": True})
        self.assertTypeError(TMap(TString(), TBool()), None)
        self.assertTypeError(TMap(TString(), TBool()), {1: True})
        self.assertTypeError(TMap(TString(), TBool()), {"true": 1})

    def testTuple(self):
        typ = TTuple(TInt(True, 8), TTuple(TString(), TInt(True, 8)))
        self.assertEquals(
            [1, ["test", 1]],
            typ.to_msgpack((1, ("test", 1))))
        self.assertEquals(
            (1, ("test", 1)),
            typ.from_msgpack((1, ("test", 1))))
        self.assertTypeError(TTuple(TInt(True, 8)), ("test", ))
        self.assertTypeError(TTuple(TInt(True, 8)), (1, 2))

    def testUserDef(self):
        class MyType:
            TYPE = TTuple(TString(), TFloat())

            def __init__(self, v1, v2):
                self.v1 = v1
                self.v2 = v2

            def to_msgpack(self):
                t = (self.v1, self.v2)
                return self.__class__.TYPE.to_msgpack(t)

            @classmethod
            def from_msgpack(cls, arg):
                val = cls.TYPE.from_msgpack(arg)
                return MyType(*val)

        typ = TUserDef(MyType)
        obj = typ.from_msgpack(("hoge", 1.0))
        self.assertTrue(isinstance(obj, MyType))
        self.assertEquals(["hoge", 1.0], typ.to_msgpack(obj))

        self.assertTypeError(typ, 1)
        self.assertTypeError(typ, [])
        self.assertTypeError(typ, None)

if __name__ == '__main__':
    unittest.main()
