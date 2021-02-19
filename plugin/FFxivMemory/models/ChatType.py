from enum import Enum


class ChatType(Enum):
    none = 0
    Debug = 1
    Urgent = 2
    Notice = 3
    Say = 10
    Shout = 11
    TellOutgoing = 12
    TellIncoming = 13
    Party = 14
    Alliance = 15
    Linkshell1 = 16
    Linkshell2 = 17
    Linkshell3 = 18
    Linkshell4 = 19
    Linkshell5 = 20
    Linkshell6 = 21
    Linkshell7 = 22
    Linkshell8 = 23
    FreeCompany = 24
    NoviceNetwork = 27
    CustomEmote = 28
    StandardEmote = 29
    Yell = 30
    CrossParty = 32
    PvPTeam = 36
    CrossLinkShell1 = 37
    Echo = 56
    SystemError = 58
    SystemMessage = 57
    GatheringSystemMessage = 59
    ErrorMessage = 60
    RetainerSale = 71
    CrossLinkShell2 = 101
    CrossLinkShell3 = 102
    CrossLinkShell4 = 103
    CrossLinkShell5 = 104
    CrossLinkShell6 = 105
    CrossLinkShell7 = 106
    CrossLinkShell8 = 107
