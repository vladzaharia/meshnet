from constants.nodetype import TYPE_GATEWAY, TYPE_NODE
from meshnet.heartbeat import Heartbeat
from meshnet.routing import Routing, RoutingEntry
from util.debug import dbg

# Initialize Routing
routing = Routing()
routing.add(RoutingEntry(b'\x01\x01\x03', TYPE_NODE))
routing.add(RoutingEntry(b'\x01\x02\x03', TYPE_GATEWAY))

# Create Message
message = Heartbeat().create()
print(message.create())

dbg(message)