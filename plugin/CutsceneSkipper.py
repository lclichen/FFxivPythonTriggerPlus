from FFxivPythonTrigger import PluginBase

nop = b"\x90\x90"
pattern = b"\x8B\xD7\x48\x8B\x08\x4C\x8B\x01"
command="@cutscence"

class CutsceneSkipper(PluginBase):
    name = "Cutscene Skipper"


    def plugin_onload(self):
        self.scanAddress = None
        self.trigger_id = None
        self.original_0 = None
        self.original_1 = None
        self.scanAddress = self.FPT.api.MemoryHandler.pattern_scan_main_module(pattern)
        self.FPT.api.command.register(command, self.process_command)
        # self.FPT.register_event("log_event", self.process_command)

    def process_command(self, args):
        self.FPT.api.Magic.echo_msg(self._process_command(args))


    def _process_command(self, arg):
        try:
            if arg[0] == "patch" or arg[0] == "p":
                return "patch success" if self.patch() else "invalid patch"
            elif arg[0] == "dispatch" or arg[0] == "d":
                return "dispatch success" if self.dispatch() else "invalid dispatch"
            else:
                return "unknown arguments {}".format(arg[0])
        except Exception as e:
            return str(e)

    def patch(self):
        if self.scanAddress is None:
            raise Exception("address scan not found")

        original_0 = self.FPT.api.MemoryHandler.read_bytes(self.scanAddress + 0x11, 2)
        original_1 = self.FPT.api.MemoryHandler.read_bytes(self.scanAddress + 0x2c, 2)

        if original_0 == nop and original_1 == nop:
            raise Exception("already patched")

        self.original_0 = original_0
        self.original_1 = original_1

        self.FPT.api.MemoryHandler.write_bytes(self.scanAddress + 0x11, nop, len(nop))
        self.FPT.api.MemoryHandler.write_bytes(self.scanAddress + 0x2c, nop, len(nop))

        return True

    def dispatch(self):
        if self.scanAddress is None:
            raise Exception("address scan not found")

        original_0 = self.FPT.api.MemoryHandler.read_bytes(self.scanAddress + 0x11, 2)
        original_1 = self.FPT.api.MemoryHandler.read_bytes(self.scanAddress + 0x2c, 2)

        if original_0 != nop or original_1 != nop:
            raise Exception("not patched")

        if self.original_0 is None:
            raise Exception("original data not found")

        self.FPT.api.MemoryHandler.write_bytes(self.scanAddress + 0x11, self.original_0, len(nop))
        self.FPT.api.MemoryHandler.write_bytes(self.scanAddress + 0x2c, self.original_1, len(nop))

        self.original_0 = None
        self.original_1 = None

        return True

    def plugin_onunload(self):
        self.FPT.api.command.unregister(command)
        try:
            self.dispatch()
        except:
            pass
