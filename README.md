# Project Mango
An attempt to observe, simulate and predict human behavior.
This program watches anonymous user actions on Reddit and models the score of posts over time.

## Bits and pieces
To run, simply run ./main.py & in a command line. 

Most configuration is in config.py. Any questions? Email me at nickmahda@gmail.com.

## Requirements
Running this bot requires:

a) Your own reddit account and credentials

b) An API key from reddit

c) praw, pandas

d) Python 3.6

## Some questions and answers
### Q: Why not SQL?

A: Honestly, SQL just isn't the best idea for Python. Multiline strings for queries just isn't fun. Numpy and Pandas are also extremely well integrated with each other, which is a big help when looking at data trends. See matplotlib.

And the main thing? Pandas is a data analysis toolkit. And when it comes to coding, Python is the language for data analysis.

Pandas also includes SQL support and to_sql methods, just in case.

### Q: Why do you have a seperate class for Pandas dataframes?
A: Short answer: I'm lazy.

Long answer:

Pandas has all sorts of obscenely long individual lines. Let's say I want to add a row to a Pandas dataframe:

df = df.append(pd.DataFrame(data={goes: [here]}}, columns=[list, of, columns, here]), ignore_index=True)

So I cut this down by 90 characters or so (yes, that is a lower bound on how long that line would be). It's probably bad practice, so let me know if you have a better idea.

### Can I run this myself?
A: Yes, so long as you have an API key and user account on Reddit set up for development.

Just run src/main.py in the background and it will a) log data to the data file, and b) log its PID and information in the data file.

### Project... Mango?
A: Your point is?
