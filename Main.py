from FFxivPythonTrigger import FFxivPythonTrigger
from plugin.FFxivMemory import FFxivMemory
from plugin.GayMagician import GayMagicianPlugin
from plugin.CutsceneSkipper import CutsceneSkipper
from plugin.SuperJump import SuperJump
from plugin.Command import Command
from plugin.Zoom import ZoomPlugin
from plugin.Teleporter import Teleporter
from plugin.NamazuServer import NamazuServer
from plugin.AutoCombo import AutoCombo
from plugin.WebChat import WebChat
from plugin.PosLocker import PosLocker
from plugin.LogHookFix import LogHookFix
import logging
import sys
import asyncio

if sys.platform == "win32" and sys.version_info >= (3, 8, 0):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

fpt = FFxivPythonTrigger([
    FFxivMemory,
    LogHookFix,
    GayMagicianPlugin,
    WebChat,
    NamazuServer,
    Command,
    CutsceneSkipper,
    SuperJump,
    ZoomPlugin,
    Teleporter,
    AutoCombo,
    PosLocker,
])
fpt.logger.print_level = logging.DEBUG
fpt.start()
exit()
