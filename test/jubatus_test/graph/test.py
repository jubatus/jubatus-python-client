#!/usr/bin/env python

import unittest
from jubatus.graph.client import graph
from jubatus.graph.types  import *

from jubatus_test.common import CommonUtils

host = "localhost"
port = 21005
timeout = 10

class GraphTest(unittest.TestCase):
  def setUp(self):
    self.srv = CommonUtils.start_server("jubagraph", port)
    self.cli = graph(host, port)

  def tearDown(self):
    CommonUtils.stop_server(self.srv)

  def test_node_info(self):
    edge_query = [["a", "b"], ["c", "d"], ["e", "f"]]
    node_query = [["0", "1"], ["2", "3"]]
    p = preset_query(edge_query, node_query)
    in_edges = [0, 0]
    out_edges = [0, 0]
    node_info(p, in_edges, out_edges)

  def test_create_node(self):
    nid = self.cli.create_node("name")
    self.assertEqual(nid, "3")

  def test_remove_node(self):
    nid = self.cli.create_node("name")
    self.assertEqual(self.cli.remove_node("name", nid), 0)

  def test_update_node(self):
    nid = self.cli.create_node("name")
    prop = {"key1":"val1", "key2":"val2"}
    self.assertEqual(self.cli.update_node("name", nid, prop), 0)

  def test_create_edge(self):
    src = self.cli.create_node("name")
    tgt = self.cli.create_node("name")
    prop = {"key1":"val1", "key2":"val2"}
    ei = edge_info(prop, src, tgt)
    eid = self.cli.create_edge("name", tgt, ei)

if __name__ == '__main__':
  test_suite = unittest.TestLoader().loadTestsFromTestCase(GraphTest)
  unittest.TextTestRunner().run(test_suite)

