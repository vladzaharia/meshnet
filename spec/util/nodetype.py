import unittest

from constants.nodetype import (
    TYPE_GATEWAY,
    TYPE_GATEWAY_TIME,
    TYPE_NODE,
    TYPE_NODE_NR,
    TYPE_PROVISIONING
)
from util.nodetype import NodeType

class NodeTypeTest(unittest.TestCase):
    def test_node(self):
        # Act
        node_type = NodeType(TYPE_NODE)

        # Assert
        self.assertTrue(node_type.is_node())
        self.assertFalse(node_type.is_gateway())
        self.assertFalse(node_type.is_auth_time_source())
        self.assertFalse(node_type.is_non_routed())

    def test_node_nr(self):
        # Act
        node_type = NodeType(TYPE_NODE_NR)

        # Assert
        self.assertTrue(node_type.is_node())
        self.assertFalse(node_type.is_gateway())
        self.assertFalse(node_type.is_auth_time_source())
        self.assertTrue(node_type.is_non_routed())

    def test_gateway(self):
        # Act
        node_type = NodeType(TYPE_GATEWAY)

        # Assert
        self.assertFalse(node_type.is_node())
        self.assertTrue(node_type.is_gateway())
        self.assertFalse(node_type.is_auth_time_source())
        self.assertFalse(node_type.is_non_routed())

    def test_gateway_time(self):
        # Act
        node_type = NodeType(TYPE_GATEWAY_TIME)

        # Assert
        self.assertFalse(node_type.is_node())
        self.assertTrue(node_type.is_gateway())
        self.assertTrue(node_type.is_auth_time_source())
        self.assertFalse(node_type.is_non_routed())

    def test_provisioning(self):
        # Act
        node_type = NodeType(TYPE_PROVISIONING)

        # Asser
        self.assertFalse(node_type.is_node())
        self.assertFalse(node_type.is_gateway())
        self.assertFalse(node_type.is_auth_time_source())
        self.assertTrue(node_type.is_non_routed())