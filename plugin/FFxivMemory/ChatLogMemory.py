from typing import Tuple

from .MemoryHandler import MemoryHandler

ChatLog_pattern = b'\x48\x8b\xda\x49\x8b\xf8\x41\x8b\xd1\x48\x8b\xf1.....\x48\x8d\x05'


class ChatLogMemory(object):
    def __init__(self, handler: MemoryHandler):
        self.handler = handler
        self.base_addr = 0
        self.check_update_ptr = 0
        self.lengths_ptr = 0
        self.count_ptr = 0
        self.page_ptr = 0
        self.least_length_ptr = 0
        self.data_ptr = 0
        self.rescan_addr()

    def rescan_addr(self):
        addr = self.handler.scan_pointer_by_pattern(ChatLog_pattern, len(ChatLog_pattern) + 4)
        try:
            self.base_addr = self.handler.scan_vTable(addr)
        except Exception:
            raise Exception("cannot scan chat log vTable")
        self.count_ptr = self.base_addr + (5 * 4)
        self.page_ptr = self.base_addr + (6 * 4)
        self.check_update_ptr = self.base_addr + (5 * 8)
        self.lengths_ptr = self.base_addr + (9 * 8)
        self.least_length_ptr = self.base_addr + (10 * 8)
        self.data_ptr = self.base_addr + (12 * 8)

    def get_update_sign(self):
        return self.handler.read_ulonglong(self.check_update_ptr)

    def get_lengths_addr(self):
        return self.handler.read_ulonglong(self.lengths_ptr)

    def get_data_addr(self):
        return self.handler.read_ulonglong(self.data_ptr)

    def count(self):
        """the message loaded"""
        return self.handler.read_ulong(self.count_ptr)
        # return (self.handler.read_ulonglong(self.least_length_ptr) - self.get_lengths_addr()) // 4

    def __getitem__(self, idx: int) -> Tuple[int, int, str, str]:
        """
        note that here only store the message LOAD, if you clear the chat message, you cant access it
        :param int idx: index of the chat log to get, can be negative to get from the end
        :returns:
            - int timestamp : unix timestamp of the chat log
            - int channel_id : channel_id of the chat log
            - str player : name of the seder if exist
            - str message : the content of the message
        """
        count = self.count()
        if idx < 0:
            idx = count + idx
        if not max(-1, count - 1000) < idx < count:
            raise IndexError('list index %s out of range' % idx)
        idx %= 1000
        lengths_addr = self.get_lengths_addr()
        start = self.handler.read_uint(lengths_addr + (idx - 1) * 4) if idx > 0 else 0
        # print(start, self.handler.read_ulong(self.get_lengths_addr() + idx * 4))
        raw_data = self.handler.read_bytes(self.get_data_addr() + start, self.handler.read_ulong(lengths_addr + idx * 4) - start)
        time = int.from_bytes(raw_data[0:4], byteorder='little')
        channel_id = int.from_bytes(raw_data[4:8], byteorder='little')
        raw_text = bytearray()
        idx2 = 9
        while idx2 < len(raw_data):
            if raw_data[idx2] == 2:
                if idx2 + 2 >= len(raw_data): break
                if raw_data[idx2 + 2] < 240: idx2 += raw_data[idx2 + 2] + 2
            else:
                raw_text.append(raw_data[idx2])
            idx2 += 1
        player, message = raw_text.decode('utf-8', errors='ignore').split('\u001f', 1)
        return time, channel_id, player, message
