import unittest

from constants.headers import ROUTING_PROVISIONING
from constants.nodetype import TYPE_NODE, TYPE_PROVISIONING
from meshnet.self import Self
from util.nodetype import NodeType

class SelfTest(unittest.TestCase):
    self_obj = Self()

    def setUp(self):
        Self().reset()

    def test_default(self):
        # Assert
        self.assertEqual(Self().node_id, ROUTING_PROVISIONING)
        self.assertEqual(Self().node_type.node_type, TYPE_PROVISIONING)

    def test_singleton(self):
        # Setup
        old_self = Self()
        self.assertEqual(old_self.node_id, ROUTING_PROVISIONING)
        self.assertEqual(old_self.node_type.node_type, TYPE_PROVISIONING)
        old_self.node_id = b'\x01\x23\x88'
        old_self.node_type = NodeType(TYPE_NODE)

        # Act
        new_self = Self()

        # Assert
        self.assertEqual(old_self.node_id, new_self.node_id)
        self.assertEqual(old_self.node_type.node_type, new_self.node_type.node_type)

    def test_reset(self):
        # Setup
        Self().node_id = b'\x01\x23\x88'
        Self().node_type = NodeType(TYPE_NODE)
        self.assertEqual(Self().node_id, b'\x01\x23\x88')
        self.assertEqual(Self().node_type.node_type, TYPE_NODE)
        
        # Act
        Self().reset()

        # Assert
        self.assertEqual(Self().node_id, ROUTING_PROVISIONING)
        self.assertEqual(Self().node_type.node_type, TYPE_PROVISIONING)
