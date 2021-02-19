from .Base import AutoComboBase


class RedMage(AutoComboBase):
    def plugin_onload(self):
        super(RedMage, self).plugin_onload()
        self.rdm_key = self.FPT.storage.data.setdefault('rdm', dict())
        self.rdm_key.setdefault('single', [1, 1])
        self.rdm_key.setdefault('multi', [1, 2])
        self.rdm_key.setdefault('combo', [1, 3])

    def red_mage_logic(self):
        meActor = self.get_me()
        if meActor is None: return
        effects = {effect.buffId: effect for effect in meActor.effects if effect.buffId != 0}
        speedSpell = 1249 in effects or 167 in effects
        gauge = self.FPT.api.FFxivMemory.playerInfo.get_gauge()
        white = gauge.white_mana <= gauge.black_mana
        if speedSpell:
            self.change_skill(*self.rdm_key['multi'], '散碎')
            if white:
                self.change_skill(*self.rdm_key['single'], '赤疾风', (10, '赤闪雷'), (4, '摇荡'))
            else:
                self.change_skill(*self.rdm_key['single'], '赤闪雷', (4, '摇荡'))
        else:
            if 1234 in effects:
                self.change_skill(*self.rdm_key['single'], '赤火炎')
            elif 1235 in effects:
                self.change_skill(*self.rdm_key['single'], '赤飞石')
            else:
                self.change_skill(*self.rdm_key['single'], '摇荡')
            if white:
                self.change_skill(*self.rdm_key['multi'], '赤烈风', (22, '赤震雷'), (18, '散碎'))
            else:
                self.change_skill(*self.rdm_key['multi'], '赤震雷', (18, '散碎'))
        combo_id = self.comboState.actionId
        if combo_id == 7504:
            self.change_skill(*self.rdm_key['combo'], '交击斩', (35, '回刺'))
        elif combo_id == 7512:
            self.change_skill(*self.rdm_key['combo'], '连攻', (50, '回刺'))
        elif combo_id == 7529:
            if white:
                self.change_skill(*self.rdm_key['combo'], '赤疾风', (70, '赤闪雷'), (68, '回刺'))
            else:
                self.change_skill(*self.rdm_key['combo'], '赤闪雷', (68, '回刺'))
        elif combo_id == 7525 or combo_id == 7526:
            self.change_skill(*self.rdm_key['combo'], '摇荡', (80, '回刺'))
        else:
            self.change_skill(*self.rdm_key['combo'], '回刺')
