from constants.headers import (
    FORMAT_RAW, 
    FORMAT_UTF8
)
from util.headers import Headers

def create_raw(message_type: bytes, 
                network: bytes, 
                priority: bytes,
                sender: bytes,
                mrh: bytes,
                recipient: bytes,
                content: bytes):
    content_len = len(content)

    message = bytearray(content_len)
    message[0:15] = Headers(message_type, network, priority, FORMAT_RAW, sender, mrh, recipient).create()
    message[16:] = content

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

def headers(message: bytearray):
    headers_var = bytearray(16)
    headers_var[0:16] = message[0:16]
    return headers_var

def content(message: bytearray):
    content_len = len(message) - 16
    content_var = bytearray(content_len)
    content_var[0:content_len] = message[16:]
    return content_var