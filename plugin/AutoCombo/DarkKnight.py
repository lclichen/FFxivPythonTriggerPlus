from .Base import AutoComboBase


class DarkKnight(AutoComboBase):
    def plugin_onload(self):
        super(DarkKnight, self).plugin_onload()
        self.dk_key = self.FPT.storage.data.setdefault('dk', dict())
        self.dk_key.setdefault('single', [1, 1])

    def dark_knight_logic(self):
        combo_id = self.comboState.actionId
        if combo_id == 3617:
            self.change_skill(*self.dk_key['single'], '吸收斩', (2, '重斩'))
        elif combo_id == 3623:
            self.change_skill(*self.dk_key['single'], '噬魂斩', (26, '重斩'))
        else:
            self.change_skill(*self.dk_key['single'], '重斩')
