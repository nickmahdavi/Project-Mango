import pandas as pd
import configparser

class DataFrame:
    def __init__(self, c):
        self.c = c
        self.df = pd.DataFrame(columns=c)

    def push(self, row):
        self.df.append(pd.DataFrame(row, columns=self.c), ignore_index=True)

    def write(self, dataframe):
        with open(config.data)

