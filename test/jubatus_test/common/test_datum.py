from jubatus.common import Datum
import unittest
import msgpack
from jubatus.common.compat import b, u

class DatumTest(unittest.TestCase):
    def test_pack(self):
        self.assertEqual(
            msgpack.packb(([['name', 'Taro']], [['age', 20.0]], [])),
            msgpack.packb(Datum({'name': 'Taro', 'age': 20}).to_msgpack()))

    def test_unpack(self):
        d = Datum.from_msgpack(([['name', 'Taro']], [['age', 20.0]], [['img', b('0101')]]))
        self.assertEqual(
            [('name', 'Taro')],
            d.string_values)
        self.assertEqual(
            [('age', 20.0)],
            d.num_values)
        self.assertEqual(
            [('img', b('0101'))],
            d.binary_values)

    def test_empty(self):
        self.assertEqual(
            msgpack.packb(([], [], [])),
            msgpack.packb(Datum().to_msgpack()))

    def test_invalid_key(self):
        self.assertRaises(TypeError, Datum, {1: ''})

    def test_invalid_value(self):
        self.assertRaises(TypeError, Datum, {'': None})
        self.assertRaises(TypeError, Datum, {'': []})

    def test_add_string(self):
        d = Datum()
        d.add_string('key', 'value')
        self.assertEqual(Datum({'key': 'value'}).to_msgpack(),
                         d.to_msgpack())

        d = Datum()
        d.add_string(u('key'), u('value'))
        self.assertEqual(Datum({'key': 'value'}).to_msgpack(),
                         d.to_msgpack())

    def test_invalid_add_string(self):
        d = Datum()
        self.assertRaises(TypeError, Datum.add_string, d, 1, 'value')
        self.assertRaises(TypeError, Datum.add_string, d, 'key', 1)

    def test_add_number(self):
        d = Datum()
        d.add_number('key', 1.0)
        self.assertEqual(Datum({'key': 1.0}).to_msgpack(),
                         d.to_msgpack())

    def test_add_int(self):
        d = Datum()
        d.add_number('key', 1)
        self.assertEqual(Datum({'key': 1.0}).to_msgpack(),
                         d.to_msgpack())

    def test_invalid_add_number(self):
        d = Datum()
        self.assertRaises(TypeError, Datum.add_number, d, 1, 1.0)
        self.assertRaises(TypeError, Datum.add_number, d, 'key', '')

    def test_add_binary(self):
        d = Datum()
        d.add_binary('key', b('value'))
        self.assertEqual(
            ([], [], [['key', b('value')]]),
            d.to_msgpack())

    def test_invalid_add_binary(self):
        d = Datum()
        self.assertRaises(TypeError, Datum.add_binary, d, 1, 1.0)
        self.assertRaises(TypeError, Datum.add_binary, d, 'key', 1)

    def test_str(self):
        d = Datum()
        d.add_string('name', 'john')
        d.add_number('age', 20)
        d.add_binary('image', b('0101'))
        s = str(d)
        self.assertTrue('datum{string_values: [[\'name\', \'john\']], num_values: [[\'age\', 20.0]], binary_values: [[\'image\', \'0101\']]}' == s or 'datum{string_values: [[\'name\', \'john\']], num_values: [[\'age\', 20.0]], binary_values: [[\'image\', b\'0101\']]}' == s)

if __name__ == '__main__':
    unittest.main()
