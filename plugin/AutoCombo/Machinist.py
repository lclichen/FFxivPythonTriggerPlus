from .Base import AutoComboBase


class Machinist(AutoComboBase):
    def plugin_onload(self):
        super(Machinist, self).plugin_onload()
        self.mch_key = self.FPT.storage.data.setdefault('mch', dict())
        self.mch_key.setdefault('single', [1, 1])
        self.mch_key.setdefault('multi', [1, 3])

    def machinist_logic(self):
        meActor = self.get_me()
        combo_id = self.comboState.actionId
        gauge = self.FPT.api.FFxivMemory.playerInfo.get_gauge()
        if gauge.overheatMilliseconds and meActor.level >= 35:
            self.change_skill(*self.mch_key['single'], "热冲击")
        elif combo_id == 2866:
            self.change_skill(*self.mch_key['single'], "独头弹", (2, "分裂弹"))
        elif combo_id == 2868:
            self.change_skill(*self.mch_key['single'], "狙击弹", (26, "分裂弹"))
        else:
            self.change_skill(*self.mch_key['single'], "分裂弹")
        if gauge.overheatMilliseconds and meActor.level >= 52:
            self.change_skill(*self.mch_key['multi'], "自动弩")
        else:
            self.change_skill(*self.mch_key['multi'], "散射")
