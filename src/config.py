import os
import time

os.chdir(os.path.dirname(os.path.abspath(__file__)))

DRY_RUN         = 0
WIPE_LOGS       = 1
WIPE_DATA       = 0
POST_GET_LIMIT  = 5
MAX_RETRIES     = 8
TIMEOUT_SECS    = 10
POST_DROP_AFTER = 127800

DATAFILE = os.path.abspath('../data/data.csv')
LOGFILE  = os.path.abspath('../data/log.log')

SUBREDDIT = 'LifeProTips'  # Find a better subreddit

CLIENT_ID      = os.environ['CLIENT_ID']
CLIENT_SECRET  = os.environ['CLIENT_SECRET']
PASSWORD       = os.environ['BOT_PASSWORD']
USERNAME       = os.environ['BOT_USERNAME']
USER_AGENT     = os.environ['USER_AGENT']

TIMEOUTS = [2, 5, 10, 15, 20, 30, 60]

ATTR     = ['id',
            'num_comments',
            'title',
            'selftext',
            'author',
            'created_utc',
            'ups',
            'downs',
            'edited'
            ]

S_ATTR   = ['active_user_count',
            'subscribers']

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
