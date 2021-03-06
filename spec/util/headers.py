import unittest

from constants.headers import (
    FORMAT_RAW, 
    FORMAT_UTF8, 
    MESSAGE_MESH_CANCEL, 
    MESSAGE_PROVISION, 
    MESSAGE_SYS_GPS, 
    NETWORK_MESH, 
    PRIORITY_HIGH, 
    PRIORITY_REGULAR, 
    ROUTING_MULTICAST
)
from util.headers import Headers

class HeadersTest(unittest.TestCase):
    headers = Headers()

    def setUp(self):
        self.headers = Headers()

    # E2E
    def test_default(self):
        # Assert
        self.assertEqual(self.headers.message_type, b'\x00')
        self.assertEqual(self.headers.network, b'\x00')
        self.assertEqual(self.headers.priority, b'\x00')
        self.assertEqual(self.headers.frmt, b'\x00')
        self.assertEqual(self.headers.sender, b'\x00\x00\x00')
        self.assertEqual(self.headers.mrh, b'\x00\x00\x00')
        self.assertEqual(self.headers.recipient, b'\x00\x00\x00')
        self.assertEqual(bytes(self.headers.to_bytearray()),b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

    def test_change(self):
        # Setup
        self.headers.message_type = MESSAGE_PROVISION
        self.headers.network = NETWORK_MESH
        self.headers.priority = PRIORITY_HIGH
        self.headers.frmt = FORMAT_UTF8
        self.headers.sender = b'\x05\x89\xE4'
        self.headers.mrh = ROUTING_MULTICAST
        self.headers.recipient = b'\x18\xAE\xF8'

        # Act
        bytes = self.headers.to_bytearray()

        # Assert
        self.assertEqual(bytes,b'\xff \x80\x10\x00\x00\x00\x05\x89\xe4\xff\xff\xff\x18\xae\xf8')

    def test_reencode(self):
        # Setup
        self.headers = Headers(MESSAGE_SYS_GPS,
                                NETWORK_MESH,
                                PRIORITY_REGULAR,
                                FORMAT_RAW,
                                b'\x12\x38\xB4',
                                ROUTING_MULTICAST,
                                ROUTING_MULTICAST)

        # Act
        new_headers = Headers().from_bytearray(self.headers.to_bytearray())

        # Assert
        self.assertEqual(new_headers.message_type, MESSAGE_SYS_GPS)
        self.assertEqual(new_headers.network, NETWORK_MESH)
        self.assertEqual(new_headers.priority, PRIORITY_REGULAR)
        self.assertEqual(new_headers.frmt, FORMAT_RAW)
        self.assertEqual(new_headers.sender, b'\x12\x38\xB4')
        self.assertEqual(new_headers.mrh, ROUTING_MULTICAST)
        self.assertEqual(new_headers.recipient, ROUTING_MULTICAST)

    # Functions
    def test_from_bytearray(self):
        # Act
        self.headers = Headers().from_bytearray(bytearray(b'\xff \x80\x10\x00\x00\x00\x05\x89\xe4\xff\xff\xff\x18\xae\xf8'))
        
        # Assert
        self.assertEqual(self.headers.message_type, MESSAGE_PROVISION)
        self.assertEqual(self.headers.network, NETWORK_MESH)
        self.assertEqual(self.headers.priority, PRIORITY_HIGH)
        self.assertEqual(self.headers.frmt, FORMAT_UTF8)
        self.assertEqual(self.headers.sender, b'\x05\x89\xE4')
        self.assertEqual(self.headers.mrh, ROUTING_MULTICAST)
        self.assertEqual(self.headers.recipient, b'\x18\xAE\xF8')

    def test_to_bytearray(self):
        # Setup
        self.headers = Headers(MESSAGE_MESH_CANCEL,
                                NETWORK_MESH,
                                PRIORITY_HIGH,
                                FORMAT_RAW,
                                b'\x83\x23\x09',
                                ROUTING_MULTICAST,
                                b'\x12\x29\x29')

        # Act + Assert
        self.assertEqual(self.headers.to_bytearray(), bytearray(b'\xf0 \x80\x00\x00\x00\x00\x83#\t\xff\xff\xff\x12))'))

if __name__ == '__main__': 
    unittest.main() 