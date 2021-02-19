from FFxivPythonTrigger import PluginBase
import math
import traceback

command = "@tp"
pattern_main = b"\xF3\x0F......\xEB.\x48\x8B.....\xE8....\x48\x85"
pattern_fly = b"\x48\x8D.....\x84\xC0\x75.\x48\x8D.....\x80\x79\x66.\x74.\xE8....\xC6\x87\xF4\x03.."


class Teleporter(PluginBase):
    name = "Teleporter"

    def plugin_onload(self):
        h = self.FPT.api.MemoryHandler
        ptr_main = h.scan_pointer_by_pattern(pattern_main, 8) + 0x14
        self.addr_main = h.read_ulonglong(ptr_main) + 160
        self.addr_fly = h.scan_pointer_by_pattern(pattern_fly, 7) + 16
        Coor = self.FPT.api.MemoryHandler.get_memory_lazy_class({
            "x": ('float', 0),
            "y": ('float', 8),
            "z": ('float', 4),
            "r": ('float', 16),
        }, 0)
        self.coor_main = Coor(h, self.addr_main)
        self.coor_fly = Coor(h, self.addr_fly)
        self.FPT.api.command.register(command, self.process_command)

    def plugin_onunload(self):
        self.FPT.api.command.unregister(command)

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
        elif a1 == "list":
            zid, data = self.get_zone_data()
            return "%s (%s): %s" % (zid,len(data),'/'.join(data.keys()))
        elif a1 == "save":
            zid, data = self.get_zone_data()
            if args[1] in data:
                return "key [%s] is already in zone [%s]"%(args[1],zid)
            data[args[1]] =[self.coor_main.x, self.coor_main.y, self.coor_main.z]
            self.FPT.storage.store()
            return "%s (%s): %s" % (zid,len(data),'/'.join(data.keys()))
        elif a1 == "goto":
            zid, data = self.get_zone_data()
            if args[1] not in data:
                return "key [%s] is not in zone [%s]" % (args[1],zid)
            dis=math.sqrt((data[args[1]][0]-self.coor_main.x)**2+(data[args[1]][1]-self.coor_main.y)**2)
            if dis>=15:
                return "target point is %.2f meters far, teleport to target is a dangerous operation,please use 'force-goto'"%dis
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
