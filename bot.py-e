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
q = {}
n=[]
fetch_count=0
cs=[]
t=[5,10,30,60,120,240]

def queue():
	first_run=1
	for e in s.new(limit=100):
		if first_run==1:
			c=time.time()
			cs.append(c)
			q[c]= {}
		first_run=0
		if e.score == 0 and e.title not in q and e.is_self == False:
			b=e.id
			q[c][b]={}
			q[c][b]["Title"]=e.title
			q[c][b]["Score (adjusted)"]=int(e.score)
			q[c][b]["Time"]=e.created
		if len(q[c]) > 10:
			break


def fetch():
	fetch_count+=1
	queue()
	n=list(q[c].keys())
	for i in t:
		if i>59:
			x="hours"
			y=t/60
		else:
			x="minutes"
			y=t
		for l in n:
			q[cs[fetch_count]][l]["Score after {0} {1}".format(y, x)]=reddit.submission(l).score
		time.sleep(i)

queue()
pprint.pprint(q)
