from FFxivPythonTrigger import PluginBase
from asyncio import sleep
import traceback
import logging

command = "@reset_combo"


class AutoComboBase(PluginBase):
    log_combo_action_id = False

    def get_me(self):
        return self.FPT.api.FFxivMemory.actorTable[0]

    def plugin_onload(self):
        self.comboState = self.FPT.api.FFxivMemory.combatData.comboState
        self.work = False
        self.keyTemp = {i: {j: None for j in range(12)} for i in range(10)}
        self.prev_combo_action_id = None
        self.FPT.api.command.register(command, self.process_command)

    def plugin_onunload(self):
        self.work = False
        self.FPT.api.command.unregister(command)

    def process_command(self, args):
        self.keyTemp = {i: {j: None for j in range(12)} for i in range(10)}

    def change_skill(self, row, block, name, *cases):
        lv = self.get_me().level
        for case in cases:
            if case[0] > lv:
                name = case[1]
            else:
                break
        if self.keyTemp and self.keyTemp[row][block] != name:
            self.keyTemp[row][block] = name
            self.FPT.api.Magic.macro_command("/hotbar set %s %s %s" % (name, row, block))

    async def plugin_start(self):
        self.work = True
        player_info = self.FPT.api.FFxivMemory.playerInfo
        while self.work:
            try:
                if self.log_combo_action_id and self.comboState.actionId != self.prev_combo_action_id:
                    self.prev_combo_action_id = self.comboState.actionId
                    self.FPT.log('new combo action %s' % self.prev_combo_action_id, logging.DEBUG)
                if player_info.job in self.combos and self.get_me() is not None:
                    self.combos[player_info.job](self)
            except:
                traceback.print_exc()
            await sleep(0.1)

    combos = dict()
