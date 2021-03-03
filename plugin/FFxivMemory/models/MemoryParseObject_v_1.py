# from ..MemoryHandler import MemoryHandler
from time import perf_counter

auto_update_sec = 0.1
default_lazy = True


class MemoryClass(object):
    vals = dict()
    auto_update_sec = auto_update_sec
    lazy = default_lazy

    def __init__(self, handler, base: int):
        self.handler = handler
        self.base = base
        self.cache = dict()
        self.last_update = dict()
        if not self.lazy:
            self.refresh_all()

    def need_update(self, key):
        try:
            return self.last_update[key] + self.auto_update_sec < perf_counter()
        except:
            return True

    def __getattr__(self, key):
        return self[key]

    def __getitem__(self, key, force_update=False):
        if key not in self.vals:
            raise IndexError('{} is not a valid key'.format(key))
        return self.refresh(key) if force_update or self.need_update(key) else self.cache[key]

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

    def refresh(self, key):
        if type(self.vals[key][0]) == str:
            if self.vals[key][0] == 'bytes':
                self.cache[key] = self.handler.read_bytes(self.base + self.vals[key][2], self.vals[key][1])
            else:
                self.cache[key] = getattr(self.handler, 'read_' + self.vals[key][0])(self.base + self.vals[key][1])
        else:
            self.cache[key] = self.vals[key][0](self.handler, self.base + self.vals[key][1])
        self.last_update[key] = perf_counter()
        return self.cache[key]

    def refresh_all(self):
        for key in self.vals.keys():
            self.refresh(key)

    def replace(self, value):
        for key in self.vals:
            self[key] = value[key]

    def get_dict(self):
        return {k: self[k] for k in self.vals.keys()}

    def __str__(self):
        return str(self.get_dict())


def get_memory_class(vals_data: dict, refresh_time=auto_update_sec, clazy=default_lazy):
    class TempClass(MemoryClass):
        vals = vals_data
        auto_update_sec = refresh_time
        lazy = clazy

    return TempClass


# def get_memory_lazy_class(vals_data: dict, refresh_time=auto_update_sec):
#     class TempClass(MemoryClass):
#         vals = vals_data
#         auto_update_sec = refresh_time
#         lazy = True
#
#     return TempClass


class MemoryArray(object):
    Length = 0
    ValType = None
    ValLen = 0
    auto_update_sec = auto_update_sec
    lazy = default_lazy

    def __init__(self, handler, base: int):
        self.handler = handler
        self.base = base
        self.cache = dict()
        self.last_update = dict()
        if not self.lazy:
            self.refresh_all()

    def need_update(self, key):
        return key not in self.last_update or self.last_update[key] + self.auto_update_sec < perf_counter()

    def refresh(self, key: int):
        if type(self.ValType) == str:
            self.cache[key] = getattr(self.handler, 'read_' + self.ValType)(self.base + (self.ValLen * key))
        else:
            self.cache[key] = self.ValType(self.handler, self.base + (self.ValLen * key))
        self.last_update[key] = perf_counter()
        return self.cache[key]

    def refresh_all(self):
        for i in range(self.Length): self.refresh(i)

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
        return self[self.i - 1]

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


def get_memory_array(val_type, val_len, count, update_time=auto_update_sec, alazy=default_lazy):
    class TempClass(MemoryArray):
        auto_update_sec = update_time
        ValType = val_type
        ValLen = val_len
        Length = count
        lazy = alazy

    return TempClass


# def get_memory_lazy_array(val_type, val_len, count, update_time=0.5):
#     class TempClass(MemoryArray):
#         auto_update_sec = update_time
#         ValType = val_type
#         ValLen = val_len
#         Length = count
#         lazy=True
#
#     return TempClass


class Pointer(object):
    auto_update_sec = auto_update_sec
    ValType = None

    def __init__(self, handler, base: int):
        self.handler = handler
        self.base = base
        self._value = None
        self.last_update = -1

    def need_update(self):
        return self.last_update + self.auto_update_sec < perf_counter()

    def refresh(self):
        addr = self.handler.read_ulonglong(self.base)
        if type(self.ValType) == str:
            self._value = getattr(self.handler, 'read_' + self.ValType)(addr)
        else:
            if self._value is None:
                self._value = self.ValType(self.handler, addr)
            else:
                self._value.base = addr
        self.last_update = perf_counter()
        return self._value

    refresh_all=refresh

    def get_value(self, force_update=False):
        return self.refresh() if force_update or self.need_update() else self._value

    def replace(self, value):
        addr = self.handler.read_ulonglong(self._value)
        if type(self.ValType) == str:
            self._value = getattr(self.handler, 'write_' + self.ValType)(addr, value)
        else:
            self._value = self.get_value().replace(value)


def get_pointer(val_type, update_time=0.5):
    class TempClass(Pointer):
        ValType = val_type
        auto_update_sec = update_time

    return TempClass
