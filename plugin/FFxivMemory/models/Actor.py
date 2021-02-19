from .MemoryParseObject import get_memory_lazy_class, get_memory_class,get_memory_array
Effect= get_memory_class({
    'buffId': ('ushort', 0),
    'param': ('ushort', 2),
    'timer': ('float', 4),
    'actorId': ('uint', 8),
})

Effects=get_memory_array(Effect,12,19)

Position = get_memory_class({
    'x': ('float', 0),
    'y': ('float', 4),
    'z': ('float', 8),
})

Actor = get_memory_lazy_class({
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
    'pos': (Position, 160),
    'heading': ('float', 176),
    'pcTargetId': ('uint', 496),
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
})
