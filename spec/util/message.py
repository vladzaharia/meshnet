import unittest

from constants.headers import FORMAT_RAW, FORMAT_UTF8, MESSAGE_PROVISION, MESSAGE_SYS_GPS, NETWORK_MESH, PRIORITY_HIGH, PRIORITY_REGULAR, ROUTING_MULTICAST
from util.headers import Headers
from util.message import Message

class MessageTest(unittest.TestCase):
    headers = Headers()
    message = Message()

    def setUp(self):
        self.headers = Headers()
        self.message = Message(self.headers)

    def test_default(self):
        pass

    def test_reencode(self):
        pass