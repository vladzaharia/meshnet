from constants.headers import MESSAGE_SYS_HEARTBEAT, NETWORK_DIRECT, PRIORITY_LOW, ROUTING_DIRECT, ROUTING_MULTICAST;
from util.message import create_raw;

def create_heartbeat(self: bytes, node_type: bytes, routes):
    return create_raw(MESSAGE_SYS_HEARTBEAT, 
                        NETWORK_DIRECT, 
                        PRIORITY_LOW, 
                        self,
                        ROUTING_DIRECT,
                        ROUTING_MULTICAST,
                        create_heartbeat_content(self, node_type, enumerate_routes(routes)))

def create_heartbeat_content(self: bytes, node_type: bytes, routes):
    message_len = len(routes) + 8
    message = bytearray(message_len)

    message[0:2] = self
    message[3:3] = node_type

    # 4 - 7 reserved

    message[8:message_len-1] = routes

    return message

def enumerate_routes(routes):
    return b''
