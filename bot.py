#!/usr/bin/python
import pdb
import pprint
import time
import asyncio
import os
import datetime
os.chdir(os.path.dirname(os.path.realpath(__file__)))
import praw

dt=datetime.datetime
r=praw.Reddit('boolinbot')
s=r.subreddit("MemeEconomy")
q = {}
fetch_count=0
cs=[]
t=[5,5,20,30,60,120]
d=[1,2,3,4]
used=tuple("abceilnqtxyz")

def queue():
	first_run=1
	global c
	for e in s.new(limit=25):
		if first_run==1:
			c=time.time()
			cs.append(c)
			q[c]= {}
		first_run=0
		if e.score == 0 and e.title not in q and e.is_self == False:
			b=e.id
			dc = dt.fromtimestamp(e.created)
			q[c][b]={}
			q[c][b]["Title"]=e.title
			q[c][b]["Score"]=int(e.score)
			q[c][b]["Time"]=e.created
			q[c][b]["CleanTime"]=str(dc.hour)+":"+str(dc.minute)+":"+str(dc.second)
			q[c][b]["CleanDate"]=str(dc.day)+"/"+str(dc.month)+"/"+str(dc.year)
		if len(q[c]) > 10:
			break


def fetch(quick=0):
	y=0
	global fetch_count
	fetch_count+=1
	queue()
	n=list(q[c].keys())
	m=0
	print("begin %s" %len(n))
	if quick=0:
		a=t
	else:
		a=d
	for i in a:
		print("loop")
		y+=i
		z=y
		if i>59:
			x="hours"
			z=y/60
			x="minute"
		else:
			x="minutes"
		if y==1:
			x="minute"
		for l in n:
			q[cs[fetch_count-1]][l]["Score after {0} {1}".format(z, x)]=r.submission(l).score
			print("get %s" %l)
		time.sleep(i*60)

fetch()
pprint.pprint(q)
