from .Base import AutoComboBase


class Warrior(AutoComboBase):
    def plugin_onload(self):
        super(Warrior, self).plugin_onload()
        self.war_key = self.FPT.storage.data.setdefault('war', dict())
        self.war_key.setdefault('single', [1, 1])
        self.war_key.setdefault('multi', [1, 2])

    def warrior_logic(self):
        meActor = self.get_me()
        if meActor is None: return
        effects = meActor.effects.get_dict()
        combo_id = self.comboState.actionId
        gauge = self.FPT.api.FFxivMemory.playerInfo.get_gauge()
        use_strength = 1177 in effects or gauge.beast >= 70
        if use_strength and meActor.level >= 35:
            self.change_skill(*self.war_key['single'], '原初之魂')
        elif combo_id == 31:
            self.change_skill(*self.war_key['single'], '凶残裂', (4, '重劈'))
        elif combo_id == 37:
            if 90 in effects and effects[90].timer > 5:
                self.change_skill(*self.war_key['single'], '暴风斩', (26, '重劈'))
            else:
                self.change_skill(*self.war_key['single'], '暴风碎', (50, '暴风斩'), (26, '重劈'))
        else:
            self.change_skill(*self.war_key['single'], '重劈')

        if use_strength and meActor.level >= 45:
            self.change_skill(*self.war_key['multi'], '钢铁旋风')
        elif combo_id == 41:
            self.change_skill(*self.war_key['multi'], '秘银暴风', (40, '超压斧'))
        else:
            self.change_skill(*self.war_key['multi'], '超压斧')
