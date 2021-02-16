from datetime import datetime, timedelta
import unittest

from constants.headers import (
    FORMAT_RAW, 
    MESSAGE_SYS_HEARTBEAT, 
    NETWORK_MESH, 
    PRIORITY_HIGH, 
    PRIORITY_LOW, 
    PRIORITY_REGULAR, 
    PRIORITY_URGENT, 
    ROUTING_MULTICAST
)
from constants.nodetype import TYPE_GATEWAY, TYPE_NODE
from meshnet.queue import MessageQueue
from meshnet.routing import Routing
from meshnet.self import Self
from util.headers import Headers
from util.message import Message
from util.nodetype import NodeType

class MessageQueueTest(unittest.TestCase):
    queue: MessageQueue

    def setUp(self):
        MessageQueue().reset()
        Routing().reset()
        Self().reset()
        self.queue = MessageQueue()

    # E2E
    def test_default(self):
        # Assert
        self.assertEqual(len(self.queue.queue_entries), 0)

    def test_add_node_urgent(self):
        # Setup
        Self().node_type = NodeType(TYPE_NODE)
        message = Message(
                    Headers(MESSAGE_SYS_HEARTBEAT, 
                            NETWORK_MESH, 
                            PRIORITY_URGENT, 
                            FORMAT_RAW, 
                            b'\x12\x92\xF3',
                            ROUTING_MULTICAST,
                            b'\x19\x28\x20'), 
                    b'foobarbaz')

        # Act
        self.queue.add(message)
        
        # Assert
        entry = self.queue.queue_entries[0]
        self.assertEqual(entry.message, message)
        self.assertAlmostEqual(entry.expiry, datetime.now() + timedelta(hours = 1), delta = timedelta(seconds = 1))
        self.assertAlmostEqual(entry.next_scheduled_time, datetime.now() + timedelta(minutes = 5), delta = timedelta(seconds = 1))
        self.assertEqual(entry.timediff, timedelta(minutes = 5))
        self.assertFalse(entry.single_hop)

    def test_add_node_high(self):
        # Setup
        Self().node_type = NodeType(TYPE_NODE)
        message = Message(
                    Headers(MESSAGE_SYS_HEARTBEAT, 
                            NETWORK_MESH, 
                            PRIORITY_HIGH, 
                            FORMAT_RAW, 
                            b'\x12\x92\xF3',
                            ROUTING_MULTICAST,
                            b'\x19\x28\x20'), 
                    b'foobarbaz')

        # Act
        self.queue.add(message)
        
        # Assert
        entry = self.queue.queue_entries[0]
        self.assertEqual(entry.message, message)
        self.assertAlmostEqual(entry.expiry, datetime.now() + timedelta(minutes = 30), delta = timedelta(seconds = 1))
        self.assertAlmostEqual(entry.next_scheduled_time, datetime.now() + timedelta(minutes = 15), delta = timedelta(seconds = 1))
        self.assertEqual(entry.timediff, timedelta(minutes = 15))
        self.assertFalse(entry.single_hop)

    def test_add_node_regular(self):
        # Setup
        Self().node_type = NodeType(TYPE_NODE)
        message = Message(
                    Headers(MESSAGE_SYS_HEARTBEAT, 
                            NETWORK_MESH, 
                            PRIORITY_REGULAR, 
                            FORMAT_RAW, 
                            b'\x12\x92\xF3',
                            ROUTING_MULTICAST,
                            b'\x19\x28\x20'), 
                    b'foobarbaz')

        # Act
        self.queue.add(message)
        
        # Assert
        entry = self.queue.queue_entries[0]
        self.assertEqual(entry.message, message)
        self.assertAlmostEqual(entry.expiry, datetime.now() + timedelta(minutes = 5), delta = timedelta(seconds = 1))
        self.assertAlmostEqual(entry.next_scheduled_time, datetime.now() + timedelta(minutes = 5), delta = timedelta(seconds = 1))
        self.assertEqual(entry.timediff, timedelta(minutes = 5))
        self.assertFalse(entry.single_hop)

    def test_add_node_low(self):
        # Setup
        Self().node_type = NodeType(TYPE_NODE)
        message = Message(
                    Headers(MESSAGE_SYS_HEARTBEAT, 
                            NETWORK_MESH, 
                            PRIORITY_LOW, 
                            FORMAT_RAW, 
                            b'\x12\x92\xF3',
                            ROUTING_MULTICAST,
                            b'\x19\x28\x20'), 
                    b'foobarbaz')

        # Act
        self.queue.add(message)
        
        # Assert
        entry = self.queue.queue_entries[0]
        message.headers.mrh = Self().node_id

        self.assertEqual(entry.message, message)
        self.assertAlmostEqual(entry.expiry, datetime.now() + timedelta(minutes = 5), delta = timedelta(seconds = 1))
        self.assertAlmostEqual(entry.next_scheduled_time, datetime.now() + timedelta(minutes = 5), delta = timedelta(seconds = 1))
        self.assertEqual(entry.timediff, timedelta(minutes = 5))
        self.assertTrue(entry.single_hop)

    def test_add_gateway_urgent(self):
        # Setup
        Self().node_type = NodeType(TYPE_GATEWAY)
        message = Message(
                    Headers(MESSAGE_SYS_HEARTBEAT, 
                            NETWORK_MESH, 
                            PRIORITY_URGENT, 
                            FORMAT_RAW, 
                            b'\x12\x92\xF3',
                            ROUTING_MULTICAST,
                            b'\x19\x28\x20'), 
                    b'foobarbaz')

        # Act
        self.queue.add(message)
        
        # Assert
        entry = self.queue.queue_entries[0]
        self.assertEqual(entry.message, message)
        self.assertAlmostEqual(entry.expiry, datetime.now() + timedelta(hours = 6), delta = timedelta(seconds = 1))
        self.assertAlmostEqual(entry.next_scheduled_time, datetime.now() + timedelta(minutes = 15), delta = timedelta(seconds = 1))
        self.assertEqual(entry.timediff, timedelta(minutes = 15))
        self.assertFalse(entry.single_hop)

    def test_add_gateway_high(self):
        # Setup
        Self().node_type = NodeType(TYPE_GATEWAY)
        message = Message(
                    Headers(MESSAGE_SYS_HEARTBEAT, 
                            NETWORK_MESH, 
                            PRIORITY_HIGH, 
                            FORMAT_RAW, 
                            b'\x12\x92\xF3',
                            ROUTING_MULTICAST,
                            b'\x19\x28\x20'), 
                    b'foobarbaz')

        # Act
        self.queue.add(message)
        
        # Assert
        entry = self.queue.queue_entries[0]
        self.assertEqual(entry.message, message)
        self.assertAlmostEqual(entry.expiry, datetime.now() + timedelta(hours = 1), delta = timedelta(seconds = 1))
        self.assertAlmostEqual(entry.next_scheduled_time, datetime.now() + timedelta(minutes = 15), delta = timedelta(seconds = 1))
        self.assertEqual(entry.timediff, timedelta(minutes = 15))
        self.assertFalse(entry.single_hop)

    def test_add_node_regular(self):
        # Setup
        Self().node_type = NodeType(TYPE_NODE)
        message = Message(
                    Headers(MESSAGE_SYS_HEARTBEAT, 
                            NETWORK_MESH, 
                            PRIORITY_REGULAR, 
                            FORMAT_RAW, 
                            b'\x12\x92\xF3',
                            ROUTING_MULTICAST,
                            b'\x19\x28\x20'), 
                    b'foobarbaz')

        # Act
        self.queue.add(message)
        
        # Assert
        entry = self.queue.queue_entries[0]
        self.assertEqual(entry.message, message)
        self.assertAlmostEqual(entry.expiry, datetime.now() + timedelta(minutes = 10), delta = timedelta(seconds = 1))
        self.assertAlmostEqual(entry.next_scheduled_time, datetime.now() + timedelta(minutes = 5), delta = timedelta(seconds = 1))
        self.assertEqual(entry.timediff, timedelta(minutes = 5))
        self.assertFalse(entry.single_hop)

    def test_add_gateway_low(self):
        # Setup
        Self().node_type = NodeType(TYPE_GATEWAY)
        message = Message(
                    Headers(MESSAGE_SYS_HEARTBEAT, 
                            NETWORK_MESH, 
                            PRIORITY_LOW, 
                            FORMAT_RAW, 
                            b'\x12\x92\xF3',
                            ROUTING_MULTICAST,
                            b'\x19\x28\x20'), 
                    b'foobarbaz')

        # Act
        self.queue.add(message)
        
        # Assert
        entry = self.queue.queue_entries[0]
        message.headers.mrh = Self().node_id
        
        self.assertEqual(entry.message, message)
        self.assertAlmostEqual(entry.expiry, datetime.now() + timedelta(minutes = 15), delta = timedelta(seconds = 1))
        self.assertAlmostEqual(entry.next_scheduled_time, datetime.now() + timedelta(minutes = 15), delta = timedelta(seconds = 1))
        self.assertEqual(entry.timediff, timedelta(minutes = 15))
        self.assertTrue(entry.single_hop)

    # Functions
    def test_process_schedule(self):
        # Setup
        Self().node_type = NodeType(TYPE_GATEWAY)
        message = Message(
                    Headers(MESSAGE_SYS_HEARTBEAT, 
                            NETWORK_MESH, 
                            PRIORITY_HIGH, 
                            FORMAT_RAW, 
                            b'\x12\x92\xF3',
                            ROUTING_MULTICAST,
                            b'\x19\x28\x20'), 
                    b'foobarbaz')
        self.queue.add(message)
        self.queue.queue_entries[0].next_scheduled_time = datetime.now() - timedelta(seconds = 5)

        # Act
        self.queue._process_schedule()

        # Assert
        self.assertAlmostEqual(self.queue.queue_entries[0].last_run, datetime.now(), delta = timedelta(seconds = 1))

    def test_process_expiry(self):
        # Setup
        Self().node_type = NodeType(TYPE_GATEWAY)
        message = Message(
                    Headers(MESSAGE_SYS_HEARTBEAT, 
                            NETWORK_MESH, 
                            PRIORITY_HIGH, 
                            FORMAT_RAW, 
                            b'\x12\x92\xF3',
                            ROUTING_MULTICAST,
                            b'\x19\x28\x20'), 
                    b'foobarbaz')
        self.queue.add(message)
        self.queue.queue_entries[0].expiry = datetime.now() - timedelta(seconds = 5)

        # Act
        self.queue._process_expiry()

        # Assert
        self.assertEqual(len(self.queue.queue_entries), 0)

    def test_reset(self):
        # Setup
        message = Message(
                    Headers(MESSAGE_SYS_HEARTBEAT, 
                            NETWORK_MESH, 
                            PRIORITY_HIGH, 
                            FORMAT_RAW, 
                            b'\x12\x92\xF3',
                            ROUTING_MULTICAST,
                            b'\x19\x28\x20'), 
                    b'foobarbaz')
        self.queue.add(message)

        # Act
        self.queue.reset()

        # Assert
        self.assertEqual(len(self.queue.queue_entries), 0)

