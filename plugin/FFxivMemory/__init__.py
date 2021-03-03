from .MemoryHandler import MemoryHandler
from .ChatLogProcess import ChatLogProcess
from .ActorTable import get_actor_table
from .PlayerInfo import PlayerInfo
from .CombatData import get_combat_data
from .TargetManager import get_target_manager
from FFxivPythonTrigger import PluginBase
from .Zone import Zone
from .ChatLogMemory import ChatLogMemory
import asyncio

"""
provide memory access for FFxiv
api:    FFxivMemory (for more details, see scripts under ./models)
            chatLog
            actorTable
            playInfo
            combatData
            targetManager
            zone

api:    MemoryHandler
            read_xxx(addr:int)
            write_xxx(addr:int,value:any)
            ida_sig_to_pattern(ida_sig:str)
            pattern_scan_main_module(pattern:bytes)
            read_pointer_shift(base_addr:int,*shifts:int)
            scan_pointer_by_pattern(self, pattern: bytes, cmd_len: int, ptr_idx: int = None)
"""

class FFxivMemory(PluginBase):
    name = "FFxiv Memory Plugin"

    def plugin_onload(self):
        self.handler = MemoryHandler()
        self.chatLog = ChatLogMemory(self.handler)
        self.actorTable = get_actor_table(self.handler)
        self.playerInfo = PlayerInfo(self.handler)
        self.combatData = get_combat_data(self.handler)
        self.zone = Zone(self.handler)
        self.chatLogProcess = ChatLogProcess(self.chatLog)
        self.targetManager = get_target_manager(self.handler)
        self.work = False

        # self.FPT.register_event("log_event", print)
        class FFxivMemoryApi(object):
            chatLog = self.chatLog
            actorTable = self.actorTable
            playerInfo = self.playerInfo
            combatData = self.combatData
            targetManager = self.targetManager
            zone = self.zone

        self.FPT.register_api('MemoryHandler', self.handler)
        self.FPT.register_api('FFxivMemory', FFxivMemoryApi())

    def plugin_onunload(self):
        self.work = False

    async def plugin_start(self):
        self.work = True
        while self.work:
            events = list()
            events += self.chatLogProcess.check_update()
            for event in events:
                self.FPT.process_event(event)
            await asyncio.sleep(0.1)
