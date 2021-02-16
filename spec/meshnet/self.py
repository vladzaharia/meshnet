import unittest

from meshnet.self import Self

class SelfTest(unittest.TestCase):
    self_obj = Self()

    def setUp(self):
        Self().reset()

    def test_default(self):
        pass

    def test_singleton(self):
        pass

    def test_reset(self):
        pass