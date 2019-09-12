#!/usr/bin/env python3
import time
import os
import sys
import logging
from logging.handlers import RotatingFileHandler

import praw
import prawcore
import pandas as pd

from stopwatch import Stopwatch
from handler import Handler
import config


attr = config.ATTR + config.S_ATTR + ['time_now'] + ['pickup_no'] + ['post_pickup']
p_attr = config.ATTR
s_attr = config.S_ATTR

FORMAT = '%(filename)s | %(asctime)s.%(msecs)03d %(levelname)s @ %(lineno)d: %(message)s'
DATEFMT = '%Y-%m-%d %H:%M:%S'

logger = logging.getLogger(__name__)
handler = RotatingFileHandler(config.LOGFILE, mode="a", maxBytes=1024**3)
formatter = logging.Formatter(FORMAT, datefmt=DATEFMT)
logger.setLevel(config.LOG_LEVEL)
handler.setLevel(config.LOG_LEVEL)
handler.setFormatter(formatter)
logger.addHandler(handler)


def get_error():
    global e_type, e_obj, e_tb, tb
    e_type, e_obj, e_tb = sys.exc_info()
    tb = (f'{e_type.__name__} @ {e_tb.tb_lineno}: \"{e_obj}\"')

    return tb


def auth():
    reddit = praw.Reddit(client_id=config.CLIENT_ID,
                    client_secret=config.CLIENT_SECRET,
                    password=config.PASSWORD,
                    username=config.USERNAME,
                    user_agent=config.USER_AGENT)

    return reddit


def main():
    r = auth()
    s = r.subreddit(config.SUBREDDIT)

    df = pd.DataFrame(columns=attr)
    df_old = pd.DataFrame(columns=attr)
    handler = Handler()
    stopwatch = Stopwatch()

    def kill_check():
        if handler.killed:
            logger.info(f"Received kill signal {handler.lastSignal} (code {handler.lastSignum})")
            if not config.DRY_RUN:
                logger.info("Writing dataframe to .CSV")
                try:
                    # df.drop(['pickup_no'], axis=1).to_csv(config.DATAFILE, index=False)
                    df.to_csv(config.DATAFILE, index=False)
                except Exception:
                    logger.warning(get_error())
                    logger.warning("Failed to write to CSV.")
                else:
                    logger.info("Successfully wrote dataframe.")
            logger.info("Exited.")

            return True

        else:
            return False

    retries = 0

    while not handler.killed:
        try:
            if retries:
                logger.info(f"Attempting to retry, attempt {retries}...")

            values = df.sort_values('pickup_no', ascending=False).drop_duplicates(subset=['id']).sort_index().reset_index(drop=True)

            row = dict((a, []) for a in attr)

            # There are better ways of doing this entire block. Also it might be slow
            for post_id in values['id'].values:
                stopwatch.reset()

                match_row = values.loc[values['id'] == post_id]
                iteration = match_row['pickup_no'].iloc[0]
                waited = time.time() - match_row['post_pickup'].iloc[0]

                try:
                    time_wait = config.POST_PICKUPS[iteration]
                    logger.debug(f"{post_id}: {waited} / {time_wait} secs,  {iteration} / {len(config.POST_PICKUPS)}")

                except IndexError:
                    logger.info(f"Hit final iteration of {post_id} @ {len(df.loc[df['id'] == post_id])}x " \
                                 "(should be 18), dropping")
                    df_old = pd.concat(df_old, df.loc[df['id'] == post_id])
                    df.drop(df.loc[df['id'] == post_id].index, inplace=True)
                    continue

                if waited < time_wait:
                    continue

                logger.debug("Post has passed threshold")

                post = r.submission(post_id)
                for _a in p_attr:
                    row[_a].append(getattr(post, _a))
                for _s in s_attr:
                    row[_s].append(getattr(s, _s))
                row['pickup_no'].append(iteration + 1)
                row['post_pickup'].append(match_row['post_pickup'].iloc[0])
                row['time_now'].append(time.time())

                # MAGIC NUMBER 2.5: don't know just threw it in there
                # it's a good estimate for how long it should take to get a post
                if stopwatch.mark() > 2.5 * len(values.index):
                    logger.warning(f'Warning: Slow iteration, {stopwatch.mark()} secs for {len(values.index)} items')

            row_new = dict((a, []) for a in attr)

            for post in s.new(limit=config.POST_GET_LIMIT):
                if (post.id in df['id'].values) or (post.id in df_old['id'].values):
                    logger.debug(f"{post.id} is a duplicate, continuing")
                    continue

                logger.debug(f"Picked up {post.id}")

                for _a in p_attr:
                    row_new[_a].append(getattr(post, _a))
                for _s in s_attr:
                    row_new[_s].append(getattr(s, _s))
                row_new['pickup_no'].append(0)
                row_new['post_pickup'].append(time.time())
                row_new['time_now'].append(time.time())

            logger.debug(f"Old {len(row['id'])} / new {len(row_new['id'])}")

            df_new = pd.DataFrame(row_new, columns=attr)
            df_update = pd.DataFrame(row, columns=attr)

            modified = False if df.equals(df.append(df_new)) and df.equals(df.append(df_update)) else True

            df = pd.concat([df, df_new, df_update], ignore_index=True)
            if not config.DRY_RUN:
                # df.drop(['pickup_no'], axis=1).to_csv(config.DATAFILE, index=False)
                df.to_csv(config.DATAFILE, index=False)

            logger.debug(len(df.index))

            del row, row_new
            del df_new, df_update

        except prawcore.exceptions.RequestException:  # You most likely do not need this
            retries += 1
            if retries < len(config.TIMEOUTS):
                logger.warning(f'Connection lost. Waiting for {config.TIMEOUTS[retries-1]} sec...')
                time.sleep(config.TIMEOUTS[retries-1])
            else:
                logger.critical('Max retries exceeded. Exiting.')
                break

        except Exception:  # Or this
            logger.error(get_error())
            time.sleep(10)

        else:
            if retries:
                logger.info("Connection reestablished")
                retries = 0

            if modified:
                logger.info(f"{len(df.index)} entries, {len(df.drop_duplicates(subset=['id']).index)} unique")

        finally:
            logger.debug(f'{len(values)} unique values')

            rem = r.auth.limits['remaining']
            res = r.auth.limits['reset_timestamp'] - time.time()
            if rem < 5:
                logger.warning('Out of calls! Waiting...')
                for _ in range(int(res + 1)):
                    time.sleep(1)
                    if kill_check():
                        killed = True
                    else:
                        killed = False

                if (res - config.TIMEOUT_SECS) > 0 and not killed:
                    for _ in range(int(res - config.TIMEOUT_SECS)):
                        time.sleep(1)
                        if kill_check():
                            break
            else:
                if modified:
                    logger.info(f"{rem:.0f} calls remaining, {res:.0f} till next reset")
                    logger.info(f"-- {time.strftime('%Y-%m-%d %H:%M:%S')} on {sys.platform}, pid {os.getpid()}")
                    logger.info(f"-- Reading from {config.SUBREDDIT}; for more inforation see config.py.\n")
                for _ in range(config.TIMEOUT_SECS):
                    time.sleep(1)
                    if kill_check():
                        break

            # No, you do not have to 'if handler.killed: break', it's a while loop, nick

if __name__ == "__main__":
    main()
