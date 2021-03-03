from time import perf_counter
import traceback

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

    def need_update(self, key):
        try:
            return self.last_update[key] + self.auto_update_sec < perf_counter()
        except:
            return True

    def get(self, key, force_update=False):
        if key not in self.vals:
            raise IndexError('{} is not a valid key'.format(key))
        return self.refresh(key) if force_update or self.need_update(key) else self.cache[key]

    def __getitem__(self, key):
        return self.get(key)

    def __getattr__(self, key):
        return self.get(key)

    def refresh(self, key):
        self.last_update[key] = perf_counter()
        row = self.vals[key]
        if type(row[0]) == str:
            if row[0] == 'bytes':
                self.cache[key] = self.handler.read_bytes(self.base + row[2], row[1])
            else:
                self.cache[key] = getattr(self.handler, 'read_' + row[0])(self.base + row[1])
        else:
            if key in self.cache and self.cache[key] is not None:
                self.cache[key].refresh_all()
            else:
                self.cache[key] = row[0](self.handler, self.base + row[1])
        return self.cache[key]

    def refresh_all(self):
        for key in self.vals.keys():
            self.refresh(key)

    def get_dict(self):
        return {k: self[k] for k in self.vals.keys()}

    def __str__(self):
        return str(self.get_dict())

    def __setitem__(self, key, value):
        if key not in self.vals:
            raise IndexError('%s is not a valid key' % key)
        row = self.vals[key]
        if type(row[0]) == str:
            if row[0] == 'bytes':
                self.handler.write_bytes(self.base + row[2], value, row[1])
            else:
                getattr(self.handler, 'write_' + row[0])(self.base + row[1], value)
        else:
            self.cache[key].replace(value)
        self.refresh(key)

    def replace(self, value):
        for key in self.value.keys():
            self[key] = value[key]


def get_memory_class(vals_data: dict, refresh_time=auto_update_sec, clazy=default_lazy):
    class TempClass(MemoryClass):
        vals = vals_data
        auto_update_sec = refresh_time
        lazy = clazy

    return TempClass


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
        try:
            return self.last_update[key] + self.auto_update_sec < perf_counter()
        except:
            return True

    def get(self, key: int, force_update=False):
        if key >= self.Length: raise IndexError('{} is Out of index'.format(key))
        return self.refresh(key) if force_update or self.need_update(key) else self.cache[key]

    def __getitem__(self, key: int):
        return self.get(key)

    def refresh(self, key: int):
        self.last_update[key] = perf_counter()
        if type(self.ValType) == str:
            self.cache[key] = getattr(self.handler, 'read_' + self.ValType)(self.base + (self.ValLen * key))
        else:
            try:
                if key in self.cache and self.cache[key] is not None:
                    self.cache[key].refresh_all()
                else:
                    self.cache[key] = self.ValType(self.handler, self.base + (self.ValLen * key))
            except:
                self.cache[key] = None
        return self.cache[key]

    def refresh_all(self):
        for i in range(self.Length): self.refresh(i)

    def get_list(self):
        return [self.get(i) for i in range(self.Length)]

    def __str__(self):
        return str(self.get_list())

    def __setitem__(self, key, value):
        if type(self.ValType) == str:
            getattr(self.handler, 'write_' + self.ValType)(self.base + (self.ValLen * key), value)
        else:
            self.cache[key].replace(value)

    def replace(self, value):
        if len(value) != self.Length:
            raise IndexError("Index out of bounds")
        for i in range(self.Length):
            self.cache[i] = value[i]

    def __iter__(self):
        return self.get_list().__iter__()

    def index_by(self, key):
        if type(self.ValType) == str:
            raise TypeError("%s type array not supported index" % self.ValType)
        temp = dict()
        for el in self.get_list():
            if el[key] not in temp: temp[el[key]] = list()
            temp[el[key]].append(el)
        return temp

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


class Pointer(object):
    auto_update_sec = auto_update_sec
    shifts = list()
    last_shift = 0
    ValType = None

    def __init__(self, handler, base: int):
        self.handler = handler
        self.base = base
        self._value = None
        self.last_update = -1

    def need_update(self):
        return self.last_update + self.auto_update_sec < perf_counter()

    def get_actual_addr(self):
        addr = self.handler.read_pointer_shift(self.base, *self.shifts)
        return addr + self.last_shift

    def refresh(self):
        self.last_update = perf_counter()
        try:
            addr = self.get_actual_addr()
            if type(self.ValType) == str:
                self._value = getattr(self.handler, 'read_' + self.ValType)(addr)
            else:
                if self._value is None:
                    self._value = self.ValType(self.handler, addr)
                else:
                    self._value.base = addr
                    self._value.refresh_all()
        except:
            self._value = None
        return self._value

    refresh_all = refresh

    def get_value(self, force_update=False):
        return self.refresh() if force_update or self.need_update() else self._value

    def replace(self, value):
        addr = self.get_actual_addr()
        if type(self.ValType) == str:
            self._value = getattr(self.handler, 'write_' + self.ValType)(addr, value)
        else:
            if self._value is None:
                self._value = self.ValType(self.handler, addr)
            self._value.base = addr
            self._value.replace(value)

    def __getattr__(self, key):
        return getattr(self.get_value(), key)

    def __getitem__(self, key):
        return self.get_value()[key]

    def __setitem__(self, key, value):
        self.get_value()[key] = value


def get_pointer(val_type, pShifts=None, lastShift=0, update_time=0.5):
    if pShifts is None:
        pShifts = [0]

    class TempClass(Pointer):
        ValType = val_type
        auto_update_sec = update_time
        shifts = pShifts
        last_shift = lastShift

    return TempClass
