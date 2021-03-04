from .Base import AutoComboBase

"""
15989：瀑泻（1）
15990：喷泉（2）
15991：逆瀑泻（20）
15992：坠喷泉（40）
15993：风车（15）
15994：落刃雨（25）
15995：升风车（35）
15996：落血雨（45）
16007：扇舞·序（30）
16008：扇舞·破（50）
16009：扇舞·急（66）
15997：标准舞步（15）
15998：技巧舞步（70）
16005：剑舞（76）
"""
"""
1814,逆瀑泻预备
1815,坠喷泉预备
1816,升风车预备
1817,落血雨预备
1818,标准舞步
1819,技巧舞步
1820,扇舞·急预备
1821,标准舞步结束
1822,技巧舞步结束
"""


def step_to_skill(step):
    return 15988 + step if step > 0 else None


class Dancer(AutoComboBase):
    def plugin_onload(self):
        super(Dancer, self).plugin_onload()
        self.dnc_key = self.FPT.storage.data.setdefault('dnc', dict())
        self.dnc_key.setdefault('single', [1, 1])
        self.dnc_key.setdefault('multi', [1, 2])
        self.dnc_key.setdefault('smallDnc', [1, 3])
        self.dnc_key.setdefault('bigDnc', [1, 4])

    def dancer_logic(self):
        meActor = self.get_me()
        if meActor is None: return
        effects = meActor.effects.get_dict()
        combo_id = self.comboState.actionId
        gauge = self.FPT.api.FFxivMemory.playerInfo.get_gauge()
        if 1814 in effects:
            self.change_skill(*self.dnc_key['single'], 15991)
        elif 1815 in effects:
            self.change_skill(*self.dnc_key['single'], 15992)
        elif combo_id == 15989:
            self.change_skill(*self.dnc_key['single'], 15990, (2, 15989))
        else:
            self.change_skill(*self.dnc_key['single'], 15989)

        if 1816 in effects:
            self.change_skill(*self.dnc_key['multi'], 15995)
        elif 1817 in effects:
            self.change_skill(*self.dnc_key['multi'], 15996)
        elif combo_id == 15993:
            self.change_skill(*self.dnc_key['multi'], 15994, (25, 15993))
        else:
            self.change_skill(*self.dnc_key['multi'], 15993)

        if 1818 in effects and gauge.currentStep < 2:
            self.change_skill(*self.dnc_key['smallDnc'], step_to_skill(gauge.step[gauge.currentStep]))
        else:
            self.change_skill(*self.dnc_key['smallDnc'], 15997)

        if 1819 in effects and gauge.currentStep < 4:
            self.change_skill(*self.dnc_key['bigDnc'], step_to_skill(gauge.step[gauge.currentStep]))
        else:
            self.change_skill(*self.dnc_key['bigDnc'], 15998)
