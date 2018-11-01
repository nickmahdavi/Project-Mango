#!/usr/bin/env python3
import time
import os
import sys
import logging
import re
import importlib
import pandas as pd
import asyncio

import praw
import prawcore

import logger
import config
from dataframe import DataFrame

logging.basicConfig(format='main.py | %(asctime)s.%(msecs)03d %(levelname)s' +
                           'ln %(lineno)d: %(message)s',
                    level=logging.INFO,
                    filename=config.log, datefmt='%Y-%m-%d %H:%M:%S')


def error(log_to=config.do_log, level='error'):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    tb = (f'{fname}: {exc_type.__name__} (line {exc_tb.tb_lineno}):' +
          f'\"{exc_obj}\"')
    if log_to:
        exec('logging.' + level + '(tb)')


class Fetcher:
    def fetch(self, dry_run=False):
            try:
                for p in s.stream.submissions():
                            self.row = {}
                            self.row['id'] = p.id
                            self.row['title'] = p.id
                            self.row['score'] = p.score
                            self.row['title'] = p.title
                            self.row['selftext'] = p.selftext

                        except Exception as e:
                            logging.error(e)
                            self.data = None

                        finally:
                            if self.fetches > 100:
                                self.data.append(self.row)
                                time.sleep(60/config.rpm)
                            self.fetches += 1
                    else:
                        try:
                            if not dry_run:
                                logger.write(self.data)
                            logging.info('Received kill signal '
                                         f'{handler.lastSignal}, '
                                         'exited gracefully')
                            break
                        except Exception as e:
                            logging.critical("A fatal error occured!")
                            error()
                            break


async def main():
    with open(config.log, 'a') as writefile:
        writefile.write(f'----- main.py: {time.strftime("%Y-%m-%d %H:%M:%S")}'
                        'on {sys.platform}, pid {os.getpid()} -----\n')
        writefile.write(f'----- Reading from {config.subreddit}; '
                        'for more inforation see config.py. -----\n')

    attr = ['id', 'score', 'num_comments', 'title', 'selftext']
    logging.info('Setting up Reddit credentials')

    r = praw.Reddit(client_id=config.client_id,
                    client_secret=config.client_secret,
                    password=config.password,
                    username=config.username,
                    user_agent=config.user_agent)
    s = r.subreddit(config.subreddit)

    df = pd.DataFrame(attr)
    handler = logger.Handler()
    logger = logger.Logger()

    while not handler.killed:  # Dry run?
        try:
            if config.maintenance:
                logging.info('MAINTENANCE MODE ENABLED. WAITING TO' +
                             'FETCH FROM REDDIT.')

                while True:
                    importlib.reload(config)
                    if not config.maintenance:
                        break
                    time.sleep(1)

                logging.info('EXITING MAINTENANCE MODE.')

            if next(s.new(limit=1)) in df.df or \
               next(s.new(limit=1)).stickied or \
               next(s.new(limit=1)).locked:
                pass
            else:
                for post in s.new():
                    if post:  # is in dataframe:
                        break
                    else:
                        row = dict((el, []) for el in attr)
                        for a in attr:
                            row[a].append [getattr(post, a)]  # List for PD

            if handler.killed:
                logging.info(f'Received kill signal {handler.lastSignal},' +
                             'exiting')
                break
    
            rem = int(reddit.auth.limits['remaining'])
            res = int(reddit.auth.limits['reset_timestamp'] - time.time())
            logging.info(f"API calls remaining: {rem:3d}, resetting in {res:3d}s")


        except prawcore.exceptions.RequestException as e_connection:
            if "Max retries exceeded" in e_connection:
                logging.error('Could not establish connection to Reddit.' +
                              'Check your internet connection or' +
                              'string parsing. Waiting...')

        except prawcore.exceptions.OAuthException as e_creds:
            error(level='critical')
            logging.critical('Invalid credentials. Bailing out...')
            exit()

        except Exception as e:
            logging.error(f'An error occured! {e}')
            error()
            time.sleep(5)

        finally:
            importlib.reload(config)

        time.sleep(config.rpm/60)

if __name__ == "__main__":
    if config.pre_wipe:
        open(config.data, 'w').close()
        open(config.log, 'w').close()

    main()
