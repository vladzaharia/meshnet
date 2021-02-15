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

def create_heartbeat():
    headers = Headers(MESSAGE_SYS_HEARTBEAT,
                      NETWORK_DIRECT,
                      PRIORITY_LOW,
                      FORMAT_RAW,
                      NODE_ID,
                      ROUTING_DIRECT,
                      ROUTING_MULTICAST)
    message = Message(headers, create_heartbeat_content(NODE_ID, NODE_TYPE, enumerate_routes()))
    return message
                        

def create_heartbeat_content(self: bytes, node_type: bytes, routes):
    message_len = len(routes) + 8
    message = bytearray(message_len)

    message[0:2] = self
    message[3:3] = node_type

    # 4 - 7 reserved

    message[8:message_len-1] = routes

    return message

def enumerate_routes():
    return b''

def node_id(message: bytearray):
    return bytes(message[0:3])

def node_type(message: bytearray):
    return bytes(message[3:4])
