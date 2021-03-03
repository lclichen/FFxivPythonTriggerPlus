from .models import Combat, MemoryParseObject

# combo_state_pattern = b"\xF3\x0F......\xF3\x0F...\xE8....\x48\x8B.\x48\x8B.\x0F\xB7", 8
PlayerGCDTime_pattern = b"\x48\x8D.....\xE8....\x48\x8D.....\xE8....\x48\x8D.....\xE8....\xB9....\x48\x8D.....\x33\xD2", 48
PlayerTargetModel_pattern = b"\x48\x83\x3D.....\x75.\xC7\x43.....", 8, 3
SkillQueueMark1_pattern = b"\x44\x89\x2D....\xF3\x0F\x11\x05....", 7
IsInFight_pattern = b"\x80\x3D.....\x0F\x95\xC0\x48\x83\xC4.", 7, 2
CoolDownGroup_pattern = b"\x0F\xB7\x0D....\x84\xC0", 7
Enemies_Base_pattern = b"\x48\x8B\x0D....\x4C\x8B\xC0\x33\xD2", 7
Enemies_shifts = [0x30, 0x58, 0x98, 0x20, 0x20]


def get_combat_data(handler):
    _=handler.ida_sig_to_pattern
    scan=handler.scan_pointer_by_pattern
    combo_state_addr = scan(_("f3 0f ?? ?? ?? ?? ?? ?? f3 0f ?? ?? ?? e8 ?? ?? ?? ?? 48 8b ?? 48 8b ?? 0f b7"),8)
    PlayerGCDTime_addr = scan(*PlayerGCDTime_pattern) + 0x474
    PlayerTargetModel_addr = scan(*PlayerTargetModel_pattern)
    SkillQueueMark1_addr = scan(*SkillQueueMark1_pattern) + 4
    IsInFight_addr = scan(*IsInFight_pattern)
    CoolDownGroup_addr = scan(*CoolDownGroup_pattern) + 0x76
    Enemies_Base_addr= scan(*Enemies_Base_pattern)
    return MemoryParseObject.get_memory_class({
        'comboState': (Combat.ComboState, combo_state_addr),
        'gcd': (Combat.GcdData, PlayerGCDTime_addr),
        'playerTargetPtr': ('ulonglong', PlayerTargetModel_addr),
        'skillQueue': (Combat.SkillQueue, SkillQueueMark1_addr),
        'isInFight': ('byte', IsInFight_addr),
        'coolDownGroups': (Combat.CoolDownGroups, CoolDownGroup_addr),
        'enemies': (MemoryParseObject.get_pointer(Combat.Enemies,Enemies_shifts), Enemies_Base_addr),
        #'enemies': (Combat.Enemies, Enemies_addr),
    }, clazy=True)(handler, 0)
