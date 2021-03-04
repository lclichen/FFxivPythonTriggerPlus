from FFxivPythonTrigger import PluginBase
import logging

"""
disable all the entity move in the client
command:    @lockPos
format:     /e @lockPos *[p(patch)/d(dispatch)]
"""

pattern = b"\xF3\x0F......\x48\x8B.\xF3\x0F......\xF3\x0F......\xF6\x81\x96..."
command = "@lockPos"


class PosLocker(PluginBase):
    name = "pos locker"

    def plugin_onload(self):
        self.scanAddress = self.FPT.api.MemoryHandler.pattern_scan_main_module(pattern)
        if self.scanAddress:
            self.FPT.log("found code address at %s" % hex(self.scanAddress),logging.DEBUG)
        else:
            self.FPT.log("code address not found",logging.WARNING)

        self.patched = False
        self.raw = None
        self.FPT.api.command.register(command, self.process_command)

    def plugin_onunload(self):
        self.FPT.api.command.unregister(command)
        try:
            self.dispatch()
        except:
            pass

    def process_command(self, args):
        self.FPT.api.Magic.echo_msg(self._process_command(args))

    def _process_command(self, arg):
        try:
            if len(arg):
                if arg[0] == "patch" or arg[0] == "p":
                    return self.patch()
                elif arg[0] == "dispatch" or arg[0] == "d":
                    return self.dispatch()
                else:
                    return "unknown arguments {}".format(arg[0])
            else:
                if self.patched:
                    return self.dispatch()
                else:
                    return self.patch()
        except Exception as e:
            return str(e)

    def patch(self):
        if self.scanAddress is None:
            raise Exception("address scan not found")
        if self.patched:
            raise Exception("already patched")
        mh=self.FPT.api.MemoryHandler
        self.raw = mh.read_bytes(self.scanAddress,27)
        mh.write_bytes(self.scanAddress,b'\x90'*8,8)
        mh.write_bytes(self.scanAddress+8+3,b'\x90'*16,16)
        self.patched=True
        return "patch success"


    def dispatch(self):
        if self.scanAddress is None:
            raise Exception("address scan not found")
        if not self.patched:
            raise Exception("not patched")
        if self.raw is None:
            raise Exception("raw data not found")
        self.FPT.api.MemoryHandler.write_bytes(self.scanAddress,self.raw,27)
        self.raw=None
        self.patched = False
        return "dispatch success"
