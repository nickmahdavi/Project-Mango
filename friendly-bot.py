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
final = {}
fetch_count=0
timestamps=[]
t=[5,5,20,30,60,120]
d=[1,2,3,4]

def queue():
	first_run=1
	global c
	for post in s.new(limit=25):
		if first_run==1:
			stamp=time.time()
			timestamps.append(stamp)
			final[stamp]= {}
		first_run=0
		if post.score == 0 and post.is_self == False:
			post_id=post.id
			dc = dt.fromtimestamp(post.created)
			final[stamp][post_id]={}
			final[stamp][post_id]["Title"]=post.title
			final[stamp][post_id]["Score"]=int(post.score)
			final[stamp][post_id]["Time"]=post.created
			final[stamp][post_id]["CleanTime"]=str(dc.hour)+":"+str(dc.minute)+":"+str(dc.second)
			final[stamp][post_id]["CleanDate"]=str(dc.day)+"/"+str(dc.month)+"/"+str(dc.year)
		if len(final[stamp]) > 10:
			break


def fetch(quickrun=0):
	totaltime=0
	global fetch_count
	fetch_count+=1
	queue()
	n=list(final[timestamps[fetch_count-1]].keys())
	print("begin %s" %len(n))
	if quickrun==0:
		truesleep=t
	else:
		truesleep=d
	for i in truesleep:
		print("loop")
		time.sleep(i*60)
		totaltime+=i
		truetotaltime=totaltime
		if y>59:
			timeid="hours"
			z=int(truetotaltime=totaltime/60)
		else:
			timeid="minutes"
		if totaltime==1:
			timeid="minute"
		elif totaltime==60:
			timeid="hour"
		for l in n:
			final[timestamps[fetch_count-1]][l]["Score after {0} {1}".format(truetotaltime, timeid)]=r.submission(l).score
			print("get %s" %l)

fetch()
pprint.pprint(q)
