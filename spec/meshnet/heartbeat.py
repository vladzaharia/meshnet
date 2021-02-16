import unittest

from meshnet.heartbeat import Heartbeat
from meshnet.routing import Routing
from meshnet.self import Self

class HeartbeatTest(unittest.TestCase):
    heartbeat = Heartbeat()

    def setUp(self):
        self.heartbeat = Heartbeat()
        Self().reset()
        Routing().reset()

    def test_default(self):
        pass

    def test_add_neighbors(self):
        pass

    def test_reencode(self):
        pass

    def test_process(self):
        pass