from constants.nodetype import TYPE_NODE
from constants.headers import PRIORITY_HIGH, PRIORITY_LOW, PRIORITY_REGULAR, PRIORITY_URGENT
from datetime import datetime, timedelta

from meshnet.self import Self
from util.headers import Headers
from util.message import Message

class MessageQueueEntry:
    next_scheduled_time: datetime
    timediff: timedelta
    expiry: datetime
    message: Message
    single_hop: bool

    def __init__(self, message: Message) -> None:
        self.message: Message = message
        headers: Headers = message.headers

        if (headers.priority == PRIORITY_URGENT):
            self.timediff = timedelta(minutes = 5) if Self().node_type.is_node() else timedelta(minutes = 15)
            self.next_scheduled_time = datetime.now + self.timediff
            self.expiry = datetime.now() + (timedelta(hours = 1) if Self().node_type.is_node() else timedelta(hours = 6))
            self.single_hop = False
        elif (headers.priority == PRIORITY_HIGH):
            self.timediff = timedelta(minutes = 15) if Self().node_type.is_node() else timedelta(minutes = 15)
            self.next_scheduled_time = datetime.now + self.timediff
            self.expiry = datetime.now() + (timedelta(minutes = 30) if Self().node_type.is_node() else timedelta(hours = 1))
            self.single_hop = False
        elif (headers.priority == PRIORITY_REGULAR):
            self.timediff = timedelta(seconds = 5) if Self().node_type.is_node() else timedelta(minutes = 15)
            self.next_scheduled_time = datetime.now + self.timediff
            self.expiry = datetime.now() + (timedelta(minutes = 1) if Self().node_type.is_node() else timedelta(hours = 1))
            self.single_hop = False
        elif (headers.priority == PRIORITY_LOW):
            self.timediff = timedelta(minutes = 1) if Self().node_type.is_node() else timedelta(seconds = 5)
            self.next_scheduled_time = datetime.now + self.timediff
            self.expiry = datetime.now() + (timedelta(seconds = 5) if Self().node_type.is_node() else timedelta(seconds = 6))
            self.single_hop = True

    def process(self):
        # TODO: #1 Send message via LoRa
        self.next_scheduled_time = datetime.now() + self.timediff

class MessageQueue:
    queue_entries: list[MessageQueueEntry]

    def __init__(self) -> None:
        self.queue_entries = list()

    def add(self, message: Message):
        self.queue_entries.append(MessageQueueEntry(message))
    
    def process(self):
        self._process_schedule()
        self._process_expiry()

    def _process_schedule(self):
        # Process entries which need to be processed
        for mqe in self.queue_entries:
            if (mqe.next_scheduled_time < datetime.now()):
                mqe.process()
    
    def _process_expiry(self):
        mqes_to_remove: list[MessageQueueEntry] = list()

        # Collect entries to remove
        for mqe in self.queue_entries:
            if (mqe.expiry < datetime.now()):
                mqes_to_remove.append(mqe)
        
        # Actually remove them
        for mqe in mqes_to_remove:
            self.queue_entries.remove(mqe)