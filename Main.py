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
import logging


fpt = FFxivPythonTrigger([
    FFxivMemory,
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
# fpt.logger.print_level=logging.DEBUG
fpt.start()
