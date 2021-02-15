from constants.headers import ROUTING_PROVISIONING
from constants.nodetype import TYPE_NON_ROUTING
from util.nodetype import NodeType

class Self:
    # Singleton instance
    _instance = None

    node_id: bytes
    node_type: NodeType

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Self, cls).__new__(cls)
            
            cls.node_id = ROUTING_PROVISIONING
            cls.node_type = NodeType(TYPE_NON_ROUTING)
        return cls._instance