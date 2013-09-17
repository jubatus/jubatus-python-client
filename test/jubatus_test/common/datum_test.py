from jubatus.common import Datum
import unittest
import msgpack

class DatumTest(unittest.TestCase):
    def test_pack(self):
        self.assertEquals(
            msgpack.packb(([['name', 'Taro']], [['age', 20.0]])),
            msgpack.packb(Datum({'name': 'Taro', 'age': 20}).to_msgpack()))

    def test_unpack(self):
        d = Datum.from_msgpack(([['name', 'Taro']], [['age', 20.0]]))
        self.assertEquals(
            [['name', 'Taro']],
            d.string_values)
        self.assertEquals(
            [['age', 20.0]],
            d.num_values)

    def test_empty(self):
        self.assertEquals(
            msgpack.packb(([], [])),
            msgpack.packb(Datum().to_msgpack()))

    def test_invalid_key(self):
        self.assertRaises(TypeError, Datum, {1: ''})

    def test_invalid_value(self):
        self.assertRaises(TypeError, Datum, {'': None})
        self.assertRaises(TypeError, Datum, {'': []})


if __name__ == '__main__':
    unittest.main()
