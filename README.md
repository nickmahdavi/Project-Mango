# Project Mango
An attempt to observe, simulate and predict human behavior.
This program watches anonymous user actions on Reddit and models the score of posts over time.

## Bits and pieces
To run, simply run main.py in a command line. 

Most configuration is in config.py. Any questions? Email me at nickmahda@gmail.com.

## Requirements
Running this bot requires:

a) Your own reddit account and credentials

b) An API key from reddit

c) praw, pandas (, numpy? Not sure if this is included with pandas. Anyways, I'm not using it at the moment.)

d) Python 3.6+ (f-strings, sorry)

## Some questions and answers (I'll update this if anyone actually reads this)
### Q: Why not SQL?

A: Honestly, SQL just isn't the best idea for Python. Multiline strings for queries just isn't fun. Numpy and Pandas are also extremely well integrated with each other, which is a big help when looking at data trends. See matplotlib.

And the main thing? Pandas is a data analysis toolkit. And when it comes to coding, Python is the language for data analysis.

Pandas also includes SQL support and to_sql methods, just in case.

### Q: Can I run this myself?
A: Yes, so long as you have an API key and user account on Reddit set up for development.

Just run src/main.py in the background and it will a) log data to the data file, and b) log its PID and information in the data file.