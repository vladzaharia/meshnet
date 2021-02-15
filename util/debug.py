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
    print("ID: {0}".format(heartbeat.node_id))
    print("Node Type: {0}".format(node_type_dbg(heartbeat)))
    print("Neighbors: {0}".format(heartbeat.routes))

def node_type_dbg(heartbeat: Heartbeat):
    node_type_var = heartbeat.node_type
    if (node_type_var == TYPE_NODE):
        return "Node"
    elif (node_type_var == TYPE_GATEWAY):
        return "Gateway"
    elif (node_type_var == TYPE_NON_ROUTING):
        return "SPECIAL - Non-Routing Node"
    else:
        return "Unknown"