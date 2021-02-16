import unittest

from meshnet.routing import Routing
from meshnet.self import Self

class RoutingTest(unittest.TestCase):
    routing = Routing()

    def setUp(self):
        Self().reset()
        Routing().reset()
        self.routing = Routing()

    def test_default(self):
        pass

    def test_add_node(self):
        pass

    def test_add_gateway(self):
        pass

    def test_from_bytearray(self):
        pass

    def test_clean(self):
        pass

    def test_reset(self):
        pass