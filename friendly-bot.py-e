#!/usr/bin/python
import pprint
import time
import asyncio
import os
import datetime

#Changes the working dir to current so that praw.ini reads and does not have to be recreated
os.chdir(os.path.dirname(os.path.realpath(__file__)))

import praw

dt=datetime.datetime
r=praw.Reddit('boolinbot')
s=r.subreddit("MemeEconomy")
final = {}
fetch_count=0
timestamps=[]
t=[5,5,20,30]#,60,120]

#Quickrun function - 1 sec, 1 sec, 3 sec, 4 sec
d=[1/60,1/60,3/60,4/60]

#Logging function
def queue():
	global c
	stamp=time.time()
	timestamps.append(stamp)
	final[stamp]= {}
	for post in s.new(limit=25):
		if post.score == 0 and post.is_self == False:
			dc = dt.fromtimestamp(post.created)
			final[stamp][post.id]={}
			final[stamp][post.id]["Title"]=post.title
			final[stamp][post.id]["Score"]=int(post.score)
			final[stamp][post.id]["Time"]=post.created
			final[stamp][post.id]["CleanTime"]=str(dc.hour)+":"+str(dc.minute)+":"+str(dc.second)
			final[stamp][post.id]["CleanDate"]=str(dc.day)+"/"+str(dc.month)+"/"+str(dc.year)
		if len(final[stamp]) > 10:
			break


def fetch(quickrun=0):
	queue()

	global fetch_count
	totaltime=0
	fetch_count+=1
	truesleep=d
	keys=list(final[timestamps[fetch_count-1]].keys())
	
	print("begin %s" %len(keys))

	if quickrun==0:
		truesleep=t
		
	for i in truesleep:
		print("loop")
		
		time.sleep(i*60)
		
		totaltime+=i
		truetotaltime=totaltime

		#Timestamp cleanup
		if totaltime>59:
			timeid="hours"
			truetotaltime=int(totaltime/60)
		elif totaltime<1:
			timeid="seconds"
			truetotaltime=int(totaltime*60)
		else:
			timeid="minutes"

		#Singular noun cleanup	
		if totaltime==1:
			timeid="minute"
		elif totaltime==1/60:
			timeid="second"
		elif totaltime==60:
			timeid="hour"

		
		for l in keys:
			#Appends score after n seconds/minutes/hours
			final[timestamps[fetch_count-1]][l]["Score after {0} {1}".format(truetotaltime, timeid)]=r.submission(l).score
			print("get %s" %l)

	return pprint.pprint(final)
