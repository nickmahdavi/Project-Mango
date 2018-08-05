import signal
import logging
import config

#config.config()
logging.basicConfig(level=logging.DEBUG, filename=config.log, format='%(asctime) %(filename)-8s %(filename) %(message)s:')
logger=logging.getLogger(__name__)


sig={1:'SIGHUP', 2:'SIGINT', 15:'SIGTERM', 17:'SIGCHLD', 19:'SIGSTOP',
     30:'SIGPWR'}

# Handles SIGTERM (15)
class KillHandler():
    def __init__(self):
        self.killed = False
        signal.signal(signal.SIGTERM, self.kill)
        signal.signal(signal.SIGINT, self.kill)
        
    def kill(self, signum, frame):
        self.killed = True
        try:
            logger.info(f"{__file__} received {sig[signum]}")
        except KeyError:
            logger.info(f"{__file__} received an abnormal signal")
            logger.info(f"{__file__} received {signum}")
