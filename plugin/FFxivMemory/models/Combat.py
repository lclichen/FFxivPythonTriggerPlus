from .MemoryParseObject import get_memory_array, get_memory_class
from time import perf_counter

ComboState = get_memory_class({
    'remain': ('float', 0),
    'actionId': ('uint', 4),
}, 0.1, clazy=True)

SkillQueue = get_memory_class({
    'mark1': ('ulong', 0),
    'mark2': ('ulong', 4),
    'abilityId': ('ulong', 8),
    'targetId': ('ulong', 16),
}, 0.1)


class GcdData(get_memory_class({
    'duration': ('float', 0),
    'total': ('float', 4),
}, 0.1)):
    @property
    def remain(self):
        return self.total - self.duration


class CoolDownGroup(get_memory_class({
    'duration': ('float', 8),
    'total': ('float', 12),
}, 0.1)):
    @property
    def remain(self):
        return self.total - self.duration


CoolDownGroups = get_memory_array(CoolDownGroup, 0x14, 100, alazy=True)

Enemy = get_memory_class({
    'id': ('uint', 0)
})


class Enemies(get_memory_array(Enemy, 4 * 5, 8, alazy=True)):
    def __init__(self, handler, base):
        super(Enemies, self).__init__(handler, base)
        self.valid_cache = None
        self.valid_last_update = None
        self.valid_update()

    def valid(self, force=False):
        return self.valid_update() if force or self.valid_cache is not None or self.valid_last_update + self.auto_update_sec < perf_counter() else self.valid_cache

    def valid_update(self):
        self.valid_cache = [enemy for enemy in self if enemy.id != 0xe0000000]
        self.valid_last_update = perf_counter()
        return self.valid_cache
