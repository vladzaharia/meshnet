import unittest

from constants.headers import FORMAT_RAW, FORMAT_UTF8, MESSAGE_PROVISION, MESSAGE_SYS_GPS, NETWORK_MESH, PRIORITY_HIGH, PRIORITY_REGULAR, ROUTING_MULTICAST
from util.headers import Headers

class HeadersTest(unittest.TestCase):
    headers = Headers()

    def setUp(self):
        self.headers = Headers()

    def test_default(self):
        self.assertEqual(self.headers.message_type, b'')
        self.assertEqual(self.headers.network, b'')
        self.assertEqual(self.headers.priority, b'')
        self.assertEqual(self.headers.frmt, b'')
        self.assertEqual(self.headers.sender, b'\x00\x00\x00')
        self.assertEqual(self.headers.mrh, b'\x00\x00\x00')
        self.assertEqual(self.headers.recipient, b'\x00\x00\x00')

        self.assertEqual(bytes(self.headers.to_bytearray()),b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

    def test_change(self):
        self.headers.message_type = MESSAGE_PROVISION
        self.headers.network = NETWORK_MESH
        self.headers.priority = PRIORITY_HIGH
        self.headers.frmt = FORMAT_UTF8
        self.headers.sender = b'\x05\x89\xE4'
        self.headers.mrh = ROUTING_MULTICAST
        self.headers.recipient = b'\x18\xAE\xF8'

        bytes = self.headers.to_bytearray()

        self.assertEqual(bytes,b'\xff \x80\x10\x00\x00\x00\x05\x89\xe4\xff\xff\xff\x18\xae\xf8\x00')

    def test_reencode(self):
        self.headers = Headers(MESSAGE_SYS_GPS,
                                NETWORK_MESH,
                                PRIORITY_REGULAR,
                                FORMAT_RAW,
                                b'\x12\x38\xB4',
                                ROUTING_MULTICAST,
                                ROUTING_MULTICAST)

        new_headers = Headers().from_bytearray(self.headers.to_bytearray())
        self.assertEqual(new_headers.message_type, MESSAGE_SYS_GPS)
        self.assertEqual(new_headers.network, NETWORK_MESH)
        self.assertEqual(new_headers.priority, PRIORITY_REGULAR)
        self.assertEqual(new_headers.frmt, FORMAT_RAW)
        self.assertEqual(new_headers.sender, b'\x12\x38\xB4')
        self.assertEqual(new_headers.mrh, ROUTING_MULTICAST)
        self.assertEqual(new_headers.recipient, ROUTING_MULTICAST)

if __name__ == '__main__': 
    unittest.main() 