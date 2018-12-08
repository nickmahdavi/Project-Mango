#!/usr/bin/env python3
import time
import os
import sys
import logging

import praw
import prawcore

from handler import Handler
from stopwatch import Stopwatch
from dataframe import DataFrame
import config


attr = config.ATTR
s_attr = config.S_ATTR

FORMAT = '%(filename)s | %(asctime)s.%(msecs)03d %(levelname)s @ %(lineno)d: %(message)s'
DATEFMT = '%Y-%m-%d %H:%M:%S'

logger = logging.getLogger(__name__)
handler = logging.FileHandler(config.log)
formatter = logging.Formatter(FORMAT, datefmt=DATEFMT)
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
    s = r.subreddit(config.subreddit)

    return r, s


def main():
    if config.PRE_WIPE:
        open(config.log, 'w').close()
        open(config.data, 'w').close()

    logger.info(f' -- {time.strftime("%Y-%m-%d %H:%M:%S")} on {sys.platform}, pid {os.getpid()}')
    logger.info(f' -- Reading from {config.subreddit}; for more inforation see config.py.')

    r, s = auth()

    df = DataFrame(attr + s_attr + ['time_now'])
    handler = Handler()
    stopwatch = Stopwatch()

    if open(config.log).read().strip('\n'):
        col = DataFrame(attr + s_attr + ['time_now'])
        logger.info('Writing columns')
        col.write()

    while True:
        try:
            s._fetch()
            break
        except (prawcore.exceptions.NotFound, prawcore.exceptions.BadRequest):
            logging.critical('Bad subreddit name. Exiting.')
            exit()
        except prawcore.exceptions.Redirect:
            logging.critical('Subreddit does not exist. Exiting.')
            exit()
        except prawcore.exceptions.RequestException:
            logging.error('Connection lost, exiting.')
            exit()

    retries = 0
 
    while not handler.killed:
        try:
            if retries:
                logger.info('Attempting to retry...')

            stopwatch.reset()            

            row, row_new = dict((el, []) for el in attr + s_attr + ['time_now'])

            for post_id in df.isolate(['id'])['id']:
                post = r.submission(post_id)
                for _a in attr:
                    row[_a].append(getattr(post, _a))
                for _s in s_attr:
                    row[_s].append(getattr(s, _s))
                row['time_now'].append(time.time())

            for post in s.new(limit=config.POST_GET_LIMIT):
                for _a in attr:
                    row_new[_a].append(getattr(post, _a))
                for _s in s_attr:
                    row_new[_s].append(getattr(s, _s))
                row_new['time_now'].append(time.time())

            df.append(row)
            df.append(row_new)

            df.isolate(['id', 'ups', 'downs'], True)
            df.write()

        except prawcore.exceptions.RequestException:
            retries += 1
            if retries < len(config.TIMEOUTS):
                logger.warning(f'Could not establish connection. Waiting for {config.TIMEOUTS[retries-1]} sec...')
                time.sleep(config.TIMEOUTS[retries-1])
            else:
                logger.critical('Max retries exceeded. Exiting.')
                break

        except prawcore.exceptions.OAuthException:
            logger.critical(get_error())
            logger.critical('Invalid credentials. Exiting.')
            break

        except Exception:
            logger.error(get_error())
            time.sleep(5)

        else:
            if retries:
                logger.info('Connection reestablished')
                retries = 0
            
            rem = r.auth.limits['remaining']
            res = r.auth.limits['reset_timestamp'] - time.time()

            logging.info(f'Took {stopwatch.mark()} sec')
            logger.info(f'{rem:.0f} calls remaining, {res:.0f} till next reset')
            logger.info(f'Currently {len(df.df.index)} entries in dataframe, {len(df.isolate("id").index)} unique')

        finally:
            for _ in range((len(df.isolate("id").index) + config.POST_GET_LIMIT) * 2):
                time.sleep(1)

                if handler.killed:
                    logger.info(f'Received kill signal {handler.lastSignal} (code {handler.lastSignum})')
                    if not config.DRY_RUN:
                        logger.info('Writing dataframe to .CSV')
                        try:
                            df.isolate(['id', 'ups', 'downs'], True)
                            df.write()
                        except Exception:
                            logger.warning(get_error())
                            logger.warning('Failed to write to CSV.')
                        else:
                            logger.info('Successfully wrote dataframe.')
                    logger.info('Exited.')
                    break


if __name__ == "__main__":
    main()
