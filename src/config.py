import os
import time
import numpy

os.chdir(os.path.dirname(os.path.abspath(__file__)))

DRY_RUN     = 0
WIPE_LOGS   = 1
WIPE_DATA   = 1
MAX_RETRIES = 8
QUICK_RUN   = 0
LOG_LEVEL   = "DEBUG"

TIMEOUT_SECS   = 10
POST_GET_LIMIT = 5

if QUICK_RUN:
    POST_PICKUPS = [60 * x for x in [1/12, 1/6, 1/3, 1/2, 3/4, 1,
                                           2, 5, 10, 15, 24,
                                           30, 36, 42, 48, 60, 72]]  # Hours
else:
    POST_PICKUPS = [3600 * x for x in [1/12, 1/6, 1/3, 1/2, 3/4, 1,
                                             2, 5, 10, 15, 24,
                                             30, 36, 42, 48, 60, 72]]  # Hours
    
DATAFILE = os.path.abspath('../data/data.csv')
LOGFILE  = os.path.abspath('../data/log.log')

SUBREDDIT = 'AskReddit'  # Find a better subreddit

CLIENT_ID     = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
PASSWORD      = os.environ['BOT_PASSWORD']
USERNAME      = os.environ['BOT_USERNAME']
USER_AGENT    = os.environ['USER_AGENT']

TIMEOUTS = [2, 5, 10, 15, 20, 30, 60]

ATTR   = ['id',
          'num_comments',
          'title',
          'author',
          'created_utc',
          'ups',
          'downs',
          'edited',
          'stickied',
          'locked'
          ]

S_ATTR = ['active_user_count',
          'subscribers'
          ]

X_ATTR = ['time_now',
          'last_interval',
          'post_pickup'
          ]

# ----------------------------------------------------- #

if WIPE_LOGS:
    open(LOGFILE, 'w').close()

if WIPE_DATA:
    open(DATAFILE, 'w').close()

if os.path.getsize("../data/log.log") != 0:
    logname = '../data/log-' + str(int(time.time())) + '.log'
    open(logname, 'a').close()
    LOGFILE = os.path.abspath('../data/' + logname)

if os.path.getsize("../data/data.csv") != 0:
    logname = '../data/data-' + str(int(time.time())) + '.csv'
    open(logname, 'a').close()
    DATAFILE = os.path.abspath('../data/' + logname)
