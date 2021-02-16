import unittest

from constants.headers import FORMAT_RAW, FORMAT_UTF8, MESSAGE_PROVISION, MESSAGE_SYS_GPS, MESSAGE_SYS_HEARTBEAT, MESSAGE_USR_TEXT, NETWORK_DIRECT, NETWORK_MESH, PRIORITY_HIGH, PRIORITY_LOW, PRIORITY_REGULAR, ROUTING_DIRECT, ROUTING_MULTICAST
from util.headers import Headers
from util.message import Message

class MessageTest(unittest.TestCase):
    headers = Headers()
    message = Message()

    def setUp(self):
        self.headers = Headers()
        self.message = Message(self.headers)

    def test_default(self):
        self.assertEqual(self.message.headers.message_type, b'\x00')
        self.assertEqual(self.message.headers.network, b'\x00')
        self.assertEqual(self.message.headers.priority, b'\x00')
        self.assertEqual(self.message.headers.frmt, b'\x00')
        self.assertEqual(self.message.headers.sender, b'\x00\x00\x00')
        self.assertEqual(self.message.headers.mrh, b'\x00\x00\x00')
        self.assertEqual(self.message.headers.recipient, b'\x00\x00\x00')

        self.assertEqual(bytes(self.message.to_bytearray()),b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

    def test_content(self):
        self.message = Message(self.headers, b'\xE4\xF6\x53\x87\x66\x0A')
        self.assertEqual(self.message.headers.frmt, b'\x00')
        self.assertEqual(self.message.content, b'\xE4\xF6\x53\x87\x66\x0A')

    def test_from_bytearray(self):
        self.message = Message().from_bytearray(bytearray(b'\x10\x10\x00\x00\x00\x00\x00\x99\x99\x99\x00\x00\x00\xff\xff\xff\x99\x99\x99\xff`+,\x96\x01\x01\x03\x01\x02\x03'))
        self.assertEqual(self.message.headers.message_type, MESSAGE_SYS_HEARTBEAT)
        self.assertEqual(self.message.headers.network, NETWORK_DIRECT)
        self.assertEqual(self.message.headers.priority, PRIORITY_LOW)
        self.assertEqual(self.message.headers.frmt, FORMAT_RAW)
        self.assertEqual(self.message.headers.sender, b'\x99\x99\x99')
        self.assertEqual(self.message.headers.mrh, b'\x00\x00\x00')
        self.assertEqual(self.message.headers.recipient, b'\xff\xff\xff')
        self.assertEqual(self.message.content, b'\x99\x99\x99\xff`+,\x96\x01\x01\x03\x01\x02\x03')

    def test_from_utf8(self):
        self.message = Message().from_utf8(self.headers, "Hello World")
        self.assertEqual(self.headers.frmt, FORMAT_UTF8)
        self.assertEqual(self.message.content, bytearray(bytes("Hello World", "utf-8")))

    def test_to_bytearray(self):
        self.headers = Headers(MESSAGE_USR_TEXT,
                                NETWORK_MESH,
                                PRIORITY_REGULAR,
                                FORMAT_RAW,
                                b'\x92\x12\x88',
                                ROUTING_MULTICAST,
                                b'\x98\xF7\xEE')
        self.message = Message(self.headers, b'\x82\xEB\xB9\xAA\xEA\xB4')
        self.assertEqual(self.message.to_bytearray(), bytearray(b'  @\x00\x00\x00\x00\x92\x12\x88\xff\xff\xff\x98\xf7\xee\x82\xeb\xb9\xaa\xea\xb4'))

    def test_reencode(self):
        self.headers = Headers(MESSAGE_SYS_GPS,
                                NETWORK_DIRECT,
                                PRIORITY_REGULAR,
                                FORMAT_RAW,
                                b'\x82\xF7\xCC',
                                ROUTING_DIRECT,
                                b'\xFE\xE8\x55')
        self.message = Message(self.headers, b'foobarbaz')

        new_message = Message().from_bytearray(self.message.to_bytearray())
        self.assertEqual(new_message.headers.message_type, MESSAGE_SYS_GPS)
        self.assertEqual(new_message.headers.network, NETWORK_DIRECT)
        self.assertEqual(new_message.headers.priority, PRIORITY_REGULAR)
        self.assertEqual(new_message.headers.frmt, FORMAT_RAW)
        self.assertEqual(new_message.headers.sender, b'\x82\xF7\xCC')
        self.assertEqual(new_message.headers.mrh, ROUTING_DIRECT)
        self.assertEqual(new_message.headers.recipient, b'\xFE\xE8\x55')
        self.assertEqual(new_message.content, b'foobarbaz')