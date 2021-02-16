import unittest

from constants.headers import MESSAGE_PROVISION, NETWORK_DIRECT, PRIORITY_LOW, ROUTING_DIRECT, ROUTING_PROVISIONING
from constants.nodetype import TYPE_GATEWAY, TYPE_PROVISIONING
from meshnet.provision import Provision
from meshnet.routing import Routing
from meshnet.self import Self

class ProvisionTest(unittest.TestCase):
    provision = Provision()

    def setUp(self):
        Self().reset()
        Routing().reset()
        self.provision = Provision()

    # E2E
    def test_default(self):
        # Assert
        self.assertEqual(self.provision.node_id, ROUTING_PROVISIONING)

        headers = self.provision.headers
        self.assertEqual(headers.message_type, MESSAGE_PROVISION)
        self.assertEqual(headers.network, NETWORK_DIRECT)
        self.assertEqual(headers.priority, PRIORITY_LOW)
        self.assertEqual(headers.sender, Self.node_id)
        self.assertEqual(headers.mrh, ROUTING_DIRECT)
        self.assertEqual(headers.recipient, ROUTING_PROVISIONING)

    def test_reencode(self):
        pass

    # Functions
    def test_from_rawbytes(self):
        pass

    def test_provision_node_id(self):
        # Setup
        self.assertEqual(Self().node_id, ROUTING_PROVISIONING)

        # Act
        self.provision.provision_node_id(b'\x07\xB4\xAE')
        self.provision.process()

        # Assert
        self.assertEqual(Self().node_id, b'\x07\xB4\xAE')

    def test_provision_node_type(self):
        # Setup
        self.assertEqual(Self().node_type.node_type, TYPE_PROVISIONING)

        # Act
        self.provision.provision_node_type(TYPE_GATEWAY)
        self.provision.process()

        # Assert
        self.assertEqual(Self().node_type.node_type, TYPE_GATEWAY)

    def test_create_message(self):
        pass

    def test_process(self):
        pass