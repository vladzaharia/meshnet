import unittest

from spec.meshnet.heartbeat import HeartbeatTest
from spec.meshnet.provision import ProvisionTest
from spec.meshnet.queue import MessageQueueTest
from spec.meshnet.routing import RoutingTest
from spec.meshnet.self import SelfTest
from spec.util.headers import HeadersTest
from spec.util.message import MessageTest
from spec.util.nodetype import NodeTypeTest

# MeshNet Tests
HeartbeatTest()
MessageQueueTest()
ProvisionTest()
RoutingTest()
SelfTest()

# Util Tests
HeadersTest()
MessageTest()
NodeTypeTest()

if __name__ == '__main__': 
    unittest.main() 