from constants.nodetype import TYPE_GATEWAY, TYPE_NODE
from meshnet.heartbeat import Heartbeat
from meshnet.routing import Routing, RoutingEntry
from util.debug import dbg, routing_dbg
from util.nodetype import NodeType

# Initialize Routing
routing = Routing()
routing.add(RoutingEntry(b'\x01\x01\x03', NodeType(TYPE_NODE)))
routing.add(RoutingEntry(b'\x01\x02\x03', NodeType(TYPE_GATEWAY)))

# Create Message
message = Heartbeat().to_message()
print(message.to_bytearray())

dbg(message)

print("Processing heartbeat")
heartbeat = Heartbeat().from_bytearray(message.content)
heartbeat.node_type = NodeType(TYPE_NODE)
heartbeat.proccess()
routing_dbg()