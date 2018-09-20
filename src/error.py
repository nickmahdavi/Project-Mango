import sys
import os
import traceback
import config

def log(log_to=True):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    tb = f"{fname[1:-1]}: {exc_type.__name__} (line {exc_tb.tb_lineno}): \"{exc_obj}\""
    if log_to:
        log=ope n(config.log,"w")
        log.write(tb)
        log.close()
    else:
        return tb

class Logger:
    def log(self, text):
        logfile = open(config.log, "w")
        logfile.write(f"{text}")
        logfile.close
    def write(self, data):
        writefile = open(config.data, "w")
        writefile.write(f"{data}")
        writefile.close()
        
