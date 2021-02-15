from meshnet.routing import Routing
from constants.globals import *;
from constants.headers import (
    FORMAT_RAW, MESSAGE_SYS_HEARTBEAT, 
    NETWORK_DIRECT, 
    PRIORITY_LOW, 
    ROUTING_DIRECT, 
    ROUTING_MULTICAST
);
from util.message import Message;
from util.headers import Headers

class Heartbeat:
    node_id: bytes
    node_type: bytes
    headers: Headers
    routes: bytearray

    def __init__(self, node_id: bytes = b'\x00\x00\x00', node_type: bytes = b'') -> None:
        self.node_id = node_id
        self.node_type = node_type
        self.headers = Headers(MESSAGE_SYS_HEARTBEAT,
                                NETWORK_DIRECT,
                                PRIORITY_LOW,
                                FORMAT_RAW,
                                NODE_ID,
                                ROUTING_DIRECT,
                                ROUTING_MULTICAST)
        self.routes = bytearray()

    @classmethod
    def from_bytearray(self, raw: bytearray):
        obj = self(raw[0:3], raw[3:4])
        obj.routes = raw[8:]
        return obj

    def create(self):
        self.create_routes()

        routes = self.routes
        message_len = len(routes) + 8
        message = bytearray(message_len)

        message[0:2] = self.node_id
        message[3:3] = self.node_type
        # 4 - 7 reserved
        message[8:] = routes

        return Message(self.headers, message)

    def create_routes(self):
        routing = Routing()
        neighbors = routing.neighbors

        self.routes = bytearray(len(neighbors) * 3)
        i = 0

        for neighbor in routing.neighbors:
            self.routes[i:i+3] = neighbor.node_id
            i = i + 3