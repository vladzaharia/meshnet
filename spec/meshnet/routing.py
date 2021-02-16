from datetime import datetime, timedelta
import unittest

from constants.nodetype import TYPE_GATEWAY, TYPE_GATEWAY_TIME, TYPE_NODE
from meshnet.routing import Routing, RoutingEntry
from meshnet.self import Self
from util.nodetype import NodeType

class RoutingTest(unittest.TestCase):
    routing = Routing()

    def setUp(self):
        Self().reset()
        Routing().reset()
        self.routing = Routing()

    # E2E
    def test_default(self):
        self.assertEqual(len(self.routing.neighbors), 0)

    def test_add_node(self):
        # Act
        self.routing.add(RoutingEntry(b'\x87\x18\x91', NodeType(TYPE_NODE)))
        self.routing.add(RoutingEntry(b'\xAE\x32\x92', NodeType(TYPE_NODE)))

        # Assert
        self.assertEqual(len(self.routing.neighbors), 2)
        self.assertEqual(self.routing.neighbors[0].node_id, b'\x87\x18\x91')
        self.assertEqual(self.routing.neighbors[0].node_type.node_type, TYPE_NODE)
        self.assertEqual(self.routing.neighbors[1].node_id, b'\xAE\x32\x92')
        self.assertEqual(self.routing.neighbors[1].node_type.node_type, TYPE_NODE)

    def test_singleton(self):
        # Setup
        self.routing.add(RoutingEntry(b'\x87\x18\x91', NodeType(TYPE_NODE)))
        self.routing.add(RoutingEntry(b'\xAE\x32\x92', NodeType(TYPE_NODE)))

        # Act
        new_routing = Routing()

        # Assert
        self.assertEqual(len(new_routing.neighbors), 2)
        self.assertEqual(new_routing.neighbors[0].node_id, b'\x87\x18\x91')
        self.assertEqual(new_routing.neighbors[0].node_type.node_type, TYPE_NODE)
        self.assertEqual(new_routing.neighbors[1].node_id, b'\xAE\x32\x92')
        self.assertEqual(new_routing.neighbors[1].node_type.node_type, TYPE_NODE)

    def test_add_gateway(self):
        # Act
        self.routing.add(RoutingEntry(b'\x17\xF7\x99', NodeType(TYPE_GATEWAY)))
        self.routing.add(RoutingEntry(b'\xAA\x21\x87', NodeType(TYPE_GATEWAY)))

        # Assert
        self.assertEqual(len(self.routing.neighbors), 2)
        self.assertEqual(self.routing.neighbors[0].node_id, b'\x17\xF7\x99')
        self.assertEqual(self.routing.neighbors[0].node_type.node_type, TYPE_GATEWAY)
        self.assertEqual(self.routing.neighbors[1].node_id, b'\xAA\x21\x87')
        self.assertEqual(self.routing.neighbors[1].node_type.node_type, TYPE_GATEWAY)

    def test_add_gateway_time(self):
        # Act
        self.routing.add(RoutingEntry(b'\x19\xFA\xE9', NodeType(TYPE_GATEWAY_TIME)))

        # Assert
        self.assertEqual(len(self.routing.neighbors), 1)
        self.assertEqual(self.routing.neighbors[0].node_id, b'\x19\xFA\xE9')
        self.assertEqual(self.routing.neighbors[0].node_type.node_type, TYPE_GATEWAY_TIME)

    # Functions
    def test_node_neighbors(self):
        # Act
        self.routing.add(RoutingEntry(b'\x87\x2A\x8F', NodeType(TYPE_NODE)))
        self.routing.add(RoutingEntry(b'\xA8\xCC\xD4', NodeType(TYPE_NODE)))
        self.routing.add(RoutingEntry(b'\x17\xF7\x99', NodeType(TYPE_GATEWAY)))
        self.routing.add(RoutingEntry(b'\xAA\x21\x87', NodeType(TYPE_GATEWAY_TIME)))

        # Assert
        node_neighbors = self.routing.node_neighbors()
        self.assertEqual(len(node_neighbors), 2)
        self.assertEqual(node_neighbors[0].node_id, b'\x87\x2A\x8F')
        self.assertEqual(node_neighbors[0].node_type.node_type, TYPE_NODE)
        self.assertEqual(node_neighbors[1].node_id, b'\xA8\xCC\xD4')
        self.assertEqual(node_neighbors[1].node_type.node_type, TYPE_NODE)


    def test_gateway_neighbors(self):
        # Act
        self.routing.add(RoutingEntry(b'\x87\x2A\x8F', NodeType(TYPE_NODE)))
        self.routing.add(RoutingEntry(b'\xA8\xCC\xD4', NodeType(TYPE_NODE)))
        self.routing.add(RoutingEntry(b'\x17\xF7\x99', NodeType(TYPE_GATEWAY)))
        self.routing.add(RoutingEntry(b'\xAA\x21\x87', NodeType(TYPE_GATEWAY_TIME)))

        # Assert
        gateway_neighbors = self.routing.gateway_neighbors()
        self.assertEqual(len(gateway_neighbors), 2)
        self.assertEqual(gateway_neighbors[0].node_id, b'\x17\xF7\x99')
        self.assertEqual(gateway_neighbors[0].node_type.node_type, TYPE_GATEWAY)
        self.assertEqual(gateway_neighbors[1].node_id, b'\xAA\x21\x87')
        self.assertEqual(gateway_neighbors[1].node_type.node_type, TYPE_GATEWAY_TIME)

    def test_clean(self):
        # Setup
        self.routing.add(RoutingEntry(b'\x87\x2A\x8F', NodeType(TYPE_NODE)))
        self.routing.add(RoutingEntry(b'\xA8\xCC\xD4', NodeType(TYPE_NODE)))
        self.routing.add(RoutingEntry(b'\x17\xF7\x99', NodeType(TYPE_GATEWAY)))
        self.routing.add(RoutingEntry(b'\xAA\x21\x87', NodeType(TYPE_GATEWAY_TIME)))
        self.routing.neighbors[0].expiry = datetime.now() - timedelta(minutes = 1)
        self.routing.neighbors[2].expiry = datetime.now() - timedelta(minutes = 1)
        self.assertEqual(len(self.routing.neighbors), 4)

        # Act
        self.routing.clean()

        # Assert
        self.assertEqual(len(self.routing.neighbors), 2)
        self.assertEqual(self.routing.neighbors[0].node_id, b'\xA8\xCC\xD4')
        self.assertEqual(self.routing.neighbors[0].node_type.node_type, TYPE_NODE)
        self.assertEqual(self.routing.neighbors[1].node_id, b'\xAA\x21\x87')
        self.assertEqual(self.routing.neighbors[1].node_type.node_type, TYPE_GATEWAY_TIME)

    def test_reset(self):
        # Setup
        self.routing.add(RoutingEntry(b'\x87\x2A\x8F', NodeType(TYPE_NODE)))
        self.routing.add(RoutingEntry(b'\xA8\xCC\xD4', NodeType(TYPE_NODE)))
        self.routing.add(RoutingEntry(b'\x17\xF7\x99', NodeType(TYPE_GATEWAY)))
        self.routing.add(RoutingEntry(b'\xAA\x21\x87', NodeType(TYPE_GATEWAY_TIME)))
        self.assertEqual(len(self.routing.neighbors), 4)

        # Act
        self.routing.reset()
        self.assertEqual(len(self.routing.neighbors), 0)
