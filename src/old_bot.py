#!/usr/bin/env python3
import pprint
import time
import asyncio
import os
import datetime

import praw

import config

dt=datetime.datetime
r = praw.Reddit(client_id=config.CLIENT_ID,
                client_secret=config.CLIENT_SECRET,
                password=config.PASSWORD,
                username=config.USERNAME,
                user_agent=config.USER_AGENT)
s=r.subreddit("MemeEconomy")
final = {}
global totaltime
totaltime=0
fetch_count=0
timestamps=[]
t=[5,5,20,30]#,60,120]

#Quickrun function - 1 sec, 1 sec, 3 sec, 4 sec
d=[1/60,1/60,3/60,4/60]

#Logging function
def queue():
        stamp=time.time()
        timestamps.append(stamp)
        final[stamp]= {}
        for post in s.new(limit=25):
                if post.is_self == False:
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
        global fetch_count

        fetch_count+=1
        queue()
        
        truesleep=d
        keys=list(final[timestamps[fetch_count-1]].keys())
        
        print("begin %s" %len(keys))

        if quickrun==0:
                truesleep=t
                
        for i in truesleep:
                print("loop")
                
                time.sleep(i*60)
                
                global totaltime
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

fetch(quickrun=1)
