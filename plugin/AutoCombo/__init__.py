from . import DarkKnight, RedMage, Warrior, Gunbreaker, Machinist


class AutoCombo(
    DarkKnight.DarkKnight,
    RedMage.RedMage,
    Warrior.Warrior,
    Gunbreaker.Gunbreaker,
    Machinist.Machinist
):
    name = "Auto Combo"
    combos = {
        # 19: PaladinGauge,  # 骑士,PLD
        # 20: MonkGauge,  # 武僧,MNK
        21: Warrior.Warrior.warrior_logic,  # 战士,WAR
        # 22: DragoonGauge,  # 龙骑士,DRG
        # 23: BardGauge,  # 吟游诗人,BRD
        # 24: WhiteMageGauge,  # 白魔法师,WHM
        # 25: BlackMageGauge,  # 黑魔法师,BLM
        # 26: ArcanistGauge,  # 秘术师,ACN
        # 27: SummonerGauge,  # 召唤师,SMN
        # 28: ScholarGauge,  # 学者,SCH
        # 30: NinjaGauge,  # 忍者,NIN
        31: Machinist.Machinist.machinist_logic,  # 机工士,MCH
        32: DarkKnight.DarkKnight.dark_knight_logic,  # 暗黑骑士,DRK
        # 33: AstrologianGauge,  # 占星术士,AST
        # 34: SamuraiGauge,  # 武士,SAM
        35: RedMage.RedMage.red_mage_logic,  # 赤魔法师,RDM
        37: Gunbreaker.Gunbreaker.gunbreaker_logic,  # 绝枪战士,GNB
        # 38: DancerGauge,  # 舞者,DNC
    }
