import logging

from FFxivPythonTrigger import PluginBase
from aiohttp import web
import asyncio

default_host = "127.0.0.1"
default_port = 2019

class NamazuServer(PluginBase):
    name = "Namazu Server"

    async def command(self, request):
        try:
            self.FPT.api.Magic.macro_command(await request.text())
        except Exception as e:
            return web.Response(body=str(e).encode('utf-8'))
        return web.Response(body="success".encode('utf-8'))

    def plugin_onload(self):
        self.server_config = self.FPT.storage.data.setdefault('server', dict())
        self.app = web.Application()
        self.app.add_routes([web.post('/command', self.command)])
        self.loop = asyncio.new_event_loop()
        self.work=False

    async def _plugin_onunload(self):
        await self.runner.shutdown()
        await self.runner.cleanup()
        self.FPT.log("Namazu Server closed")
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
        self.FPT.log("Namazu Server started on %s:%s" % (host, port))
        self.work = True
        while self.work:
            await asyncio.sleep(1)

    def plugin_start(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._plugin_start())
