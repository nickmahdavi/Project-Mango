#!/usr/bin/env python3
import re
import time
import logging
import os
import sys

import pandas as pd
import praw

import error
from error import Handler, Logger
import config

r=praw.Reddit(client_id=config.client_id,
              client_secret=config.client_secret,
              password=config.password,
              username=config.username,
              user_agent=config.user_agent
              )
s=r.subreddit(config.subreddit)

class Fetcher:
    def __init__(self):
        self.data = pd.DataFrame()
    def __call__(self, dry_run = False):
        self.fetch(dry_run)    
    def fetch(self, dry_run):
        for p in s.stream.submissions():
            if not handler.killed:
                print (f"Fetching new {self.fetches}")
                try:
                    self.row={}
                    self.row['id'] = p.id
                    self.row['title'] = p.id
                    self.data['score'] = p.score
                    self.data['title'] = p.title
                    if p.is_self:
                        self.data[self.fetches - 1]["self"] = True
                        self.data[self.fetches - 1]["selftext"] = p.selftext
                    else:
                        self.data[self.fetches - 1]["self"] = False
                        
                except Exception:
                    logger.error()
                    self.data[self.fetches - 1]["error"] = logger.mark()
                finally:
                    self.fetches+=1
                    time.sleep(1)
            else:
                try:
                    if not dry_run:
                        logger.write(self.data)
                    sys.exit(f"Received kill signal {handler.lastSignal}, exited gracefully")
                except Exception as e:
                    print("The following fatal error occured while shutting down:")
                    error.log()

def main():
    if "wipe" in sys.argv:
        open(config.data, 'w').close()
    if "dry" in sys.argv:
        fetcher(True)
    elif "none" not in sys.argv:
        fetcher()
    else:
        sys.exit()
        
        
if __name__ == "__main__":
    handler=Handler()
    logger=Logger()
    fetcher=Fetcher()
    main()
