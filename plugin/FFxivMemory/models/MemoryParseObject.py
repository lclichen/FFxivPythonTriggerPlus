#from ..MemoryHandler import MemoryHandler
from time import time

auto_update_sec = 0.5


class Base(object):
    vals = dict()
    auto_update_sec = auto_update_sec

    def __init__(self, handler, base: int):
        self.handler = handler
        self.base = base
        self.cache = dict()
        self.last_update = dict()

    def need_update(self, key):
        return self.last_update[key] + self.auto_update_sec < time()

    def __getattr__(self, key):
        return self[key]

    def __getitem__(self, key, force_update=False):
        if key not in self.vals:
            raise IndexError('%s is not a valid key' % key)
        return self.refresh(key) if force_update or self.need_update(key) else self.cache[key]

    def refresh(self, key):
        if type(self.vals[key][0]) == str:
            if self.vals[key][0] == 'bytes':
                self.cache[key] = self.handler.read_bytes(self.base + self.vals[key][2], self.vals[key][1])
            else:
                self.cache[key] = getattr(self.handler, 'read_' + self.vals[key][0])(self.base + self.vals[key][1])
        else:
            self.cache[key] = self.vals[key][0](self.handler, self.base + self.vals[key][1])
        self.last_update[key] = time()
        return self.cache[key]

    def __setitem__(self, key, value):
        if key not in self.vals:
            raise IndexError('%s is not a valid key' % key)
        if type(self.vals[key][0]) == str:
            if self.vals[key][0] == 'bytes':
                self.handler.write_bytes(self.base + self.vals[key][2], value, self.vals[key][1])
            else:
                getattr(self.handler, 'write_' + self.vals[key][0])(self.base + self.vals[key][1], value)
        else:
            self.cache[key].replace(value)
        self.refresh(key)

    def replace(self, value):
        for key in self.vals:
            self[key] = value[key]

    def get_dict(self):
        return {k: self[k] for k in self.vals.keys()}

    def __str__(self):
        return str(self.get_dict())


class MemoryObject(Base):
    def __init__(self, handler, base: int):
        super(MemoryObject, self).__init__(handler, base)
        for key in self.vals:
            self.refresh(key)


class MemoryLazyObject(Base):
    def __getitem__(self, key, force_update=False):
        if key not in self.vals:
            raise IndexError('%s is not a valid key' % key)
        return self.refresh(key) if key not in self.cache or self.need_update(key) or force_update else self.cache[key]


def get_memory_class(vals_data: dict, refresh_time=auto_update_sec):
    class TempClass(MemoryObject):
        vals = vals_data
        auto_update_sec = refresh_time

    return TempClass


def get_memory_lazy_class(vals_data: dict, refresh_time=auto_update_sec):
    class TempClass(MemoryLazyObject):
        vals = vals_data
        auto_update_sec = refresh_time

    return TempClass


class MemoryArrayLazy(object):
    Length = 0
    ValType = None
    ValLen = 0
    auto_update_sec = auto_update_sec

    def __init__(self, handler, base: int):
        self.handler = handler
        self.base = base
        self.cache = dict()
        self.last_update = dict()
        for i in range(self.Length): self.refresh(i)

    def need_update(self, key):
        return key not in self.last_update or self.last_update[key] + self.auto_update_sec < time()

    def refresh(self, key: int):
        if type(self.ValType) == str:
            self.cache[key] = getattr(self.handler, 'read_' + self.ValType)(self.base + (self.ValLen * key))
        else:
            self.cache[key] = self.ValType(self.handler, self.base + (self.ValLen * key))
        self.last_update[key] = time()
        return self.cache[key]

    def __getitem__(self, key: int, force_update=False):
        return self.refresh(key) if force_update or self.need_update(key) else self.cache[key]

    def __setitem__(self, key, value):
        if type(self.ValType) == str:
            getattr(self.handler, 'write_' + self.ValType)(self.base + (self.ValLen * key), value)
        else:
            self.cache[key].replace(value)

    def replace(self, value):
        for i in range(self.Length):
            self.cache[i] = value[i]

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        self.i += 1
        if self.i > self.Length: raise StopIteration
        return self.cache[self.i - 1]

    def index_by(self, key):
        temp = dict()
        for el in self:
            if el[key] not in temp:
                temp[el[key]] = list()
            temp[el[key]].append(el)
        return temp

    def get_list(self):
        return [self[i] for i in range(self.Length)]

    def __str__(self):
        return str(self.get_list())

    def __contains__(self, item):
        for el in self:
            if item == el:
                return True
        return False


class MemoryArray(MemoryArrayLazy):
    def __init__(self, handler, base: int):
        super(MemoryArray, self).__init__(handler, base)
        for i in range(self.Length): self.refresh(i)


class Pointer(object):
    auto_update_sec = auto_update_sec
    ValType = None

    def __init__(self, handler, base: int):
        self.handler = handler
        self.base = base
        self._value = None
        self.last_update = -1

    def need_update(self):
        return self.last_update + self.auto_update_sec < time()

    def refresh(self):
        addr = self.handler.read_ulonglong(self._value)
        if type(self.ValType) == str:
            self._value = getattr(self.handler, 'read_' + self.ValType)(addr)
        else:
            self._value = self.ValType(self.handler, addr)
        self.last_update = time()
        return self._value

    def get_value(self, force_update=False):
        return self.refresh() if force_update or self.need_update() else self._value

    def replace(self, value):
        addr = self.handler.read_ulonglong(self._value)
        if type(self.ValType) == str:
            self._value = getattr(self.handler, 'write_' + self.ValType)(addr, value)
        else:
            self._value = self.get_value().replace(value)


def get_memory_array(val_type, val_len, count, update_time=0.5):
    class TempClass(MemoryArray):
        auto_update_sec = update_time
        ValType = val_type
        ValLen = val_len
        Length = count

    return TempClass


def get_memory_lazy_array(val_type, val_len, count, update_time=0.5):
    class TempClass(MemoryArrayLazy):
        auto_update_sec = update_time
        ValType = val_type
        ValLen = val_len
        Length = count

    return TempClass

def get_pointer(val_type, update_time=0.5):
    class TempClass(Pointer):
        ValType = val_type
        auto_update_sec = update_time

    return TempClass
