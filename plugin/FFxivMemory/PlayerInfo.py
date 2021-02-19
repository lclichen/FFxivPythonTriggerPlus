from .MemoryHandler import MemoryHandler
from .models.Player import Player

gauge_pattern = b"\x48\x8D.....\xE8....\x80\xBE\x13\x07.."
player_pattern = b"\x0F\x10.....\x40\x0F..\x0F\x95"


class PlayerInfo(Player):
    def __init__(self, handler: MemoryHandler):
        self.gauge_addr = handler.scan_pointer_by_pattern(gauge_pattern, 7) + 0x10
        self.player_addr =handler.scan_pointer_by_pattern(player_pattern, 7) - 0x11
        super(PlayerInfo, self).__init__(handler,self.player_addr)

