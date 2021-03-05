from FFxivPythonTrigger import PluginBase
import traceback
import logging

"""
provide a service process echo message as commands
api:    command
            register(command: str, callback:callable)
            unregister(command:str)

privide some basic control commands
command:    @fpt
format:     /e @fpt [func] [args]...
functions (*[arg] is optional args):
    [close]:    shut down the FFxiv Python trigger (recommend!!!!)
    [raise]:    try to raise an exception
    [log]:      log something
                format: /e @fpt log [message]
"""

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
        elif args[0] == 'log':
            self.FPT.log(" ".join(args[1:]))

    def deal_chat_log(self, event):
        if event.channel_id == 56:
            args = event.message.split(' ')
            if args[0] in self.commands:
                self.FPT.log(event.message,logging.DEBUG)
                try:
                    self.commands[args[0]](args[1:])
                except SystemExit:
                    raise SystemExit
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

