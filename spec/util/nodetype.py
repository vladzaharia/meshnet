from constants.nodetype import TYPE_GATEWAY, TYPE_GATEWAY_TIME, TYPE_NODE, TYPE_NODE_NR, TYPE_PROVISIONING
import unittest

from util.nodetype import NodeType

class NodeTypeTest(unittest.TestCase):
    def test_node(self):
        node_type = NodeType(TYPE_NODE)
        self.assertTrue(node_type.is_node())
        self.assertFalse(node_type.is_gateway())
        self.assertFalse(node_type.is_auth_time_source())
        self.assertFalse(node_type.is_non_routed())

    def test_node_nr(self):
        node_type = NodeType(TYPE_NODE_NR)
        self.assertTrue(node_type.is_node())
        self.assertFalse(node_type.is_gateway())
        self.assertFalse(node_type.is_auth_time_source())
        self.assertTrue(node_type.is_non_routed())

    def test_gateway(self):
        node_type = NodeType(TYPE_GATEWAY)
        self.assertFalse(node_type.is_node())
        self.assertTrue(node_type.is_gateway())
        self.assertFalse(node_type.is_auth_time_source())
        self.assertFalse(node_type.is_non_routed())

    def test_gateway_time(self):
        node_type = NodeType(TYPE_GATEWAY_TIME)
        self.assertFalse(node_type.is_node())
        self.assertTrue(node_type.is_gateway())
        self.assertTrue(node_type.is_auth_time_source())
        self.assertFalse(node_type.is_non_routed())

    def test_provisioning(self):
        node_type = NodeType(TYPE_PROVISIONING)
        self.assertFalse(node_type.is_node())
        self.assertFalse(node_type.is_gateway())
        self.assertFalse(node_type.is_auth_time_source())
        self.assertTrue(node_type.is_non_routed())