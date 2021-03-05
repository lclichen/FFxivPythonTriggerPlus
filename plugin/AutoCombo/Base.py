from FFxivPythonTrigger import PluginBase
from time import sleep
import traceback
import logging

command = "@reset_combo"


class AutoComboBase(PluginBase):

    def get_me(self):
        return self.FPT.api.FFxivMemory.actorTable.get_me()

    def plugin_onload(self):
        self.comboState = self.FPT.api.FFxivMemory.combatData.comboState
        self.work = False
        self.keyTemp = {i: {j: None for j in range(12)} for i in range(10)}
        self.prev_combo_action_id = None
        self.FPT.api.command.register(command, self.process_command)
        self.action_sheet = self.FPT.api.Magic.get_excel_sheet('Action')
        self.name_cache = dict()

    def plugin_onunload(self):
        self.work = False
        self.FPT.api.command.unregister(command)

    def process_command(self, args):
        self.keyTemp = {i: {j: None for j in range(12)} for i in range(10)}

    def change_skill(self, row, block, name, *cases):
        try:
            lv = self.get_me().level
        except:
            return
        for case in cases:
            if case[0] > lv:
                name = case[1]
            else:
                break
        if name is None: return
        if type(name) == int:
            if name not in self.name_cache:
                self.name_cache[name] = self.FPT.api.Magic.get_sheet_row(self.action_sheet, name).Name
            name = self.name_cache[name]
        if self.keyTemp and self.keyTemp[row][block] != name:
            self.keyTemp[row][block] = name
            self.FPT.api.Magic.macro_command("/hotbar set \"%s\" %s %s" % (name, row, block))

    def plugin_start(self):
        self.work = True
        player_info = self.FPT.api.FFxivMemory.playerInfo
        count_error = 0
        while self.work:
            try:
                if player_info.job in self.combos and self.get_me() is not None:
                    self.combos[player_info.job](self)
            except:
                self.FPT.log("error occurred:\n"+traceback.format_exc(),logging.ERROR)
                count_error += 1
                if count_error >= 20:
                    self.FPT.log("end because too many error occurred",logging.ERROR)
                    break
            else:
                count_error = 0
            sleep(0.1)

    combos = dict()
