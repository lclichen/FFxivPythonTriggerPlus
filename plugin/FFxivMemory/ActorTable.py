from .MemoryHandler import MemoryHandler
from .models.Actor import Actor
from .models.MemoryParseObject import get_memory_array,get_pointer
from time import time

pattern = b"\x48\x8D.....\xE8....\x48\x8B.\x48\x8B.\x48\x8D.....\xE8....\x48\x8D.....\xBA....\xE8....\x89\x2F"
auto_update_sec = 0.5
Length=200

class ActorTable(object):
    def __init__(self, handler: MemoryHandler):
        self.handler = handler
        self.addr = self.handler.scan_pointer_by_pattern(pattern, 7)
        self.cache = []
        self.name_dict = dict()
        self.id_dict = dict()
        self.last_update = -1
        self.update()

    def update(self):
        addr = self.addr
        self.cache.clear()
        for i in range(Length):
            temp = self.handler.read_ulonglong(addr)
            if self.handler.read_ulonglong(addr) != 0:
                self.cache.append(Actor(self.handler, temp))
            addr += 8
        self.name_dict = self.index_by('name')
        self.id_dict = self.index_by('id')
        self.last_update = time()

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        self.i += 1
        if self.i > len(self.cache): raise StopIteration
        return self.cache[self.i - 1]

    def index_by(self,key):
        temp=dict()
        for actor in self.cache:
            if actor[key] not in temp:
                temp[actor[key]] = list()
            temp[actor[key]].append(actor)
        return temp

    def __getitem__(self,key,force_update=False):
        if force_update or time() - auto_update_sec > self.last_update:
            self.update()
        if type(key) == int:
            if key > 1000:
                return self.id_dict[key][0] if key in self.id_dict else None
            else:
                return self.cache[key] if key < len(self) else None
        else:
            return self.name_dict[key] if key in self.name_dict else None

    def __len__(self):
        return len(self.cache)
