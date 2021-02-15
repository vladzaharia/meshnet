from datetime import datetime, timedelta

from constants.nodes import TYPE_GATEWAY, TYPE_NODE, TYPE_NON_ROUTING

TIMEOUT_NODE = 5
TIMEOUT_GATEWAY = 15

class RoutingEntry:
    node_id: bytes
    node_type: bytes
    expiry: datetime

    def __init__(self, node_id, node_type) -> None:
        self.node_id = node_id
        self.node_type = node_type

        if (node_type == TYPE_NON_ROUTING):
            raise Exception("Cannot create RoutingEntry for non-routing node")
        elif (node_type == TYPE_NODE):
            self.expiry = datetime.now() + timedelta(minutes = TIMEOUT_NODE)
        elif (node_type == TYPE_GATEWAY):
            self.expiry = datetime.now() + timedelta(minutes = TIMEOUT_GATEWAY)

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
        return filter(lambda n: n.node_type == TYPE_NODE, self.neighbors)

    def node_gateways(self):
        return filter(lambda n: n.node_type == TYPE_GATEWAY, self.neighbors)
    
    def clean(self):
        neighbors_to_clean = list()

        for neighbor in self.neighbors:
            if (neighbor.expiry < datetime.now()):
                neighbors_to_clean.append(neighbor)
        
        for neighbor in neighbors_to_clean:
            self.neighbors.remove(neighbor)

    def clear(self):
        self.neighbors = list()
