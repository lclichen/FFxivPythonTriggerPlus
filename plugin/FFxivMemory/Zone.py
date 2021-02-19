pattern = b"\x0F\xB7.....\x48\x8D...\xF3\x0F..\x33\xD2"


class Zone(object):
    def __init__(self, handler):
        self.handler=handler
        self.addr=handler.scan_pointer_by_pattern(pattern,7)

    @property
    def id(self):
        return self.handler.read_uint(self.addr)
