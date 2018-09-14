import os
import sys
import logging

# This file is not meant to be modified. Please make sure you know what you
# are changing before you make the changes, and document them well.

# ----------------------------------------------------------- #
## <-- Environment variables for the bot and other code. --> ##
# ----------------------------------------------------------- #

rpm = os.environ['REQ_PER_MIN'] = '30'
dry_run = os.environ['BOT_DRY_RUN'] = '1'
do_write = os.environ['DRY_WRITE_RUN'] = '1'
data = os.environ['FILE_WRITE_TO'] = os.path.abspath('../data/data')
log = os.environ['FILE_DEBUG'] = os.path.abspath('../data/log.log')

# For sorted logging - disabled for now, you will have
# to set this up manually.
'
debug = os.environ['FILE_DEBUG'] = open(os.join(os.path.realpath(__file),
                                                '../data/debug.log'))
info = os.environ['FILE_DEBUG'] = open(os.join(os.path.realpath(__file),
                                                '../data/info.log'))
error = os.environ['FILE_DEBUG'] = open(os.join(os.path.realpath(__file),
                                                '../data/error.log'))
warning = os.environ['FILE_DEBUG'] = open(os.join(os.path.realpath(__file),
                                                '../data/warning.log'))
'


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


# ------------------------------------- #
## <-- Local variables for the bot --> ##
# ------------------------------------- #

basename = os.path.basename(__file__)[-3:]

# ----------------------------------------------------------- #
## <-- Setup functions for logging, etc --> ##
# ----------------------------------------------------------- #
