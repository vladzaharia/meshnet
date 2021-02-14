def create(message_type: bytes, 
            network: bytes, 
            priority: bytes,
            format: bytes,
            sender: bytes,
            mrh: bytes,
            recipient: bytes):
    header = bytearray(16)

    # Set routing fields
    header[0:0] = message_type
    header[1:1] = network
    header[2:2] = priority
    header[3:3] = format

    # 4 5 6 = reserved

    # Set sender, mrh, recipient
    header[7:9] = sender
    header[10:12] = mrh
    header[13:15] = recipient

    return header

def message_type(header: bytearray):
    return bytes(header[0:1])
    
def network(header: bytearray):
    return bytes(header[1:2])
    
def priority(header: bytearray):
    return bytes(header[2:3])
    
def frmt(header: bytearray):
    return bytes(header[3:4])

def sender(header: bytearray):
    return bytes(header[7:10])

def mrh(header: bytearray):
    return bytes(header[10:13])

def recipient(header: bytearray):
    return bytes(header[13:16])