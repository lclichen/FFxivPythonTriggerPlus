from FFxivPythonTrigger import PluginBase

offset = 0x1cb9024
default = 10.4
command='@sjump'

class SuperJump(PluginBase):
    name = "Super Jump"

    def plugin_onload(self):
        self.addr = self.FPT.api.MemoryHandler.process_base.lpBaseOfDll + offset
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
                return "unknown arg [%s]"%arg[0]
        except Exception as e:
            return str(e)

