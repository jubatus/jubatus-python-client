#!/usr/bin/env python

from jubatus.common import MessageStringGenerator
import unittest

class MessageStringGeneratorTest(unittest.TestCase):
    def testEmpty(self):
        gen = MessageStringGenerator()
        gen.open("test")
        gen.close()
        self.assertEquals("test{}", gen.to_string())

    def testOne(self):
        gen = MessageStringGenerator()
        gen.open("test")
        gen.add("k1", "v1")
        gen.close()
        self.assertEquals("test{k1: v1}", gen.to_string())

    def testTwo(self):
        gen = MessageStringGenerator()
        gen.open("test")
        gen.add("k1", "v1")
        gen.add("k2", "v2")
        gen.close()
        self.assertEquals("test{k1: v1, k2: v2}", gen.to_string())

    def testNumber(self):
        gen = MessageStringGenerator()
        gen.open("test")
        gen.add("k1", 1)
        gen.close()
        self.assertEquals("test{k1: 1}", gen.to_string())

if __name__ == '__main__':
    unittest.main()
