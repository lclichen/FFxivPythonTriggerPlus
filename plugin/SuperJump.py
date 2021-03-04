from FFxivPythonTrigger import PluginBase
import logging

"""
change the jump value to let you jump higher -- or lower
command:    @sjump
format:     /e @sjump [func] [args]...
functions (*[arg] is optional args):
    [get]:      get current jump value
    [set]:      set current jump value
                format: /e @sjump set [value(float) / "default"]
"""

sig="f3 0f 10 35 ?? ?? ?? ?? 48 85 c0 74 ?? 48 8b 88 ?? ?? ?? ?? 48 85 c9 75 ?? 32 c0 eb ?? f6 05 ?? ?? ?? ?? ?? 75 ?? 33 d2 e8 ?? ?? ?? ?? f6 d8 " \
    "0f 28 d6 48 8b cb 1b d2 83 c2 ?? 0f 28 74 24 ?? 48 83 c4 ?? 5b e9 ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? 40 53 "
default = 10.4
command = '@sjump'


class SuperJump(PluginBase):
    name = "Super Jump"

    def plugin_onload(self):
        mh = self.FPT.api.MemoryHandler
        self.FPT.api.command.register(command, self.process_command)
        self.addr = mh.scan_pointer_by_pattern(mh.ida_sig_to_pattern(sig), 8)
        self.FPT.log("found address at %s" % hex(self.addr), logging.DEBUG)

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
