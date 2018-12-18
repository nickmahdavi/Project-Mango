#!/usr/bin/env python3
import time
import os
import sys
import logging

import praw
import prawcore
import pandas as pd

from stopwatch import Stopwatch
from handler import Handler
import config


p_attr = config.ATTR
s_attr = config.S_ATTR
attr = p_attr + s_attr + ['time_now']

FORMAT = '%(filename)s | %(asctime)s.%(msecs)03d %(levelname)s @ %(lineno)d: %(message)s'
DATEFMT = '%Y-%m-%d %H:%M:%S'

logger = logging.getLogger(__name__)
handler = logging.FileHandler(config.LOGFILE)
formatter = logging.Formatter(FORMAT, datefmt=DATEFMT)
logger.setLevel('INFO')
handler.setLevel('INFO')
handler.setFormatter(formatter)
logger.addHandler(handler)


def get_error():
    global e_type, e_obj, e_tb, tb
    e_type, e_obj, e_tb = sys.exc_info()
    tb = (f'{e_type.__name__} @ {e_tb.tb_lineno}: \"{e_obj}\"')

    return tb


def auth():
    r = praw.Reddit(client_id=config.CLIENT_ID,
                    client_secret=config.CLIENT_SECRET,
                    password=config.PASSWORD,
                    username=config.USERNAME,
                    user_agent=config.USER_AGENT)
    s = r.subreddit(config.SUBREDDIT)

    return r, s


def main():
    logger.info(f'-- {time.strftime("%Y-%m-%d %H:%M:%S")} on {sys.platform}, pid {os.getpid()}')
    logger.info(f'-- Reading from {config.SUBREDDIT}; for more inforation see config.py.')

    r, s = auth()

    df = pd.DataFrame(columns=attr)
    handler = Handler()

    def kill_check():
        if handler.killed:
            logger.info(f'Received kill signal {handler.lastSignal} (code {handler.lastSignum})')
            if not config.DRY_RUN:
                logger.info('Writing dataframe to .CSV')
                try:
                    df.drop_duplicates(subset=['id', 'ups', 'downs'], inplace=True)
                    df.to_csv(config.DATAFILE, index=False)
                except Exception:
                    logger.warning(get_error())
                    logger.warning('Failed to write to CSV.')
                else:
                    logger.info('Successfully wrote dataframe.')
            logger.info('Exited.')

            return True

    retries = 0

    while not handler.killed:
        try:
            if retries:
                logger.info('Attempting to retry...')

            row = row_new = dict((a, []) for a in attr)

            values = df.drop_duplicates(subset=['id'])

            # There are better ways of doing this entire block
            for post_id in values['id'].values:
                if (time.time() - values.loc[values['id'] == post_id]['created_utc']) > config.POST_DROP_AFTER:
                    continue
                post = r.submission(post_id)
                for _a in p_attr:
                    row[_a].append(getattr(post, _a))
                for _s in s_attr:
                    row[_s].append(getattr(s, _s))
                row['time_now'].append(time.time())

            for post in s.new(limit=config.POST_GET_LIMIT):
                if post.id in values['id'].values:
                    break
                for _a in p_attr:
                    row_new[_a].append(getattr(post, _a))
                for _s in s_attr:
                    row_new[_s].append(getattr(s, _s))
                row_new['time_now'].append(time.time())

            df = df.append(pd.DataFrame(row_new, columns=attr), ignore_index=True)
            df = df.append(pd.DataFrame(row, columns=attr), ignore_index=True)
            df.drop_duplicates(subset=['id', 'ups', 'downs'], inplace=True)
            df.to_csv(config.DATAFILE, index=False)

        except prawcore.exceptions.RequestException:  # You most likely do not need this
            retries += 1
            if retries < len(config.TIMEOUTS):
                logger.warning(f'Could not establish connection. Waiting for {config.TIMEOUTS[retries-1]} sec...')
                time.sleep(config.TIMEOUTS[retries-1])
            else:
                logger.critical('Max retries exceeded. Exiting.')
                break

        except Exception:  # Or this
            logger.error(get_error())
            exit()

        else:
            if retries:
                logger.info('Connection reestablished')
                retries = 0
            logger.info(f'Currently {len(df.index)} entries in dataframe, {len(df.drop_duplicates(subset=["id"]).index)} unique')

        finally:
            rem = r.auth.limits['remaining']
            res = r.auth.limits['reset_timestamp'] - time.time()
            if rem > 5:
                logger.info(f'{rem:.0f} calls remaining, {res:.0f} till next reset')
                for _ in range(config.TIMEOUT_SECS):
                    time.sleep(1)
                    if kill_check():
                        break
            else:
                logger.warning('Out of calls! Waiting...')
                for _ in range(int(res) + 1):
                    time.sleep(1)
                    if kill_check():
                        break

            # No, you do not have to 'if handler.killed: break', it's a while loop

if __name__ == "__main__":
    main()
