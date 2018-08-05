import re
import time
import logging

#from fetcher import Fetcher
import config
from kill_handler import KillHandler

logging.basicConfig(level=logging.DEBUG, filename=config.log, format=)

def main():
    killhandler=KillHandler()
    while not killhandler.killed:
        print(1)
        time.sleep(0.5)

if __name__ == "__main__":
    main()
