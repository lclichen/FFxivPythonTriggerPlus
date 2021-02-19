from .MemoryParseObject import get_memory_lazy_class
from .JobGauges import *
from ..MemoryHandler import MemoryHandler

_Player = get_memory_lazy_class({
    'localContentId': ('ulong', 88),
    'job': ('byte', 106),
    'str': ('uint', 356),
    'dex': ('uint', 360),
    'vit': ('uint', 364),
    'int': ('uint', 368),
    'mnd': ('uint', 372),
    'pie': ('uint', 376),
    'tenacity': ('uint', 428),
    'attack': ('uint', 432),
    'directHit': ('uint', 440),
    'crit': ('uint', 460),
    'attackMagicPotency': ('uint', 484),
    'healMagicPotency': ('uint', 488),
    'det': ('uint', 528),
    'skillSpeed': ('uint', 532),
    'spellSpeed': ('uint', 536),
    'craft': ('uint', 632),
    'control': ('uint', 636),
})

gauges = {
    19: PaladinGauge,  # 骑士,PLD
    20: MonkGauge,  # 武僧,MNK
    21: WarriorGauge,  # 战士,WAR
    22: DragoonGauge,  # 龙骑士,DRG
    23: BardGauge,  # 吟游诗人,BRD
    24: WhiteMageGauge,  # 白魔法师,WHM
    25: BlackMageGauge,  # 黑魔法师,BLM
    26: ArcanistGauge,  # 秘术师,ACN
    27: SummonerGauge,  # 召唤师,SMN
    28: ScholarGauge,  # 学者,SCH
    30: NinjaGauge,  # 忍者,NIN
    31: MachinistGauge,  # 机工士,MCH
    32: DarkKnightGauge,  # 暗黑骑士,DRK
    33: AstrologianGauge,  # 占星术士,AST
    34: SamuraiGauge,  # 武士,SAM
    35: RedMageGauge,  # 赤魔法师,RDM
    37: GunbreakerGauge,  # 绝枪战士,GNB
    38: DancerGauge,  # 舞者,DNC
}


class Player(_Player):
    gauge_addr = None

    def get_gauge(self):
        if self.job in gauges:
            return gauges[self.job](self.handler, self.gauge_addr)
