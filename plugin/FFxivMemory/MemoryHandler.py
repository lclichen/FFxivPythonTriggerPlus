import logging
import pymem
import struct
from .ValToBytes import long_to_bytes
from .models import MemoryParseObject

pymem.logger.setLevel(logging.ERROR)


def byte_to_sbyte(byte):
    return struct.unpack('b', struct.pack('<i', byte)[:1])[0]


def sbyte_to_byte(sbyte):
    return struct.unpack('B', struct.pack('<i', sbyte)[:1])[0]


class MemoryHandler(pymem.Pymem):
    def __init__(self, name: str = None, pid: int = None):
        if name and pid:
            raise Exception("Should not call by both name and pid")
        if name is not None:
            super().__init__(name)
        elif pid is not None:
            super().__init__()
            self.open_process_from_id(pid)
        else:
            super().__init__('ffxiv_dx11.exe')

        self.main_module = pymem.process.module_from_name(self.process_handle, "ffxiv_dx11.exe")

    def pattern_scan_main_module(self, pattern: bytes):
        """
        scan memory after a byte pattern for the main module and return its corresponding memory address

        :param bytes pattern: A regex byte pattern to search for
        :return: int Memory address of given pattern, or None if one was not found
        """
        return pymem.pattern.pattern_scan_module(self.process_handle, self.main_module, pattern)

    def scan_pointer_by_pattern(self, pattern: bytes, cmd_len: int, ptr_idx: int = None):
        """
        scan memory after a byte pattern for the main module and get the upper pointer

        :param bytes pattern: A regex byte pattern to search for
        :param int cmd_len: the length from start of pattern to the end of target address
        :return:  int Memory address of given pattern
        """
        ptr_idx = ptr_idx or cmd_len - 4
        temp = self.pattern_scan_main_module(pattern)
        if temp is None: return None
        return self.read_ulong(temp + ptr_idx) + temp + cmd_len

    def get_address_by_offset(self, offset: int):
        return offset + self.process_base.lpBaseOfDll

    def read_byte(self, addr: int):
        return self.read_bytes(addr, 1)[0]

    def write_byte(self, address, value):
        return self.write_bytes(address, bytes([value]), 1)

    def write_string(self, address, value):
        super(MemoryHandler, self).write_string(address, value)
        self.write_byte(address + len(value.encode()), 0)

    def read_pointer_shift(self, base, *shifts):
        ptr = base
        for shift in shifts:
            ptr = self.read_ulonglong(ptr) + shift
        return ptr

    def scan_vTable(self, signature: int):
        next_page = 0
        ans = None
        while ans is None:
            next_page, ans = pymem.pattern.scan_pattern_page(self.process_handle, next_page,
                                                             long_to_bytes(signature, True))
        return ans

    def read_sbyte(self, address: int):
        return byte_to_sbyte(self.read_byte(address))

    def write_sbyte(self, address: int, value: int):
        return self.write_byte(address, sbyte_to_byte(value))

    get_memory_array = staticmethod(MemoryParseObject.get_memory_array)
    get_memory_lazy_array = staticmethod(MemoryParseObject.get_memory_lazy_array)
    get_memory_class = staticmethod(MemoryParseObject.get_memory_class)
    get_memory_lazy_class = staticmethod(MemoryParseObject.get_memory_lazy_class)
