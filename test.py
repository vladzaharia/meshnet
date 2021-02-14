from constants.node_types import NON_ROUTING_TEST
from meshnet.heartbeat import create_heartbeat

# Create Message
self = b'\x01\x02\x03'
message = create_heartbeat(self, NON_ROUTING_TEST, [])
print(message)