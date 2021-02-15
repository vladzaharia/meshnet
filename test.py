from constants.globals import NODE_ID, NODE_TYPE
from constants.nodes import TYPE_NODE
from meshnet.heartbeat import Heartbeat
from meshnet.routing import Routing, RoutingEntry
from util.debug import dbg

# Initialize Routing
routing = Routing()
routing.add(RoutingEntry(b'\x01\x01\x03', TYPE_NODE))
routing.add(RoutingEntry(b'\x01\x02\x03', TYPE_NODE))

# Create Message
message = Heartbeat(NODE_ID, NODE_TYPE).create()
print(message)

dbg(message)