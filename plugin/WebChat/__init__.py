import json
import time
from asyncio import CancelledError,set_event_loop,new_event_loop,run

from FFxivPythonTrigger import PluginBase
from aiohttp import web, WSMsgType
import asyncio
from pathlib import Path
import sys

res = Path(sys._MEIPASS)/'res'/'WebChat' if getattr(sys, 'frozen', False) else Path(__file__).parent / 'res'

default_host = "127.0.0.1"
default_port = 2020


class WebChat(PluginBase):
    name = "web chat"

    async def root_handler(self, request):
        return web.HTTPFound('/index.html')

    def macro_command(self, s):
        return self.FPT.api.Magic.macro_command(s)

    async def ws_handler(self, request):
        ws = web.WebSocketResponse()
        cid = self.client_count
        self.client_count += 1
        self.clients[cid] = ws
        await ws.prepare(request)
        for msg in self.chatLogCache[-200:]: await ws.send_json(msg)
        try:
            async for msg in ws:
                if msg.type == WSMsgType.TEXT:
                    try:
                        data = json.loads(msg.data)
                        if data['a'] == "close":
                            await ws.close()
                        elif data['a'] == "macro":
                            self.macro_command(data['m'])
                        elif data['a'] == "say":
                            self.macro_command("/s %s" % data['m'])
                        elif data['a'] == "emote":
                            self.macro_command("/em %s" % data['m'])
                        elif data['a'] == "yell":
                            self.macro_command("/y %s" % data['m'])
                        elif data['a'] == "shout":
                            self.macro_command("/sh %s" % data['m'])
                        elif data['a'] == "tell":
                            self.macro_command("/t %s@%s %s" % (data['t'], data['s'], data['m']))
                        elif data['a'] == "alliance":
                            self.macro_command("/a %s" % data['m'])
                        elif data['a'] == "freecompany":
                            self.macro_command("/fc %s" % data['m'])
                        elif data['a'].startswith("cwlinkshell"):
                            self.macro_command("/cwl%d %s" % (int(data['a'][-1]), data['m']))
                        elif data['a'].startswith("linkshell"):
                            self.macro_command("/l%d %s" % (int(data['a'][-1]), data['m']))
                        elif data['a'] == "echo":
                            self.macro_command("/e %s" % data['m'])
                        elif data['a'] == "party":
                            self.macro_command("/p %s" % data['m'])
                        elif data['a'] == "novicenetwork":
                            self.macro_command("/b %s" % data['m'])
                        else:
                            await ws.send_json({'t': time.time(), 'c': -1, 's': None, 'm': "unknown action [%s]"%data['a']})
                    except Exception as e:
                        await ws.send_json({'t': time.time(), 'c': -1, 's': None, 'm': str(e)})
                elif msg.type == WSMsgType.ERROR:
                    pass
        except CancelledError:
            pass
        del self.clients[cid]
        return ws

    def plugin_onload(self):
        self.server_config = self.FPT.storage.data.setdefault('server', dict())
        self.app = web.Application()
        self.app.router.add_route('GET', '/', self.root_handler)
        self.app.router.add_route('GET', '/ws', self.ws_handler)
        self.app.router.add_static('/', path=res)
        self.clients = dict()
        self.client_count = 0
        self.FPT.register_event("log_event", self.deal_chat_log)
        self.chatLogCache = []
        self.FPT.guard=False
        self.loop=new_event_loop()

    async def _plugin_onunload(self):
        await self.runner.shutdown()
        await self.runner.cleanup()
        self.FPT.log("WebChat Server closed")
        self.work = False

    def plugin_onunload(self):
        asyncio.set_event_loop(self.loop)
        self.loop.create_task(self._plugin_onunload())

    async def _plugin_start(self):
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        host = self.server_config.setdefault('host', default_host)
        port = self.server_config.setdefault('port', default_port)
        await web.TCPSite(self.runner, host, port).start()
        self.FPT.log("WebChat Server started on %s:%s" % (host, port))
        self.work = True
        while self.work:
            await asyncio.sleep(1)

    def plugin_start(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._plugin_start())

    def deal_chat_log(self, event):
        data = event.get_dict()
        self.chatLogCache.append(data)
        if len(self.chatLogCache)>500:self.chatLogCache=self.chatLogCache[-200:]
        # print(data)
        for cid, client in self.clients.items():
            asyncio.run(client.send_json(data))
