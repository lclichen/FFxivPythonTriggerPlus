from .MemoryParseObject import get_memory_array, get_memory_class, get_memory_lazy_array, get_memory_lazy_class

PlayerGCDTime_offset = 0x1CB96E8
PlayerTargetModel_offset = 0x1D05160
SkillQueueMark1_offset = 0x1cb9138
IsInFight_offset = 0x1D5553A
CoolDownGroup_offset = 0x1CB9258

ComboState = get_memory_lazy_class({
    'duration': ('float', 0),
    'actionId': ('uint', 4),
}, 0.1)

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


CoolDownGroups = get_memory_lazy_array(CoolDownGroup, 0x14, 100)
