from util.nodetype import NodeType
from constants.headers import (
    FORMAT_RAW, 
    MESSAGE_PROVISION, 
    NETWORK_DIRECT, 
    PRIORITY_LOW, 
    ROUTING_DIRECT, 
    ROUTING_PROVISIONING
)
from meshnet.self import Self
from util.headers import Headers
from util.message import Message

# This will need to eventually be more secure
ADMIN_TOKEN: bytes = b'yufboPkn'

OPERATION_SET_NODE_ID = b'\x10'
OPERATION_SET_NODE_TYPE = b'\x20'

class Provision:
    node_id: bytes
    headers: Headers
    operation: bytes
    content: bytes

    def __init__(self, node_id = ROUTING_PROVISIONING) -> None:
        self.node_id = node_id
        self.headers = Headers(MESSAGE_PROVISION,
                                NETWORK_DIRECT,
                                PRIORITY_LOW,
                                FORMAT_RAW,
                                Self().node_id,
                                ROUTING_DIRECT,
                                self.node_id)
    
    @classmethod
    def from_rawbytes(self, raw: bytearray):
        message = Message().from_bytearray(raw)
        obj = self(message.headers.recipient)
        obj.headers = message.headers
        obj.content = message.content
        return obj

    def provision_node_id(self, node_id: bytes):
        self.operation = OPERATION_SET_NODE_ID
        self.content = node_id
        message: Message = self._create_message()

        # Update Node ID for future requests
        self.node_id = node_id
        self.headers = Headers(MESSAGE_PROVISION,
                                NETWORK_DIRECT,
                                PRIORITY_LOW,
                                FORMAT_RAW,
                                Self().node_id,
                                ROUTING_DIRECT,
                                self.node_id)

        return message

    def provision_node_type(self, node_type: bytes):
        self.operation = OPERATION_SET_NODE_TYPE
        self.content = node_type

        return self._create_message()

    def _create_message(self):
        message_len = len(self.content) + 12
        message = bytearray(message_len)

        message[0:1] = self.operation
        # 1 - 3 are reserved
        message[4:12] = ADMIN_TOKEN
        message[12:] = self.content

        return Message(self.headers, message)

    def process(self):
        if (self.operation == OPERATION_SET_NODE_ID):
            Self().node_id = self.content
        elif (self.operation == OPERATION_SET_NODE_TYPE):
            Self().node_type = NodeType(self.content)