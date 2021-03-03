from FFxivPythonTrigger import PluginBase
import logging

"""
change the zoom value to let you see more
command:    @zoom
format:     /e @zoom [func] [args]...
functions (*[arg] is optional args):
    [get]:      get current zoom value
    [set]:      set current zoom value
                format: /e @zoom set [value(float) / "default"]
"""

pattern = b"\x48\x8D\x1D....\x48\x8B\xCB\x41\x8D\x50\x02"
default = 20
command = '@zoom'


class ZoomPlugin(PluginBase):
    name = "zoom plugin"

    def plugin_onload(self):
        ptr=self.FPT.api.MemoryHandler.scan_pointer_by_pattern(pattern, 7)
        self.FPT.log("found zoom pointer at offset %s"%hex(ptr-self.FPT.api.MemoryHandler.process_base.lpBaseOfDll),logging.DEBUG)
        self.addr = self.FPT.api.MemoryHandler.read_ulonglong(ptr) + 284
        self.FPT.log("found zoom address at addr %s"%hex(self.addr),logging.DEBUG)
        self.FPT.storage.data.setdefault('user_default', 20.0)
        self.FPT.api.command.register(command, self.process_command)
        # self.FPT.register_event("log_event", self.process_command)

    def plugin_onunload(self):
        self.FPT.api.command.unregister(command)

    def process_command(self, args):
        self.FPT.api.Magic.echo_msg(self._process_command(args))

    async def plugin_start(self):
        self.FPT.api.MemoryHandler.write_float(self.addr, float(self.FPT.storage.data["user_default"]))

    def _process_command(self, arg):
        try:
            if arg[0] == "set":
                if arg[1] == 'default':
                    arg[1] = default
                else:
                    self.FPT.storage.data["user_default"] = float(arg[1])
                self.FPT.api.MemoryHandler.write_float(self.addr, float(arg[1]))
                return "set to %s" % arg[1]
            elif arg[0] == "get":
                return self.FPT.api.MemoryHandler.read_float(self.addr)
            else:
                return "unknown arg [%s]" % arg[0]
        except Exception as e:
            return str(e)
