import subprocess
import pymem
import sys
import os
from json import dumps
print(sys.version)

#n=subprocess.Popen("notepad.exe")
pm = pymem.Pymem('ffxiv_dx11.exe')
pm.inject_python_interpreter()

wdir = os.path.abspath('.')

log_path = os.path.join(wdir, 'out.log').replace("\\", "\\\\")
err_path = os.path.join(wdir, 'err.log').replace("\\", "\\\\")

shellcode1 = """
import sys
from os import chdir
from traceback import format_exc
sys.path=%s
chdir(sys.path[0])
try:
    exec(open("%s").read())
    sys.modules.clear()
except:
    with open("%s", "w+") as f:
        f.write(format_exc())
""" % (
    dumps(sys.path).replace("\\", "\\\\"),
    'Main.py',
    'err.log',
)
pm.inject_python_shellcode(shellcode1)
#n.kill()
