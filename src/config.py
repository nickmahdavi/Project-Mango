import os, time
from inspect import getfile, currentframe

os.chdir(os.path.dirname(os.path.abspath(getfile(currentframe()))))

dry_run        = 0
pre_wipe       = 1
post_get_limit = 1
max_retries    = (5, 8)

data = os.path.abspath('../data/data.csv')
log = os.path.abspath('../data/log.log')
config = os.path.abspath(__file__)

subreddit = 'AskReddit'

maintenance = 0

cid        = os.environ['CLIENT_ID']
secret     = os.environ['CLIENT_SECRET']
password   = os.environ['PASSWORD']
username   = os.environ['USERNAME']
user_agent = os.environ['USER_AGENT']

timeouts = {
            1: [2, 2],
            2: [5, 5],
            3: [10, 10],
            4: [30, 15],
            5: [None, 20],
            6: [None, 30],
            7: [None, 60]
            }

attributes = ['id',
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

sattributes = ['active_user_count',
               'subscribers'
              ]

xattributes = {'time_now': 'time.time()'
              }
