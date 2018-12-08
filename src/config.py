import os, time
from inspect import getfile, currentframe

os.chdir(os.path.dirname(os.path.abspath(getfile(currentframe()))))

DRY_RUN        = 0
PRE_WIPE       = 1
POST_GET_LIMIT = 1
MAX_RETRIES    = 8

data = os.path.abspath('../data/data.csv')
log  = os.path.abspath('../data/log.log')

subreddit = 'AskReddit'

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
            'subreddit',
            'locked',
            'stickied',
            'created_utc',
            'ups',
            'downs',
            'num_reports',
            'edited'
            ]

S_ATTR   = ['active_user_count',
            'subscribers']
