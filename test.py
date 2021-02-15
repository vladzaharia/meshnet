from constants.nodetype import TYPE_GATEWAY, TYPE_NODE
from meshnet.heartbeat import Heartbeat, proccess_heartbeat
from meshnet.routing import Routing, RoutingEntry
from util.debug import dbg, routing_dbg
from util.nodetype import NodeType

# Initialize Routing
routing = Routing()
routing.add(RoutingEntry(b'\x01\x01\x03', NodeType(TYPE_NODE)))
routing.add(RoutingEntry(b'\x01\x02\x03', NodeType(TYPE_GATEWAY)))

# Create Message
heartbeat = Heartbeat()
message = heartbeat.create()
print(message.create())

dbg(message)

print("Processing heartbeat")
heartbeat.node_type = NodeType(TYPE_NODE)
proccess_heartbeat(heartbeat)
routing_dbg()