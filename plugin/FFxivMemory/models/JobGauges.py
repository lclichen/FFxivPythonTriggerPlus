from .MemoryParseObject import get_memory_class, get_memory_array
from enum import Enum


def byte_get_bit(byte: int, start: int, length: int):
    return (1 << length) - 1 & byte >> start


RedMageGauge = get_memory_class({
    'white_mana': ('byte', 0),
    'black_mana': ('byte', 1),
})
WarriorGauge = get_memory_class({
    'beast': ('byte', 0)
})
GunbreakerGauge = get_memory_class({
    'cartridges': ('byte', 0),
    'continuationMilliseconds': ('ushort', 2),  # Is 15000 if and only if continuationState is not zero.
    'continuationState': ('byte', 4)
})
DarkKnightGauge = get_memory_class({
    'blood': ('byte', 0),
    'darksideMilliseconds': ('ushort', 2),
})
PaladinGauge = get_memory_class({
    'oath': ('byte', 0),
})


class BardGauge(get_memory_class({
    'songMilliseconds': ('ushort', 0),
    'songProcs': ('byte', 2),
    'soulGauge': ('byte', 3),
    'songType': ('byte', 4)
})):
    class Song(Enum):
        none = 0
        ballad = 5  # Mage's Ballad.
        paeon = 10  # Army's Paeon.
        minuet = 15  # The Wanderer's Minuet.


class DancerGauge(get_memory_class({
    'feathers': ('byte', 0),
    'step': (get_memory_array('byte', 1, 4, 0), 2),
    'currentStep': ('byte', 6)
})):
    class Step(Enum):
        none = 0
        emboite = 1
        entrechat = 2
        jete = 3
        pirouette = 4


class DragoonGauge(get_memory_class({
    'blood_or_life_ms': ('ushort', 0),
    'stance': ('byte', 2),  # 0 = None, 1 = Blood, 2 = Life
    'eyesAmount': ('byte', 3),
})):
    @property
    def bloodMilliseconds(self):
        return self.blood_or_life_ms if self.stance == 1 else 0

    @property
    def lifeMilliseconds(self):
        return self.blood_or_life_ms if self.stance == 2 else 0


NinjaGauge = get_memory_class({
    'hutonMilliseconds': ('uint', 0),
    'ninkiAmount': ('byte', 4),
    'hutonCount': ('byte', 5),
})

ThaumaturgeGauge = get_memory_class({
    'umbralMilliseconds': ('ushort', 2),  # Number of ms left in umbral fire/ice.
    'umbralStacks': ('sbyte', 4),  # Positive = Umbral Fire Stacks, Negative = Umbral Ice Stacks.
})


class BlackMageGauge(get_memory_class({
    'nextPolyglotMilliseconds': ('ushort', 0),
    'umbralMilliseconds': ('ushort', 2),
    'umbralStacks': ('sbyte', 4),
    'umbralHearts': ('byte', 5),
    'foulCount': ('byte', 6),
    'enochain_state': ('byte', 7),
})):
    @property
    def enochain_active(self):
        return byte_get_bit(self.enochain_state, 0, 1)

    @property
    def polygot_active(self):
        return byte_get_bit(self.enochain_state, 1, 1)


WhiteMageGauge = get_memory_class({
    'lilyMilliseconds': ('ushort', 2),
    'lilyStacks': ('byte', 4),
    'bloodlilyStacks': ('byte', 5),
})

ArcanistGauge = get_memory_class({
    'aetherflowStacks': ('byte', 4),
})


class SummonerGauge(get_memory_class({
    'stanceMilliseconds': ('ushort', 0),
    'bahamutStance': ('byte', 2),
    'bahamutSummoned': ('byte', 3),
    'stacks': ('byte', 3),
})):
    @property
    def aetherflowStacks(self):
        return byte_get_bit(self.stacks, 0, 2)

    @property
    def dreadwyrmStacks(self):
        return byte_get_bit(self.stacks, 2, 2)

    @property
    def phoenixReady(self):
        return byte_get_bit(self.stacks, 4, 1)


ScholarGauge = get_memory_class({
    'aetherflowStacks': ('byte', 2),
    'fairyGauge': ('byte', 3),
    'fairyMilliseconds': ('ushort', 4),  # Seraph time left ms.
    'fairyStatus': ('byte', 6)
    # Varies depending on which fairy was summoned, during Seraph/Dissipation: 6 - Eos, 7 - Selene, else 0.
})

PuglistGauge = get_memory_class({
    'lightningMilliseconds': ('ushort', 0),
    'lightningStacks': ('byte', 2),
})
MonkGauge = get_memory_class({
    'lightningMilliseconds': ('ushort', 0),
    'lightningStacks': ('byte', 2),
    'chakraStacks': ('byte', 3),
})
MachinistGauge = get_memory_class({
    'overheatMilliseconds': ('ushort', 0),
    'batteryMilliseconds': ('ushort', 2),
    'heat': ('byte', 4),
    'battery': ('byte', 5)
})


class AstrologianGauge(get_memory_class({
    'heldCard': ('byte', 4),
    'arcanums': (get_memory_array('byte', 1, 3), 5),
})):
    class Card(Enum):
        none = 0
        balance = 1
        bole = 2
        arrow = 3
        spear = 4
        ewer = 5
        spire = 6

    class Arcanum(Enum):
        none = 0
        solar = 1
        lunar = 2
        celestial = 3


class SamuraiGauge(get_memory_class({
    'kenki': ('byte', 4),
    'sen_bits': ('byte', 5)
})):
    @property
    def snow(self):
        return (self.sen_bits & 1) != 0

    @property
    def moon(self):
        return (self.sen_bits & 2) != 0

    @property
    def flower(self):
        return (self.sen_bits & 4) != 0
