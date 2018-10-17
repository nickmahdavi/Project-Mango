import os

# This file is not meant to be modified. Please make sure you know what you
# are changing before you make the changes, and document them well.

# ----------------------------------------------------------- #
## <-- Environment variables for the bot and other code. --> ##
# ----------------------------------------------------------- #

rpm = '30'
dry_run = '1'
do_write = '1'
data = os.path.abspath('../data/data')
log = os.path.abspath('../data/log.log')

# Config to enable praw to access Reddit. See
# praw.readthedocs.io/en/latest/getting_started/quick_start.html
# for details on generating your own bot credentials.

client_id = os.environ['CLIENT_ID'] = 
client_secret = os.environ['CLIENT_SECRET'] = 
password = os.environ['CLIENT_PASSWORD'] = 
username = os.environ['CLIENT_USERNAME'] = 
user_agent = os.environ['USER_AGENT'] = 

# If the bot is accessing Reddit, this determines which
# subreddit it should monitor.

subreddit = os.environ['SUBREDDIT'] = 'MemeEconomy'
