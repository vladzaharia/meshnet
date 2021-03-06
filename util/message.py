from constants.headers import FORMAT_UTF8
from util.headers import Headers

class Message:
    headers: Headers
    content: bytes

    def __init__(self, headers = Headers(), content: bytes = b'') -> None:
        self.headers = headers
        self.content = content

    @classmethod
    def from_utf8(self, headers = Headers(), content: str = ""):
        content_as_bytes = bytes(content, "utf-8")
        headers.frmt = FORMAT_UTF8
        return self(headers, content_as_bytes)

    @classmethod
    def from_bytearray(self, message: bytearray):
        headers = Headers().from_bytearray(message[0:16])
        content = message[16:]
        return self(headers, content)

    def to_bytearray(self):
        message = bytearray(len(self.content) + 16)
        message[0:15] = self.headers.to_bytearray()
        message[16:] = self.content
        return message