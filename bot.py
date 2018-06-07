#!/usr/bin/python
import pdb
import pprint
import calendar
import time
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))
import praw

r=praw.Reddit('boolinbot')
s=r.subreddit("MemeEconomy")
ss = {}

def queue():
    d=1
    for b in s.new(limit=25):
        if d==1:
            c=time.time()
            ss[c]= {}
        d=0
        if b.score < 10 and b.title not in ss and b.is_self == False:
            ss[c][b]={}
            ss[c][b]["Title"]=b.title
            ss[c][b]["Score (adjusted)"]=int(b.score)+1
            ss[c][b]["Time"]=b.created
            ss[c][b]["Reliability Factor (/10)"]=10-int(b.score)


queue()
