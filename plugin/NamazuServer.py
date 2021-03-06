import logging

from FFxivPythonTrigger import PluginBase
from aiohttp import web
import asyncio
import traceback

default_host = "127.0.0.1"
default_port = 2019


class NamazuServer(PluginBase):
    name = "Namazu Server"

    async def post_route(self, request: web.Request):
        paths = request.path.strip('/').split('/')
        if not paths or paths[0] not in self.routes:
            res= web.json_response({'msg': 'resource not found', 'code': 404}, status=404)
        else:
            try:
                res=await self.routes[paths[0]](request)
            except:
                res= web.json_response({'msg': 'server error occurred', 'trace': traceback.format_exc(), 'code': 500}, status=500)
        self.FPT.log("request:%s ; response: %s"%(request,res),logging.DEBUG)
        return res

    async def command(self, request: web.Request):
        try:
            self.FPT.api.Magic.macro_command(await request.text())
        except Exception as e:
            return web.Response(body=str(e).encode('utf-8'))
        return web.Response(body="success".encode('utf-8'))

    def register_post_route(self, path, controller):
        if path in self.routes:
            raise Exception("%s is already registered" % path)
        self.routes[path] = controller

    def unregister_post_route(self, path):
        if path not in self.routes:
            raise Exception("%s is not registered" % path)
        del self.routes[path]

    def plugin_onload(self):
        self.server_config = self.FPT.storage.data.setdefault('server', dict())
        self.app = web.Application()
        self.app.add_routes([web.post('/{uri:.*}', self.post_route)])
        self.loop = asyncio.new_event_loop()
        self.routes = dict()
        self.register_post_route('command', self.command)
        self.work = False

        class temp: register_post_route = self.register_post_route;unregister_post_route = self.unregister_post_route
        self.FPT.register_api('Namazu',temp())

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
