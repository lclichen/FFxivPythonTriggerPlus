from .MemoryParseObject import get_memory_class, get_memory_array, get_pointer
from enum import Enum
from time import perf_counter

Effect = get_memory_class({
    'buffId': ('ushort', 0),
    'param': ('ushort', 2),
    'timer': ('float', 4),
    'actorId': ('uint', 8),
})


class Effects(get_memory_array(Effect, 12, 19)):
    def get_dict(self):
        try:
            return {effect.buffId: effect for effect in self if effect.buffId}
        except:
            return dict()


Position = get_memory_class({
    'x': ('float', 0),
    'y': ('float', 4),
    'z': ('float', 8),
})


class ActorType(Enum):
    Null = 0
    Player = 1
    BattleNpc = 2
    EventNpc = 3
    Treasure = 4
    Aetheryte = 5
    GatheringPoint = 6
    EventObj = 7
    MountType = 8
    Companion = 9  # minion
    Retainer = 10
    Area = 11
    Housing = 12
    Cutscene = 13
    CardStand = 14


class Actor(get_memory_class({
    'name': ('string', 48),
    'id': ('uint', 116),
    'bNpcId1': ('uint', 120),
    'bNpcId2': ('uint', 128),
    'ownerId': ('uint', 132),
    'type': ('byte', 140),
    'subType': ('byte', 141),
    'isFriendly': ('byte', 142),
    'effectiveDistanceX': ('byte', 144),
    'playerTargetStatus': ('byte', 145),
    'effectiveDistanceY': ('byte', 146),
    'unitStatus1': ('byte', 148),
    'unitStatus2': ('uint', 260),
    'pos': (Position, 160),
    'heading': ('float', 176),
    'pcTargetId': ('uint', 496),
    'pcTargetId2': ('uint', 560),
    'npcTargetId': ('uint', 6136),
    'bNpcNameId': ('uint', 6248),
    'currentWorldID': ('ushort', 6276),
    'homeWorldID': ('ushort', 6278),
    'currentHP': ('uint', 6296),
    'maxHP': ('uint', 6300),
    'currentMP': ('uint', 6304),
    'maxMP': ('uint', 6308),
    'currentGP': ('ushort', 6314),
    'maxGP': ('ushort', 6314),
    'currentCP': ('ushort', 6318),
    'maxCP': ('ushort', 6320),
    'job': ('byte', 6362),
    'level': ('byte', 6364),
    'effects': (Effects, 6488),
}, clazy=True)):

    def get_effects(self):
        return {effect.buffId: effect for effect in self.effects if effect.buffId != 0}

    def can_select(self):
        a1 = self.unitStatus1
        a2 = self.unitStatus2
        return bool(a1 & 2 and a1 & 4 and ((a2 >> 11 & 1) <= 0 or a1 >= 128) and not a2 & 0xffffe7f7)


class ActorTable(get_memory_array(get_pointer(Actor), 8, 200, alazy=True, update_time=0.5)):
    def __init__(self, handler, base):
        super(ActorTable, self).__init__(handler, base)
        self.name_cache = dict()
        self.id_cache = dict()
        self.valid_cache = list()
        self.cache_last_update = -1
        self.refresh_all()

    def update_id_cache(self):
        self.id_cache.clear()
        for el in self.get_list():
            try:
                if el.get_actual_addr():
                    a = el.get_value()
                    self.id_cache[a.id] = a
            except:pass

    def update_name_cache(self):
        self.name_cache.clear()
        for el in self.get_list():
            if el.get_actual_addr():
               try:
                   a = el.get_value()
                   if a.name not in self.name_cache:
                       self.name_cache[a.name] = list()
                   self.name_cache[a.name].append(a)
               except:pass

    def refresh_all(self):
        self.cache_last_update = perf_counter()
        super(ActorTable, self).refresh_all()
        self.valid_cache = [el.get_value for el in self.get_list() if el.get_actual_addr()]
        self.update_name_cache()
        self.update_id_cache()

    def get_valid_list(self, force_update=False):
        if force_update or self.cache_last_update + self.auto_update_sec <= perf_counter():
            self.refresh_all()
        return self.valid_cache

    def get_me(self, force_update=False):
        temp = self[0]
        if temp is not None and force_update:
            temp.refresh_all()
        return temp.get_value()

    def get_by_name(self, name, force_update=False):
        if force_update or self.cache_last_update + self.auto_update_sec <= perf_counter():
            self.refresh_all()
        return self.name_cache[name] if name in self.name_cache else None

    def get_by_id(self, id, force_update=False):
        if force_update or self.cache_last_update + self.auto_update_sec <= perf_counter():
            self.refresh_all()
        return self.id_cache[id] if id in self.id_cache else None
