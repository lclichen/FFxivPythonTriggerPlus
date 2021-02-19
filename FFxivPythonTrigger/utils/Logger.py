import logging
from datetime import datetime
# import inspect
import os
import time
import traceback
import asyncio

log_format = "[{lv}]\t[{time}|{name}]\t{msg}"
time_format = "%H:%M:%S"
log_file_format = 'log_{int_time}.txt'

loop = asyncio.get_event_loop()
a_lock = asyncio.Lock()


class Logger(object):
    def __init__(self, log_path: str = None, default_print_level: int = None):
        self.buffer = list()
        if log_path is None:
            self.log_path = None
        else:
            fn = log_file_format.format(int_time=int(time.time()))
            self.log_path = os.path.join(log_path, fn)
        self.print_level = logging.INFO if default_print_level is None else default_print_level
        self.recalls = set()

    def get_buffer(self, size: int = 50):
        return self.buffer[-size:]

    async def async_log(self, name: str, msg: str, level: int = None):
        if level is None:
            level = logging.INFO
        msg_log = Log(name, msg, level)
        with await a_lock:
            self.buffer.append(msg_log)
            if level >= self.print_level:
                print(msg_log)
            if self.log_path is not None:
                with open(self.log_path, 'a+') as fo:
                    fo.write(msg_log)
                    fo.write('\n')
        for recall in self.recalls:
            try:
                recall(msg_log)
            except:
                self.recalls.remove(recall)
                emsg = 'Error occur in log recall %s:\n%s' % (recall, traceback.format_exc())
                self.log('Logger', emsg, logging.ERROR)

    def log(self, name: str, msg: str, level: int = None):
        # print(Log(name, msg, level))
        loop.create_task(self.async_log(name, msg, level))


class Log(object):
    def __init__(self, name: str, msg: str, lv: int):
        self.time = datetime.now()
        self.msg = msg
        self.name = name
        self.lv = lv
        # self.module = inspect.getmodule(inspect.stack()[2][0]).__name__

    def __str__(self):
        return log_format.format(
            time=self.time.strftime(time_format),
            name=self.name,
            msg=self.msg,
            lv=logging.getLevelName(self.lv),
            # module=self.module
        )

    def __dict__(self):
        return {
            'time': self.time.strftime(time_format),
            'name': self.name,
            'msg': self.msg,
            'lv': logging.getLevelName(self.lv),
            # 'module': self.module,
        }


def log(msg, lv=0):
    print(msg)
