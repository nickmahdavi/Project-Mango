#!/usr/bin/env python3
import time, os, sys, logging, importlib

import praw
import prawcore

from handler import Handler
from stopwatch import Stopwatch
from dataframe import DataFrame
import config


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler(config.log)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(filename)s | %(asctime)s.%(msecs)03d %(levelname)s @ %(lineno)d: %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)


def error():
    global e_type, e_obj, e_tb, tb
    e_type, e_obj, e_tb = sys.exc_info()
    tb = (f'{e_type.__name__} @ {e_tb.tb_lineno}: \"{e_obj}\"')


def isempty(file):
    return os.path.isfile(file) and (os.path.getsize(file) == 0)


def auth(id=config.cid,
         secret=config.secret,
         password=config.password,
         username=config.username,
         agent=config.user_agent,
         subreddit=config.subreddit):
    r = praw.Reddit(client_id=id,
                    client_secret=secret,
                    password=password,
                    username=username,
                    user_agent=agent)
    s = r.subreddit(subreddit)

    return r, s


def main():
    if config.pre_wipe:
        open(config.log, 'w').close()

    with open(config.log, 'a') as file:
        if not os.path.getsize(config.log) == 0:
            file.write(('- ' * 37) + '-\n')
        file.close()

    logger.info(f'{time.strftime("%Y-%m-%d %H:%M:%S")} on {sys.platform}, pid {os.getpid()}')
    logger.info(f'Reading from {config.subreddit}; for more inforation see config.py.')

    attr = config.attributes
    sattr = config.sattributes
    xattr = config.xattributes
    timeout = config.timeouts

    r, s = auth()

    retries = 0

    df = DataFrame(attr+sattr+list(xattr.keys()))
    handler = Handler()
    stopwatch = Stopwatch()  # Superfluous and so not implemented

    if os.path.getsize(config.data) < 2:
        col = DataFrame(attr+sattr+list(xattr.keys()))
        logger.info('Writing columns')
        col.write(header=True)

    retries = 0

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
            retries += 1
            if retries < config.max_retries[0]:
                logging.error('Could not establish connection.')
                logging.error(f'Waiting for {config.timeouts[retries][0]} seconds...')
            else:
                logging.critical('Max retries exceeded. Exiting.')
                exit()

    while not handler.killed:  # Dry run?
        if config.maintenance:
                logger.info('MAINTENANCE MODE ENABLED. WAITING TO FETCH FROM REDDIT.')
                while True:
                    importlib.reload(config)
                    if not config.maintenance:
                        break
                if handler.killed:
                    logger.info(f'Received kill signal {handler.lastSignal} (code {handler.lastSignum})')
                    if not config.dry_run:
                        logger.info('Writing dataframe to .CSV')
                        try:
                            df.write()
                        except Exception:
                            logger.log('Failed to write to CSV.')
                    logger.info('Exited successfully.')
                    time.sleep(1)
                logger.info('EXITING MAINTENANCE MODE.')

        try:
            if retries:
                logger.info('Attempting to retry...')

            row = dict((el, []) for el in attr + sattr + list(xattr.keys()))

            for post_id in df.isolate(['id'])['id']:
                post = r.submission(post_id)
                for _a in attr:
                    row[_a].append(getattr(post, _a))
                for _s in sattr:
                    row[_s].append(getattr(s, _s))
                for _x in list(xattr.keys()):
                    row[_x].append(eval(xattr[_x]))

            df.append(row)

            row = dict((el, []) for el in attr + sattr + list(xattr.keys()))
            
            for post in s.new(limit=config.post_get_limit):
                for _a in attr:
                    row[_a].append(getattr(post, _a))
                for _s in sattr:
                    row[_s].append(getattr(s, _s))
                for _x in list(xattr.keys()):
                    row[_x].append(eval(xattr[_x]))

            df.append(row)

            df.isolate(['id', 'ups', 'downs'], True)
            df.write()

        except prawcore.exceptions.RequestException:
            retries += 1
            if retries < 8:
                logger.warning(f'Could not establish connection. Waiting for {timeout[retries][1]} sec...')
                time.sleep(timeout[retries][1])
            else:
                logger.critical('Max retries exceeded. Exiting.')
                break

        except prawcore.exceptions.OAuthException:
            error()
            logger.critical(tb)
            logger.critical('Invalid credentials. Exiting.')
            break

        except Exception:
            error()
            logger.error(tb)
            time.sleep(5)

        else:
            if retries:
                logger.info('Connection reestablished')
                retries = 0
            logger.info(f'Currently {len(df.df.index)} entries in dataframe, {len(df.isolate("id").index)} unique')

        finally:
            if handler.killed:
                logger.info(f'Received kill signal {handler.lastSignal} (code {handler.lastSignum})')
                if not config.dry_run:
                    logger.info('Writing dataframe to .CSV')
                    try:
                        df.isolate(['id', 'ups', 'downs'], True)
                        df.write()
                    except Exception:
                        error()
                        logger.warning('Failed to write to CSV.')
                        logger.warning(tb)
                    else:
                        logger.info('Successfully wrote dataframe.')
                logger.info('Exited.')
                break
            
            rem = r.auth.limits['remaining']
            res = r.auth.limits['reset_timestamp'] - time.time()
            logger.info(f'{rem:.0f} calls remaining, {res:.0f} till next reset')
            
            importlib.reload(config)

            time.sleep((len(df.isolate("id").index) + config.post_get_limit) * 2)


if __name__ == "__main__":
    main()
