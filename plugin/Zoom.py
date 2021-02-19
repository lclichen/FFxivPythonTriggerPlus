from FFxivPythonTrigger import PluginBase

pattern=b"\x48\x8D\x1D....\x48\x8B\xCB\x41\x8D\x50\x02"
default = 20
command='@zoom'

class ZoomPlugin(PluginBase):
    name = "zoom plugin"

    def plugin_onload(self):
        self.addr = self.FPT.api.MemoryHandler.read_ulonglong(self.FPT.api.MemoryHandler.scan_pointer_by_pattern(pattern,7))+284
        self.FPT.api.command.register(command, self.process_command)
        #self.FPT.register_event("log_event", self.process_command)

    def plugin_onunload(self):
        self.FPT.api.command.unregister(command)

    def process_command(self, args):
        self.FPT.api.Magic.echo_msg(self._process_command(args))

    def _process_command(self, arg):
        try:
            if arg[0] == "set":
                if arg[1] == 'default':
                    arg[1] = default
                self.FPT.api.MemoryHandler.write_float(self.addr, float(arg[1]))
                return "set to %s" % arg[1]
            elif arg[0] == "get":
                return self.FPT.api.MemoryHandler.read_float(self.addr)
            else:
                return "unknown arg [%s]" % arg[0]
        except Exception as e:
            return str(e)
