from constants.nodetype import TYPE_NODE
from constants.headers import PRIORITY_HIGH, PRIORITY_LOW, PRIORITY_REGULAR, PRIORITY_URGENT
from datetime import date, datetime, timedelta

from meshnet.routing import Routing
from meshnet.self import Self
from util.headers import Headers
from util.message import Message

class MessageQueueEntry:
    last_run: datetime
    next_scheduled_time: datetime
    timediff: timedelta
    expiry: datetime
    message: Message
    single_hop: bool

    def __init__(self, message: Message) -> None:
        self.message: Message = message
        self.last_run = None
        headers: Headers = message.headers

        if (headers.priority == PRIORITY_URGENT):
            self.timediff = timedelta(minutes = 5) if Self().node_type.is_node() else timedelta(minutes = 15)
            self.next_scheduled_time = datetime.now() + self.timediff
            self.expiry = datetime.now() + (timedelta(hours = 1) if Self().node_type.is_node() else timedelta(hours = 6))
            self.single_hop = False
        elif (headers.priority == PRIORITY_HIGH):
            self.timediff = timedelta(minutes = 15) if Self().node_type.is_node() else timedelta(minutes = 15)
            self.next_scheduled_time = datetime.now() + self.timediff
            self.expiry = datetime.now() + (timedelta(minutes = 30) if Self().node_type.is_node() else timedelta(hours = 1))
            self.single_hop = False
        elif (headers.priority == PRIORITY_REGULAR):
            self.timediff = timedelta(minutes = 5) if Self().node_type.is_node() else timedelta(minutes = 15)
            self.next_scheduled_time = datetime.now() + self.timediff
            self.expiry = datetime.now() + (timedelta(minutes = 10) if Self().node_type.is_node() else timedelta(hours = 1))
            self.single_hop = False
        elif (headers.priority == PRIORITY_LOW):
            self.timediff = timedelta(minutes = 5) if Self().node_type.is_node() else timedelta(minutes = 15)
            self.next_scheduled_time = datetime.now() + self.timediff
            self.expiry = datetime.now() + (timedelta(minutes = 5) if Self().node_type.is_node() else timedelta(minutes = 15))
            self.single_hop = True

    def process(self):
        if (self.single_hop):
            routing = Routing()
            filtered_list = list(filter(lambda r: r.node_id == self.message.headers.recipient, routing.neighbors))

            if (len(filtered_list) > 0):
                self.message.headers.mrh = Self().node_id
                self.update_schedule()
                # TODO: #1 Send message via LoRa
        else:
            self.update_schedule()
            # TODO: #1 Send message via LoRa

        

    def should_run(self):
        return self.next_scheduled_time < datetime.now()

    def should_expire(self):
        return self.expiry < datetime.now()

    def update_schedule(self):
        self.last_run = datetime.now()
        self.next_scheduled_time = datetime.now() + self.timediff

class MessageQueue:
    # Singleton instance
    _instance = None

    queue_entries: list[MessageQueueEntry]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MessageQueue, cls).__new__(cls)
            cls.queue_entries = list()
        return cls._instance

    def add(self, message: Message):
        self.queue_entries.append(MessageQueueEntry(message))
    
    def process(self):
        self._process_schedule()
        self._process_expiry()

    def _process_schedule(self):
        # Process entries which need to be processed
        for mqe in self.queue_entries:
            if (mqe.should_run()):
                mqe.process()
        
    def _process_expiry(self):
        mqes_to_remove: list[MessageQueueEntry] = list()

        # Collect entries to remove
        for mqe in self.queue_entries:
            if (mqe.should_expire()):
                mqes_to_remove.append(mqe)
        
        # Actually remove them
        for mqe in mqes_to_remove:
            self.queue_entries.remove(mqe)

    def reset(self):
        self.queue_entries = list()