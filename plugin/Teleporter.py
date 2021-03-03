import logging
from FFxivPythonTrigger import PluginBase
import math
import traceback
from time import sleep

"""
tele~port~er~~~

command:    @tp
format:     /e @tp [func] [args]...
functions (*[arg] is optional args):
    [get]:          get current coordinates
    
    [set]:          set current coordinates
                    format: /e @tp set [x:float] [y:float] [z:float]
                    
    [lock]:         lock current coordinates by a "While True" loop
    
    [list]:         list saved coordinates in current zone
    
    [save]:         save coordinates with a name
    
                    format: /e @tp save [name:str]
    [drop]:         drop a saved coordinates
    
                    format: /e @tp drop [name:str]
                    
    [goto]:         goto a saved coordinates with 15 meters limit
                    format: /e @tp goto [name:str]
                    
    [force-goto]:   goto a saved coordinates with no distance limit
                    format: /e @tp force-goto [name:str]

    relative coordinates teleport:
        format: /e @tp [direction] [distance:float]
        direction:  u/up,
                    d/down,
                    f/front,
                    l/left,
                    r/right,
                    b/back,
                    n/north,
                    e/east,
                    w/west,
                    s/south
"""

command = "@tp"
pattern_main = b"\xF3\x0F......\xEB.\x48\x8B.....\xE8....\x48\x85"
pattern_fly = b"\x48\x8D.....\x84\xC0\x75.\x48\x8D.....\x80\x79\x66.\x74.\xE8....\xC6\x87\xF4\x03.."


class Teleporter(PluginBase):
    name = "Teleporter"

    def plugin_onload(self):
        h = self.FPT.api.MemoryHandler
        self.ptr_main = h.scan_pointer_by_pattern(pattern_main, 8) + 0x14
        self.addr_fly = h.scan_pointer_by_pattern(pattern_fly, 7) + 16
        self.FPT.log("main coordinate pointer at %s"%hex(self.ptr_main),logging.DEBUG)
        self.FPT.log("fly coordinate address at %s"%hex(self.addr_fly),logging.DEBUG)
        _Coor = h.get_memory_class({
            "x": ('float', 0),
            "y": ('float', 8),
            "z": ('float', 4),
            "r": ('float', 16),
        }, 0)
        Coor = h.get_pointer(_Coor, pShifts=[160])
        self._coor_main = Coor(h, self.ptr_main)
        self.coor_fly = _Coor(h, self.addr_fly)
        self.FPT.api.command.register(command, self.process_command)
        self.work = False
        self.lock_coor = None

    @property
    def coor_main(self):
        return self._coor_main.get_value()

    def plugin_start(self):
        self.work = True
        while self.work:
            try:
                if self.lock_coor is not None:
                    self.tp(*self.lock_coor)
                else:
                    sleep(0.1)
            except:
                self.FPT.log("error occurred:\n"+traceback.format_exc(),logging.ERROR)

    def plugin_onunload(self):
        self.FPT.api.command.unregister(command)
        self.work = False

    def tp(self, x=None, y=None, z=None):
        if x is not None:
            self.coor_main['x'] = x
            self.coor_fly['x'] = x
        if y is not None:
            self.coor_main['y'] = y
            self.coor_fly['y'] = y
        if z is not None:
            self.coor_main['z'] = z
            self.coor_fly['z'] = z

    def tp_rxy(self, angle, dis):
        self.tp(x=self.coor_main.x + (math.sin(angle) * dis), y=self.coor_main.y + (math.cos(angle) * dis))

    def tp_rz(self, dis):
        self.tp(z=self.coor_main.z + dis)

    def get_zone_data(self):
        zid = self.FPT.api.FFxivMemory.zone.id
        data = self.FPT.storage.data.setdefault(str(zid), dict())
        return zid, data

    def _process_command(self, args):
        a1 = args[0].lower()
        if a1 == "set":
            return self.tp(float(args[1]), float(args[2]), float(args[3]))
        elif a1 == "get":
            return "%.2f %.2f %.2f" % (self.coor_main.x, self.coor_main.y, self.coor_main.z)
        elif a1 == 'lock':
            if self.lock_coor is None:
                self.lock_coor = (self.coor_main.x, self.coor_main.y, self.coor_main.z)
                return "lock at [%.2f,%.2f,%.2f]" % self.lock_coor
            else:
                self.lock_coor = None
                return "unlocked"
        elif a1 == "list":
            zid, data = self.get_zone_data()
            return "%s (%s): %s" % (zid, len(data), '/'.join(data.keys()))
        elif a1 == "save":
            zid, data = self.get_zone_data()
            if args[1] in data:
                return "key [%s] is already in zone [%s]" % (args[1], zid)
            data[args[1]] = [self.coor_main.x, self.coor_main.y, self.coor_main.z]
            self.FPT.storage.store()
            return "%s (%s): %s" % (zid, len(data), '/'.join(data.keys()))
        elif a1 == "goto":
            zid, data = self.get_zone_data()
            if args[1] not in data:
                return "key [%s] is not in zone [%s]" % (args[1], zid)
            dis = math.sqrt((data[args[1]][0] - self.coor_main.x) ** 2 + (data[args[1]][1] - self.coor_main.y) ** 2)
            if dis >= 15:
                return "target point is %.2f meters far, teleport to target is a dangerous operation,please use 'force-goto'" % dis
            self.tp(*data[args[1]])
            return "success"
        elif a1 == "force-goto":
            zid, data = self.get_zone_data()
            if args[1] not in data:
                return "key [%s] is not in zone [%s]" % (zid, args[1])
            self.tp(*data[args[1]])
            return "success"
        elif a1 == "drop":
            zid, data = self.get_zone_data()
            if args[1] not in data:
                return "key [%s] is not in zone [%s]" % (zid, args[1])
            del data[args[1]]
            self.FPT.storage.store()
            return "success"
        dis = float(args[1])
        if a1 in ["north", "n"]:
            self.tp_rxy(math.pi, dis)
            return "tp to north %s" % dis
        elif a1 in ["east", "e"]:
            self.tp_rxy(math.pi / 2, dis)
            return "tp to east %s" % dis
        elif a1 in ["west", "w"]:
            self.tp_rxy(math.pi / -2, dis)
            return "tp to west %s" % dis
        elif a1 in ["south", "s"]:
            self.tp_rxy(0, dis)
            return "tp to south %s" % dis
        elif a1 in ["front", "f"]:
            self.tp_rxy(self.coor_main.r, dis)
            return "tp to front %s" % dis
        elif a1 in ["back", "b"]:
            self.tp_rxy(self.coor_main.r - math.pi, dis)
            return "tp to back %s" % dis
        elif a1 in ["left", "l"]:
            self.tp_rxy(self.coor_main.r + math.pi / 2, dis)
            return "tp to left %s" % dis
        elif a1 in ["right", "r"]:
            self.tp_rxy(self.coor_main.r - math.pi / 2, dis)
            return "tp to right %s" % dis
        elif a1 in ["up", "u"]:
            self.tp_rz(dis)
            return "tp to up %s" % dis
        elif a1 in ["down", "d"]:
            self.tp_rz(-dis)
            return "tp to down %s" % dis
        else:
            return "unknown direction: [%s]" % a1

    def process_command(self, args):
        try:
            msg = self._process_command(args)
            if msg is not None:
                self.FPT.api.Magic.echo_msg(msg)
        except Exception as e:
            self.FPT.api.Magic.echo_msg(str(e))
