from FFxivPythonTrigger import PluginBase
from.Magics import Magics

"""
Provide some magics Api
api:    Magic
            macro_command(command:str)
            echo_msg(msg:str)
            get_excel_sheet(sheet_name:str)
            get_sheet_row(self, sheet, rowId: int)
"""

class GayMagicianPlugin(PluginBase):
    name = "Gay Magician"

    def plugin_onload(self):
        self.magic= Magics(self.FPT.api.MemoryHandler.process_id)
        self.FPT.register_api('Magic', self.magic)
        self.magic.echo_msg('GayMagician loaded')

    def plugin_onunload(self):
        self.magic.detach()
