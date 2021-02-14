from constants.headers import FORMAT_RAW, FORMAT_UTF8;

# ABCD ZZZ EEE FFF GGG H…
def create_raw(message_type: bytes, 
                network: bytes, 
                priority: bytes,
                sender: bytes,
                mrh: bytes,
                recipient: bytes,
                content: bytes):
    content_len = len(content)

    message = bytearray(content_len)
    message[0:15] = create_header(message_type, network, priority, FORMAT_RAW, sender, mrh, recipient)
    message[16:content_len-1] = content

    return message

def create_utf8(message_type: bytes, 
                network: bytes, 
                priority: bytes,
                sender: bytes,
                mrh: bytes,
                recipient: bytes,
                content: str):
    content_as_bytes = bytes(content, "utf-8")

    message = create_raw(message_type, network, priority, sender, mrh, recipient, content_as_bytes)
    message[3:3] = FORMAT_UTF8
    
    return message

def create_header(message_type: bytes, 
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
