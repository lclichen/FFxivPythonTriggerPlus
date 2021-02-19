from .models import Combat, MemoryParseObject

combo_state_pattern = b"\xF3\x0F......\xF3\x0F...\xE8....\x48\x8B.\x48\x8B.\x0F\xB7"
PlayerGCDTime_offset = 0x1CB96E8
PlayerTargetModel_offset = 0x1D05160
SkillQueueMark1_offset = 0x1cb9138
IsInFight_offset = 0x1D5553A
CoolDownGroup_offset = 0x1CB9258


def get_combat_data(handler):
    combo_state_offset = handler.scan_pointer_by_pattern(combo_state_pattern, 8)-handler.process_base.lpBaseOfDll
    return MemoryParseObject.get_memory_lazy_class({
        'comboState':(Combat.ComboState,combo_state_offset),
        'gcd': (Combat.GcdData, PlayerGCDTime_offset),
        'playerTargetPtr': ('ulonglong', PlayerTargetModel_offset),
        'skillQueue': (Combat.SkillQueue, SkillQueueMark1_offset),
        'isInFight': ('byte', IsInFight_offset),
        'coolDownGroups': (Combat.CoolDownGroups, CoolDownGroup_offset),
    })(handler,handler.process_base.lpBaseOfDll)
