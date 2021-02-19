from FFxivPythonTrigger import PluginBase
import traceback

class CommandManager(dict):
    def register(self, command, callback):
        if command in self:
            raise Exception("Command %s already exists" % command)
        self[command] = callback

    def unregister(self, command):
        if command in self:
            del self[command]


class Command(PluginBase):
    name = "command controller"

    def FptManager(self, args):
        if args[0] == 'close':
            self.FPT._fpt.close()
        elif args[0] == 'raise':
            raise Exception("111aw")

    def deal_chat_log(self, event):
        if event.channel_id == 56:
            args = event.message.split(' ')
            if args[0] in self.commands:
                try:
                    self.commands[args[0]](args[1:])
                except:
                    self.FPT.log('exception occurred:\n{}'.format(traceback.format_exc()))

    def register(self, command: str, callback):
        if ' ' in command:
            raise Exception("Command should not contain blanks")
        if command in self.commands:
            raise Exception("Command %s already exists" % command)
        self.commands[command] = callback

    def unregister(self, command):
        if command in self.commands:
            del self.commands[command]

    def plugin_onload(self):
        class temp: register = self.register;unregister = self.unregister

        self.commands = dict()
        self.FPT.register_event("log_event", self.deal_chat_log)
        self.FPT.register_api('command', temp())
        self.register('@fpt',self.FptManager)

