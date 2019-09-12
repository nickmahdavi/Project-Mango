# Project Mango
An attempt to observe, simulate and predict human behavior.
This program watches anonymous user actions on Reddit and models the score of posts over time, based off of trends in post metadata.

## Bits and pieces
To run, simply run main.py on the command line.

Most of the configuration is in config.py. Any questions? Email me at [nickmahda@gmail.com](mailto:nickmahda@gmail.com).

The big datafile is zipped; you'll have to unzip it after cloning.

## Requirements
Running this bot requires:

a) Your own reddit account and credentials

b) An API key from reddit

c) All dependencies in requirements.txt. **Note that these include the (possibly unnecessary) dependencies for the notebooks, too!**

d) Python 3.6+

## Some questions and answers (will update infrequently)
### Okay, but what does this actually do?
TL;DR: Get data predict data.

A:

First is the data scraper. The first step is just grabbing everything we can find—that is, everything we want to find. In this case, the preset config values are mainly looking at _post specific values_, e.g. title, number of comments, etc. So we grab all the IDs we can, and check in on them at set intervals, which get farther apart as tine goes on (posts are less volatile the longer they exist). For example, we might get all the values (time posted, title, all that stuff) and log it. Then wait some time and check back in, and log the _new_ values, along with the same ID. We're looking at values during snapshots of time, so we can draw the conclusions independently later.

Second is the modeling. A few notebooks are in the docs folder, for an example of what I did, but there are many more ways to draw conclusions from however large of a data file you have. And it's CSV, so it can be... pretty big. I only looked at a single value vs post score, but with PRAW, even image analysis is possible. There are essentially no bounds on the data you can collect, even beyond the bounds of what a user can see.

### Q: Why not SQL?
A: Honestly, SQL just isn't the best idea for Python. Multiline strings for queries just isn't fun. Numpy and Pandas are also extremely well integrated with each other, which is a big help when looking at data trends. See matplotlib.

And the main thing? Pandas is a data analysis toolkit. And when it comes to coding, Python is the language for data analysis. Pandas also includes SQL support and the to_sql() method, though, so it's not completely impossible.

### Q: Can I run this myself?
A: Yes, so long as you have an API key and user account on Reddit set up for development. Set all the respective variables as environment vars, and the config will pick them up.

Just run src/main.py in the background and it will a) log data to the data file, and b) log its PID and information in the data file. ~A bit crude, but it gets the job done.~
