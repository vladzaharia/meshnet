from util.debug import dbg
from meshnet.heartbeat import create_heartbeat

# Create Message
message = create_heartbeat()
print(message)

dbg(message)