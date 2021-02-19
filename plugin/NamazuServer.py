from FFxivPythonTrigger import PluginBase
from aiohttp import web
import asyncio

default_host = "127.0.0.1"
default_port = 2019
loop = asyncio.get_event_loop()


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
        self.app = web.Application(loop=loop)
        self.app.add_routes([web.post('/command', self.command)])
        self.runner = web.AppRunner(self.app)
        loop.run_until_complete(self.runner.setup())

    def plugin_onunload(self):
        asyncio.run(self.app.shutdown())

    async def plugin_start(self):
        host = self.server_config.setdefault('host', default_host)
        port = self.server_config.setdefault('port', default_port)
        await web.TCPSite(self.runner, host, port).start()
