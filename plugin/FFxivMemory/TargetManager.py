from .models.Target import TargetPtr
from .models.Actor import Actor


class TargetManager(TargetPtr):
    @property
    def current(self):
        return Actor(self.handler, self.currentPtr) if self.currentPtr else None

    @property
    def mouseOver(self):
        return Actor(self.handler, self.mouseOverPtr) if self.mouseOverPtr else None

    @property
    def focus(self):
        return Actor(self.handler, self.focusPtr) if self.focusPtr else None

    @property
    def previous(self):
        return Actor(self.handler, self.previousPtr) if self.previousPtr else None

    def set_current(self,actor=None):
        self["currentPtr"]=actor.base if actor is not None else 0

    def set_focus(self,actor=None):
        self["focusPtr"]=actor.base if actor is not None else 0

def get_target_manager(handler):
    _ = handler.ida_sig_to_pattern
    scan = handler.scan_pointer_by_pattern
    addr = scan(_("48 8B 05 ?? ?? ?? ?? 48 8D 0D ?? ?? ?? ?? FF 50 ?? 48 85 DB"), 7)
    return TargetManager(handler, addr)
