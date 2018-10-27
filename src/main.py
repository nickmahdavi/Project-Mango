#!/usr/bin/env python3
import time
import os
import sys
import logging
import re
import importlib

import praw
import prawcore

import logger
import config

logging.basicConfig(format='main.py | %(asctime)s.%(msecs)03d %(levelname)s | ln %(lineno)d: %(message)s', level=logging.INFO, filename=config.log, datefmt='%Y-%m-%d %H:%M:%S')


r=praw.Reddit(client_id=config.client_id,
          client_secret=config.client_secret,
          password=config.password,
          username=config.username,
          user_agent=config.user_agent
          )

s=r.subreddit(config.subreddit)


def error(log_to=config.do_log, level='error'):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    tb = f"{fname}: {exc_type.__name__} (line {exc_tb.tb_lineno}): \"{exc_obj}\""
    if log_to:
        exec('logging.' + level + '(tb)')
        
class Fetcher:
    def __init__(self):
        self.data = []
        self.fetches = 1
    def __call__(self):
        if config.dry_run:
            self.fetch(True)
        else:
            self.fetch()
        
    def fetch(self, dry_run=False):
            try:
                for p in s.stream.submissions():
                    importlib.reload(config)
                    if not handler.killed:
                        if config.maintenance:
                            with open(config.log) as file:
                                if not re.search('ENTERING MAINTENENCE', [line.rstrip('\n') for line in file][-1]):
                                    logging.info("ENTERING MAINTENENCE MODE. NEW POSTS WILL NOT BE PROCESSED AND CHANGES WILL NOT TAKE PLACE.")
                            continue
                        if self.fetches == 1:
                            logging.info(f"Fetching and ignoring first 100 replies")
                        elif self.fetches > 100:
                            logging.info(f"Fetching new {self.fetches}")
                        try:
                            if not p.is_self:
                                continue
                            self.row = {}
                            self.row['id'] = p.id
                            self.row['title'] = p.id
                            self.row['score'] = p.score
                            self.row['title'] = p.title
                            self.row["selftext"] = p.selftext

                        except Exception as e:
                            logging.error(e)
                            self.data = None

                        finally:
                            if self.fetches > 100:
                                self.data.append(self.row)
                                time.sleep(60/config.rpm)
                            self.fetches+=1
                    else:
                        try:
                            if not dry_run:
                                logger.write(self.data)
                            logging.info(f"Received kill signal {handler.lastSignal}, exited gracefully")
                            break
                        except Exception as e:
                            logger.critical("A fatal error occured!")
                            error()
                            break
            except Exception as e:
                logging.critical("Error occured!")
                error(level='critical')
                logging.critical("Exiting...")
                exit()
    

if __name__ == "__main__":
    if config.pre_wipe:
        open(config.data, 'w').close()
        open(config.log, 'w').close()
        
    handler = logger.Handler()
    logger = logger.Logger()
    fetcher = Fetcher()
    
    with open(config.log, 'a') as writefile:
        writefile.write(f'------ main.py: {time.strftime("%Y-%m-%d %H:%M:%S")} on {sys.platform}, pid {os.getpid()} ------\n')
        writefile.write(f'------ Reading from {config.subreddit}; for more inforation see config.py. ------\n')
    fetcher()
