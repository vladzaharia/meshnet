from constants.nodetype import (
    TYPE_GATEWAY, 
    TYPE_GATEWAY_TIME, 
    TYPE_NODE, 
    TYPE_NODE_NR, 
    TYPE_PROVISIONING
)

class NodeType:
    node_type: bytes

    def __init__(self, node_type: bytes) -> None:
        self.node_type = node_type

    def is_node(self):
        return self.node_type == TYPE_NODE or self.node_type == TYPE_NODE_NR
    
    def is_non_routed(self):
        return self.node_type == TYPE_NODE_NR or self.node_type == TYPE_PROVISIONING

    def is_gateway(self):
        return self.node_type == TYPE_GATEWAY or self.node_type == TYPE_GATEWAY_TIME

    def is_auth_time_source(self):
        return self.node_type == TYPE_GATEWAY_TIME

    def to_string(self):
        if (self.node_type == TYPE_NODE):
            return "Node"
        if (self.node_type == TYPE_NODE_NR):
            return "Node - Non-Routing"
        elif (self.node_type == TYPE_GATEWAY):
            return "Gateway"
        elif (self.node_type == TYPE_GATEWAY_TIME):
            return "Gateway w/ Auth Time Source"
        elif (self.node_type == TYPE_PROVISIONING):
            return "SPECIAL - Provisioning"
        else:
            return "Unknown"