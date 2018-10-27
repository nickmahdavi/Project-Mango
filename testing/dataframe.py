import pandas as pd

class DataFrame:
    def __init__(self, c):
        self.args = {} # WIP, not going to do this until later 
        self.c = c
        self.data = pd.DataFrame(columns=c)
        
    def push(self, row, *argv):
        for self.arg in argv:
            if self.arg in self.args.values():
                exec(self.args[self.arg]) # This is... probably not a good way of doing this.
        
        self.data.append(row, ignore_index=True)
        
