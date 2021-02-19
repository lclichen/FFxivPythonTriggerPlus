import clr
clr.AddReference('GayMagician')
from GayMagician import GayMagician
gm = GayMagician()
gm.LoadGameProcess()
gm.DoTextCommand("/e 1")
gm.Detach()
