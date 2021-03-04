from .MemoryParseObject import get_memory_class

TargetPtr = get_memory_class({
    "currentPtr": ('ulonglong', 0x80),
    "mouseOverPtr": ('ulonglong', 0xD0),
    "focusPtr": ('ulonglong', 0xF8),
    "previousPtr": ('ulonglong', 0x110),
})
