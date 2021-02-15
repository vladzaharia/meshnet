from datetime import datetime, timedelta
from time import sleep

from meshnet.routing import Routing, RoutingEntry
from constants.headers import (
    FORMAT_RAW, 
    FORMAT_UTF8, 
    MESSAGE_MESH_CANCEL, 
    MESSAGE_SYS_GPS, 
    MESSAGE_SYS_HEARTBEAT, 
    MESSAGE_USR_TEXT, 
    NETWORK_DIRECT, 
    NETWORK_MESH, 
    PRIORITY_HIGH, 
    PRIORITY_LOW, 
    PRIORITY_REGULAR, 
    PRIORITY_URGENT
)
from constants.nodes import (
    TYPE_GATEWAY, 
    TYPE_NODE, 
    TYPE_NON_ROUTING
)
from meshnet.heartbeat import Heartbeat
from util.headers import Headers
from util.message import Message

def dbg(message: Message):
    headers_var = message.headers
    content_var = message.content

    message_type_var = headers_var.message_type

    headers_dbg(headers_var)
    print()

    print("# Content Debug #")
    print(content_var)

    if (message_type_var == MESSAGE_SYS_HEARTBEAT):
        heartbeat_dbg(content_var)
    
    routing_dbg()

def headers_dbg(header: Headers):
    print("# Header Debug #")
    print(header)
    print("Type: {0}".format(message_type_dbg(header)))
    print("Network: {0}".format(network_dbg(header)))
    print("Priority: {0}".format(priority_dbg(header)))
    print("Content Format: {0}".format(frmt_dbg(header)))
    print("---")
    print("Sender: {0}".format(header.sender))
    print("Recipient: {0}".format(header.recipient))
    print("Route Hint: {0}".format(header.mrh))

def message_type_dbg(header: Headers):
    message_type_var = header.message_type
    if (message_type_var == MESSAGE_SYS_HEARTBEAT):
        return "Sys - Heartbeat"
    elif (message_type_var == MESSAGE_SYS_GPS):
        return "Sys - GPS"
    elif (message_type_var == MESSAGE_USR_TEXT):
        return "User - Text"
    elif (message_type_var == MESSAGE_MESH_CANCEL):
        return "Mesh - Cancel relay"
    else:
        return "Unknown"

def network_dbg(header: Headers):
    network_var = header.network
    if (network_var == NETWORK_DIRECT):
        return "LoRa Direct"
    elif (network_var == NETWORK_MESH):
        return "LoRa Mesh"
    return "Unknown"

def priority_dbg(header: Headers):
    priority_var = header.priority
    if (priority_var == PRIORITY_URGENT):
        return "Urgent"
    elif (priority_var == PRIORITY_HIGH):
        return "High"
    elif (priority_var == PRIORITY_REGULAR):
        return "Regular"
    elif (priority_var == PRIORITY_LOW):
        return "Low"
    return "Unknown"

def frmt_dbg(header: Headers):
    frmt_var = header.frmt
    if (frmt_var == FORMAT_RAW):
        return "Raw"
    elif (frmt_var == FORMAT_UTF8):
        return "UTF-8"

def heartbeat_dbg(message: bytearray):
    heartbeat = Heartbeat().from_bytearray(message)
    print("# Heartbeat Debug #")
    print("ID: {0}".format(bytes(heartbeat.node_id)))
    print("Node Type: {0}".format(node_type_dbg(heartbeat.node_type)))
    print("Time: {0}".format(heartbeat.timestamp.strftime("%c")))
    print("Neighbors:")
    neighbors_dbg(heartbeat.routes)

def node_type_dbg(node_type_var: bytes):
    if (node_type_var == TYPE_NODE):
        return "Node"
    elif (node_type_var == TYPE_GATEWAY):
        return "Gateway"
    elif (node_type_var == TYPE_NON_ROUTING):
        return "SPECIAL - Non-Routing Node"
    else:
        return "Unknown"

def neighbors_dbg(routes: bytearray):
    num_routes = int(len(routes) / 3)
    for i in range(0, num_routes):
        print(bytes(routes[i*3:(i*3)+3]))

def routing_dbg():
    routing = Routing()
    
    print()
    print("# Routing Debug #")
    print_routes(routing.neighbors)

    for neighbor in routing.neighbors:
        neighbor.expiry = datetime.now() + timedelta(seconds = 5)

    print("Waiting for expiry to clean up...")
    sleep(5)
    routing.clean()
    print("Cleaned up!")
    
    print_routes(routing.neighbors)

def print_routes(routes: list[RoutingEntry]):
    for neighbor in routes:
        print("ID: {0}, Type: {1}, Expiry: {2}".format(neighbor.node_id, node_type_dbg(neighbor.node_type), neighbor.expiry.strftime("%c")))


