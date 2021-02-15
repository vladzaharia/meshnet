from constants.nodetype import TYPE_GATEWAY, TYPE_GATEWAY_TIME, TYPE_NODE, TYPE_NON_ROUTING

class NodeType:
    node_type: bytes

    def __init__(self, node_type: bytes) -> None:
        self.node_type = node_type

    def is_node(self):
        return self.node_type == TYPE_NODE
    
    def is_gateway(self):
        return self.node_type == TYPE_GATEWAY or self.node_type == TYPE_GATEWAY_TIME

    def is_auth_time_source(self):
        return self.node_type == TYPE_GATEWAY_TIME

    def to_string(self):
        if (self.node_type == TYPE_NODE):
            return "Node"
        elif (self.node_type == TYPE_GATEWAY):
            return "Gateway"
        elif (self.node_type == TYPE_GATEWAY_TIME):
            return "Gateway w/ Auth Time Source"
        elif (self.node_type == TYPE_NON_ROUTING):
            return "SPECIAL - Non-Routing Node"
        else:
            return "Unknown"