#TEMPORARY
import os
import sys
   
sys.path.insert(0, '/Users/nicmahd/Desktop/')

import praw
import config
import error

r=praw.Reddit(client_id=config.client_id,
              client_secret=config.client_secret,
              password=config.password,
              username=config.username,
              user_agent=config.user_agent
              )
s=r.subreddit(config.subreddit)

class Fetcher:
    def __init__(self):
        self.data = []
        self.fetches = 0
        logger=Logger()
    def __call__(self, quick_run = False):
        fetch(quick_run)    
    def fetch(self, quick_run):
        self.fetches += 1
        try:
            for post in s.new:
                if not post in self.data:
                    pass
        except Exception:
            log()
