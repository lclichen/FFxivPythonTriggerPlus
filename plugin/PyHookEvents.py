import PyHook3

def OnKeyboardEvent(event):
    print('MessageName:', event.MessageName)
    print('Window:', event.Window)
    print('Key:', event.Key)
    return True

hm = PyHook3.HookManager()
hm.KeyDown = OnKeyboardEvent
hm.KeyUp = OnKeyboardEvent
hm.HookKeyboard()

import pythoncom
pythoncom.PumpMessages()
