#import traceback
import sys
import os
import config
import signal

def log(log_to=True):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    tb = f"{fname[1:-1]}: {exc_type.__name__} (line {exc_tb.tb_lineno}): \"{exc_obj}\""
    if log_to:
        log=open(config.log,"w")
        log.write(tb)
        log.close()
    else:
        return tb

class Handler:
    def __init__(self):
        self.killed = self.receivedTermSignal = False
        catchSignals = [
            1,
            2,
            3,
            10,
            12,
            15,
        ]
        for signum in catchSignals:
            signal.signal(signum, self.handler)

    def handler(self, signum, frame):
        self.lastSignal = signum
        self.killed = True
        if signum in [2, 3, 15]:
            self.receivedTermSignal = True
            
class Logger:
    def mark(self):
        log(False)
    def error(self):
        log()
    def log(self, text):
        logfile = open(config.log, "w")
        logfile.write(f"{str(text)}")
        logfile.close()
    def write(self, data):
        writefile = open(config.data, "w")
        writefile.write(f"{str(data)}")
        writefile.close()
