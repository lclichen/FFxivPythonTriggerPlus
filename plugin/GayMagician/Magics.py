from os import path
import clr
import sys
if getattr(sys, 'frozen', False):
    res = path.join('res','GayMagician','GayMagician')
else:
    res = path.join(path.dirname(path.realpath(__file__)),'res', 'GayMagician')
clr.AddReference(res)
from GayMagician import GayMagician

class Magics(object):
    def __init__(self, *argv):
        self.gm = GayMagician()
        self.load_game_process(*argv)

    def load_game_process(self,*argv):
        self.gm.LoadGameProcess(*argv)

    def detach(self):
        self.gm.Detach()

    def attach(self):
        self.gm.Attach()

    def macro_command(self, command: str):
        self.gm.DoTextCommand(command)

    def echo_msg(self, msg):
        self.macro_command('/e ' + str(msg))

    def get_excel_sheet(self, sheet_name):
        return self.gm.GetExcelSheet(sheet_name)

    def get_sheet_row(self, sheet, rowId: int):
        return self.gm.GetSheetRow(sheet, rowId)

    def use_item(self, item_id, is_hq=False, target=0xE0000000):
        self.gm.UseItem(item_id, is_hq, target)
