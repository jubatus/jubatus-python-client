from jubatus.common import *
import unittest

def convert(type, value):
    return type.from_msgpack(value)

class TypeCheckTest(unittest.TestCase):
    def assertTypeOf(self, type, value):
        self.assertEquals(value, convert(type, value))

    def assertTypeError(self, type, value):
        self.assertRaises(TypeError, lambda: convert(type, value))

    def assertValueError(self, type, value):
        self.assertRaises(ValueError, lambda: convert(type, value))

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
        self.assertTypeOf(TTuple(TInt(True, 8), TTuple(TString(), TInt(True, 8))), (1, ("test", 1)))
        self.assertTypeError(TTuple(TInt(True, 8)), ("test", ))
        self.assertTypeError(TTuple(TInt(True, 8)), (1, 2))


if __name__ == '__main__':
    unittest.main()
