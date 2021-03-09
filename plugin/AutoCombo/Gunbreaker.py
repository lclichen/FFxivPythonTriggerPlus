from .Base import AutoComboBase


class Gunbreaker(AutoComboBase):
    def plugin_onload(self):
        super(Gunbreaker, self).plugin_onload()
        self.gnb_key = self.FPT.storage.data.setdefault('gnb', dict())
        self.gnb_key.setdefault('single', [1, 1])
        self.gnb_key.setdefault('multi', [1, 2])
        self.gnb_key.setdefault('combo', [1, 3])
        self.gnb_key.setdefault('combo_bind', True)

    def gunbreaker_logic(self):
        meActor = self.get_me()
        combo_id = self.comboState.actionId
        effects = meActor.effects.get_dict()
        gauge = self.FPT.api.FFxivMemory.playerInfo.get_gauge()

        if combo_id == 16137:
            self.change_skill(*self.gnb_key['single'], '残暴弹', (4, '利刃斩'))
        elif combo_id == 16139:
            self.change_skill(*self.gnb_key['single'], '迅连斩', (26, '利刃斩'))
        else:
            self.change_skill(*self.gnb_key['single'], '利刃斩')

        if combo_id == 16141:
            self.change_skill(*self.gnb_key['multi'], '恶魔杀', (40, '恶魔切'))
        else:
            self.change_skill(*self.gnb_key['multi'], '恶魔切')

        self.gunbreaker_combo_logic(effects,gauge.continuationState)

    def gunbreaker_combo_logic(self,effects,continuationState):
        if self.gnb_key['combo_bind'] and (1842 in effects or 1843 in effects or 1844 in effects):
            return self.change_skill(*self.gnb_key['combo'], '续剑')
        if continuationState == 1:
            self.change_skill(*self.gnb_key['combo'], '猛兽爪')
        elif continuationState == 2:
            self.change_skill(*self.gnb_key['combo'], '凶禽爪')
        else:
            self.change_skill(*self.gnb_key['combo'], '烈牙')
