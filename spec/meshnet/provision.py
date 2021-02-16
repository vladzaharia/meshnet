import unittest

from meshnet.provision import Provision
from meshnet.routing import Routing
from meshnet.self import Self

class ProvisionTest(unittest.TestCase):
    provision = Provision()

    def setUp(self):
        self.provision = Provision()
        Self().reset()
        Routing().reset()

    def test_default(self):
        pass

    def test_set_id(self):
        pass

    def test_reencode(self):
        pass

    def test_process(self):
        pass