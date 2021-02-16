from datetime import datetime, timedelta
import struct
from constants.headers import MESSAGE_SYS_HEARTBEAT, NETWORK_DIRECT, PRIORITY_LOW, ROUTING_DIRECT, ROUTING_MULTICAST
import unittest

from constants.nodetype import TYPE_GATEWAY, TYPE_GATEWAY_TIME, TYPE_NODE, TYPE_NODE_NR, TYPE_PROVISIONING
from meshnet.heartbeat import Heartbeat
from meshnet.routing import Routing, RoutingEntry
from meshnet.self import Self
from util.nodetype import NodeType

class HeartbeatTest(unittest.TestCase):
    heartbeat = Heartbeat()

    def setUp(self):
        Self().reset()
        Routing().reset()
        self.heartbeat = Heartbeat()

    # E2E
    def test_default(self):
        self.assertEqual(self.heartbeat.node_id, Self().node_id)
        self.assertEqual(self.heartbeat.node_type.node_type, Self().node_type.node_type)
        self.assertEqual(len(self.heartbeat.routes), 0)

    def test_add_neighbors(self):
        Routing().add(RoutingEntry(b'\x78\xB7\xBD', NodeType(b'\x10')))
        Routing().add(RoutingEntry(b'\x5D\xA9\xEE', NodeType(b'\x20')))
        self.heartbeat = Heartbeat()

        # Force creation of routes
        self.heartbeat.create_routes()
        self.assertEqual(len(self.heartbeat.routes), 6)
        self.assertEqual(self.heartbeat.routes, b'\x78\xB7\xBD\x5D\xA9\xEE')

    def test_reencode(self):
        Routing().add(RoutingEntry(b'\x8B\x12\xB6', NodeType(TYPE_NODE)))
        Routing().add(RoutingEntry(b'\xCA\xA2\x2B', NodeType(TYPE_GATEWAY_TIME)))
        self.heartbeat = Heartbeat(b'\xFE\xA7\xAB', NodeType(TYPE_GATEWAY))

        new_message = self.heartbeat.to_message()
        new_heartbeat = Heartbeat().from_bytearray(new_message.content)
        self.assertEqual(new_heartbeat.node_id, b'\xFE\xA7\xAB')
        self.assertEqual(new_heartbeat.node_type.node_type, TYPE_GATEWAY)
        self.assertEqual(len(new_heartbeat.routes), 6)
        self.assertEqual(new_heartbeat.routes, b'\x8B\x12\xB6\xCA\xA2\x2B')

    # Functions
    def test_from_bytearray(self):
        self.heartbeat = Heartbeat().from_bytearray(bytearray(b'\xfe\xa7\xab `+?\x17\x8b\x12\xb6\xca\xa2+'))
        self.assertEqual(self.heartbeat.node_id, b'\xFE\xA7\xAB')
        self.assertEqual(self.heartbeat.node_type.node_type, TYPE_GATEWAY)
        self.assertEqual(len(self.heartbeat.routes), 6)
        self.assertEqual(self.heartbeat.routes, b'\x8B\x12\xB6\xCA\xA2\x2B')

    def test_to_message(self):
        message = self.heartbeat.to_message()
        headers = message.headers
        self.assertEqual(headers.message_type, MESSAGE_SYS_HEARTBEAT)
        self.assertEqual(headers.network, NETWORK_DIRECT)
        self.assertEqual(headers.priority, PRIORITY_LOW)
        self.assertEqual(headers.sender, Self().node_id)
        self.assertEqual(headers.mrh, ROUTING_DIRECT)
        self.assertEqual(headers.recipient, ROUTING_MULTICAST)
        
        new_heartbeat = Heartbeat().from_bytearray(message.content)
        self.assertEqual(new_heartbeat.node_id, Self().node_id)
        self.assertEqual(new_heartbeat.node_type.node_type, Self().node_type.node_type)
        self.assertEqual(len(new_heartbeat.routes), 0)

    def test_get_time(self):
        dt_now = datetime.now()
        timestamp = int(datetime.timestamp(dt_now))
        timestamp_bytes = struct.pack(">i", timestamp)

        self.assertEqual(self.heartbeat.get_time(), timestamp_bytes)

    def test_set_time(self):
        dt_now = datetime.now() + timedelta(minutes = 1)
        timestamp = int(datetime.timestamp(dt_now))
        timestamp_bytes = struct.pack(">i", timestamp)
        self.heartbeat.set_time(timestamp_bytes)
        new_timestamp = datetime.fromtimestamp(float(struct.unpack(">i", timestamp_bytes)[0]))
        
        self.assertEqual(self.heartbeat.timestamp, new_timestamp)

    def test_process(self):
        Heartbeat(b'\x67\x10\x22', NodeType(TYPE_GATEWAY)).process()
        Heartbeat(b'\x29\x12\x4A', NodeType(TYPE_NODE)).process()
        Heartbeat(b'\x01\x02\x03', NodeType(TYPE_NODE_NR)).process() # ignored
        Heartbeat(b'\x99\x99\x99', NodeType(TYPE_PROVISIONING)).process() # ignored
        
        routing = Routing()
        self.assertEqual(len(routing.neighbors), 2)
        first_neighbor = routing.neighbors[0]
        self.assertEqual(first_neighbor.node_id, b'\x67\x10\x22')
        self.assertEqual(first_neighbor.node_type.node_type, TYPE_GATEWAY)

        second_neighbor = routing.neighbors[1]
        self.assertEqual(second_neighbor.node_id, b'\x29\x12\x4A')
        self.assertEqual(second_neighbor.node_type.node_type, TYPE_NODE)