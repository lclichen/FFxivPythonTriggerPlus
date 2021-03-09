import logging
import clr
from os import path
from FFxivPythonTrigger import PluginBase

res = path.join(path.dirname(path.realpath(__file__)), 'LogHook')
clr.AddReference(res)
from LogHook import LogHook as lh
import System


class LogHookFix(PluginBase):
    name = "log hook fix"

    def HookCallback(self, addr):
        new_addr= addr - 72
        if self.FPT.api.FFxivMemory.chatLog.base_addr !=new_addr:
            self.FPT.log("fix log base address to %s"%hex(new_addr), logging.DEBUG)
            self.FPT.api.FFxivMemory.chatLog.rebase_addr(new_addr)

    def plugin_onload(self):
        mh = self.FPT.api.MemoryHandler
        addr = mh.get_address_by_offset(0x1140D70)
        if addr is None:
            self.FPT.log("address not found", logging.ERROR)
            return
        self.FPT.log("address found at %s" % hex(addr))
        self.hook = lh(addr)
        self.hook.callback = getattr(System,"Action`1")[System.Int64](self.HookCallback)

    def plugin_onunload(self):
        self.hook.Dispose()

