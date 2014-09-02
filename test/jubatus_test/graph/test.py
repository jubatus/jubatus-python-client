#!/usr/bin/env python

import unittest
import json
import msgpackrpc

from jubatus.graph.client import Graph
from jubatus.graph.types    import *
from jubatus.common import Datum

from jubatus_test.test_util import TestUtil

host = "127.0.0.1"
port = 21005
timeout = 10

class GraphTest(unittest.TestCase):
    def setUp(self):
        self.config = {
            "method": "graph_wo_index",
            "parameter": {
                "damping_factor": 0.9,
                "landmark_num": 5
                }
            }

        TestUtil.write_file('config_graph.json', json.dumps(self.config))
        self.srv = TestUtil.fork_process('graph', port, 'config_graph.json')
        try:
            self.cli = Graph(host, port, "name")
        except:
            TestUtil.kill_process(self.srv)
            raise

    def tearDown(self):
        if self.cli:
            self.cli.get_client().close()
        TestUtil.kill_process(self.srv)

    def test_node_info(self):
        edge_query = [["a", "b"], ["c", "d"], ["e", "f"]]
        node_query = [["0", "1"], ["2", "3"]]
        p = PresetQuery(edge_query, node_query)
        in_edges = [0, 0]
        out_edges = [0, 0]
        Node(p, in_edges, out_edges)

    def test_get_client(self):
        self.assertTrue(isinstance(self.cli.get_client(), msgpackrpc.client.Client))

    def test_create_node(self):
        nid = self.cli.create_node()
        self.assertEqual(str(int(nid)), nid)

    def test_remove_node(self):
        nid = self.cli.create_node()
        self.assertEqual(self.cli.remove_node(nid), True)

    def test_update_node(self):
        nid = self.cli.create_node()
        prop = {"key1":"val1", "key2":"val2"}
        self.assertEqual(self.cli.update_node(nid, prop), True)

    def test_create_edge(self):
        src = self.cli.create_node()
        tgt = self.cli.create_node()
        prop = {"key1":"val1", "key2":"val2"}
        ei = Edge(prop, src, tgt)
        eid = self.cli.create_edge(tgt, ei)

    def test_str(self):
        self.assertEqual("node{property: {}, in_edges: [], out_edges: []}",
                         str(Node({}, [], [])))
        self.assertEqual("preset_query{edge_query: [], node_query: []}",
                         str(PresetQuery([], [])))
        self.assertEqual("edge{property: {}, source: src, target: tgt}",
                         str(Edge({}, 'src', 'tgt')))
        self.assertEqual("shortest_path_query{source: src, target: tgt, max_hop: 10, query: preset_query{edge_query: [], node_query: []}}",
                         str(ShortestPathQuery('src', 'tgt', 10, PresetQuery([], []))))

if __name__ == '__main__':
    test_suite = unittest.TestLoader().loadTestsFromTestCase(GraphTest)
    unittest.TextTestRunner().run(test_suite)

