#!/usr/bin/python
import pdb
import pprint
import time
import asyncio
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))
import praw

r=praw.Reddit('boolinbot')
s=r.subreddit("MemeEconomy")
ss = {}
n=[]
t=[5,10,30,60,120,240]

async def queue():
    d=1
    global c
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
            n.append(b)

def loop():
    queue()
    for x in t:a
        time.
        for y in len(ss[c]):
            b=t[y]
            ss[c][b]["%s min report" %t[y]]=int(b.score)+1
            
            


queue()
