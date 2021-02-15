class Headers:
    message_type: bytes
    network: bytes
    priority: bytes
    frmt: bytes
    sender: bytes
    mrh: bytes
    recipient: bytes

    def __init__(self, 
        message_type: bytes = b'', 
        network: bytes = b'', 
        priority: bytes = b'', 
        frmt: bytes = b'', 
        sender: bytes = b'\x00\x00\x00', 
        mrh: bytes = b'\x00\x00\x00', 
        recipient: bytes = b'\x00\x00\x00'):
        self.message_type = message_type
        self.network = network
        self.priority = priority
        self.frmt = frmt
        self.sender = sender
        self.mrh = mrh
        self.recipient = recipient
    
    @classmethod
    def from_bytearray(self, raw: bytearray):
        return self(raw[0:1], raw[1:2], raw[2:3], raw[3:4], raw[7:10], raw[10:13], raw[13:16])

    def create(self):
        header = bytearray(16)

        # Set routing fields
        header[0:0] = self.message_type
        header[1:1] = self.network
        header[2:2] = self.priority
        header[3:3] = self.frmt

        # 4 5 6 = reserved

        # Set sender, mrh, recipient
        header[7:9] = self.sender
        header[10:12] = self.mrh
        header[13:15] = self.recipient

        return header