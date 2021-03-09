from FFxivPythonTrigger import PluginBase
import json
import traceback


class Debug(PluginBase):
    name = "debug"

    def plugin_onload(self):
        self.work=False
    def plugin_onunload(self):
        self.work=False

    async def plugin_start(self):
        self.work=True
        try:
            while self.work:
                ans = []
                for enemy in self.FPT.api.FFxivMemory.combatData.enemies:
                    if enemy.id != 0xe0000000:
                        ans.append(self.FPT.api.FFxivMemory.actorTable.get_by_id(enemy.id).name)
                if ans: print(ans)
                await asyncio.sleep(1)
        except:
            traceback.print_exc()
