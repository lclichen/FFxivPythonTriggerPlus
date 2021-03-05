import atexit
import logging
import traceback
import threading
import sys

from .AttrContainer import AttrContainer
from .Storage import Storage
from .Logger import Logger

t_lock = threading.Lock()


class Mission(threading.Thread):
    def __init__(self, name: str, mission_id: int, mission, *args, **kwargs):
        super(Mission, self).__init__(name="%s#%s" % (name, mission_id))
        self.name = name
        self.mission_id = mission_id
        self.mission = mission
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.mission(*self.args, **self.kwargs)


class FFxivPythonTrigger(object):
    def __init__(self, plugins=None):
        self.plugins = dict()
        self.api = AttrContainer()
        self.missions = list()
        self.events = dict()
        self.storage = Storage()
        self.mainStorage = self.storage.get_core_storage()
        self.logger = Logger(log_path=self.mainStorage.path)
        self.allow_create_missions = True
        atexit.register(self.close)
        try:
            self.register_plugins(plugins if plugins is not None else [])
        except:
            self.close()

    def log(self, msg, lv=None):
        self.logger.log('Main', msg, lv)

    def register_plugins(self, plugins):
        for plugin in plugins:
            self.register_plugin(plugin)

    def register_plugin(self, plugin):
        self.log("register plugin [start]: %s" % plugin.name, logging.DEBUG)
        temp_plugin = PluginContainer(self, plugin)
        if temp_plugin.name in self.plugins:
            raise Exception("Plugin %s was already registered" % temp_plugin.name)
        self.plugins[temp_plugin.name] = temp_plugin
        try:
            temp_plugin.init_plugin()
        except:
            self.log('error occurred during plugin initialization: %s' % temp_plugin.name, logging.ERROR)
            self.log('error trace:\n' + traceback.format_exc())
            raise Exception('plugin initialization error')
        self.log("register plugin [success]: %s" % plugin.name)

    def register_event(self, event_id, callback):
        if event_id not in self.events:
            self.events[event_id] = set()
        self.events[event_id].add(callback)

    def unregister_event(self, event_id, callback):
        self.events[event_id].remove(callback)
        if not self.events[event_id]:
            del self.events[event_id]

    def process_event(self, event):
        if event.id in self.events:
            for callback in self.events[event.id].copy():
                callback.call(event)

    def unload_plugin(self, plugin_name):
        self.log("unregister plugin [start]: %s" % plugin_name, logging.DEBUG)
        try:
            self.plugins[plugin_name].plugin_unload()
        except:
            self.log('error occurred during unload plugin\n %s' % traceback.format_exc(), logging.ERROR)
        del self.plugins[plugin_name]
        self.log("unregister plugin [success]: %s" % plugin_name)

    def close(self):
        self.allow_create_missions = False
        for name in reversed(list(self.plugins.keys())):
            self.unload_plugin(name)
        self.mainStorage.store()

    def append_missions(self, mission, guard=True):
        if self.allow_create_missions:
            if guard: self.missions.append(mission)
            mission.start()
            return True
        return False

    def start(self):
        for plugin in self.plugins.values():
            plugin.start()
        if self.missions:
            self.log('FFxiv Python Trigger started')
            p = 0
            while p < len(self.missions):
                self.missions[p].join()
                p += 1
            self.log('FFxiv Python Trigger closed')
        else:
            self.log('FFxiv Python Trigger closed (no mission is found)')
        alive_missions =[m for m in self.missions if m.is_alive()]
        if self.plugins or alive_missions:
            self.log('above item havn\'t cleared, try again')
            for plugin in self.plugins:
                self.log("plugin: "+plugin.name)
            for mission in alive_missions:
                print("mission: "+str(mission))
            self.close()


class PluginContainer(object):
    def __init__(self, fpt: FFxivPythonTrigger, plugin):
        self._fpt = fpt
        self.api = fpt.api
        self.process_event = fpt.process_event
        self.name = plugin.name
        self._plugin = plugin
        self.events = list()
        self.apis = list()
        self.plugin = None
        self.storage = self._fpt.storage.get_plugin_storage(self.name)
        self.mission_count = 0
        self.missions = list()
        self.guard=True

    def log(self, msg, lv=None):
        self._fpt.logger.log(self.name, msg, lv)

    def init_plugin(self):
        self.plugin = self._plugin(self)
        self.plugin.plugin_onload()

    def create_mission(self, call, *args, **kwargs):
        def temp(*args, **kwargs):
            try:
                call(*args, **kwargs)
            except SystemExit:
                raise SystemExit
            except:
                self.log("error occurred in mission:" + traceback.format_exc(), logging.ERROR)

        with t_lock:
            mId = self.mission_count
            self.mission_count += 1
        mission = Mission(self.name, mId, temp, *args, **kwargs)
        if self._fpt.append_missions(mission,self.guard):
            self.missions.append(mission)

    def start(self):
        self.create_mission(self.plugin.plugin_start)

    def register_api(self, name, api_object):
        self.apis.append(name)
        self.api.register_attribute(name, api_object)

    def register_event(self, event_id, call):
        callback = EventCallback(self, call)
        self.events.append((event_id, callback))
        self._fpt.register_event(event_id, callback)

    def plugin_unload(self):
        for event_id, callback in self.events:
            self._fpt.unregister_event(event_id, callback)
        for name in self.apis:
            self.api.unregister_attribute(name)
        self.plugin.plugin_onunload()
        self.storage.store()
        if not self.guard:
            try:
                for m in self.missions: m.join(-1)
            except:
                pass


class EventCallback(object):
    def __init__(self, plugin, call):
        self.plugin = plugin
        self._call = call

    def call(self, *args, **kwargs):
        self.plugin.create_mission(self._call, *args, **kwargs)


class EventBase(object):
    id = 0
    name = "unnamed event"


class PluginBase(object):
    name = "unnamed_plugin"

    def __init__(self, FPT: PluginContainer):
        self.FPT = FPT

    def plugin_onload(self):
        pass

    def plugin_onunload(self):
        pass

    def plugin_start(self):
        pass
