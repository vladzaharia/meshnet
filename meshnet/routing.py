from datetime import datetime, timedelta

from constants.nodetype import TYPE_NON_ROUTING
from util.nodetype import NodeType

TIMEOUT_NODE = 5
TIMEOUT_GATEWAY = 15

class RoutingEntry:
    node_id: bytes
    node_type: NodeType
    expiry: datetime

    def __init__(self, node_id: bytes, node_type: NodeType) -> None:
        self.node_id = node_id
        self.node_type = node_type
        if (node_type.node_type == TYPE_NON_ROUTING):
            raise Exception("Cannot create RoutingEntry for non-routing node")
        elif (self.node_type.is_node()):
            self.expiry = datetime.now() + timedelta(minutes = TIMEOUT_NODE)
        elif (self.node_type.is_gateway()):
            self.expiry = datetime.now() + timedelta(minutes = TIMEOUT_GATEWAY)
        else:
            self.expiry = datetime.now() + timedelta(seconds = 5)

class Routing:
    # Singleton instance
    _instance = None

    neighbors: list[RoutingEntry] = list[RoutingEntry]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Routing, cls).__new__(cls)
            cls.neighbors = list()
        return cls._instance

    def add(self, entry: RoutingEntry):
        self.neighbors.append(entry)
    
    def node_neighbors(self):
        return filter(lambda n: n.node_type.is_node(), self.neighbors)

    def node_gateways(self):
        return filter(lambda n: n.node_type.is_gateway(), self.neighbors)
    
    def clean(self):
        neighbors_to_clean = list()

        for neighbor in self.neighbors:
            if (neighbor.expiry < datetime.now()):
                neighbors_to_clean.append(neighbor)
        
        for neighbor in neighbors_to_clean:
            self.neighbors.remove(neighbor)

    def reset(self):
        self.neighbors = list()
