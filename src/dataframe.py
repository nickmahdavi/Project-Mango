import pandas as pd
import config


class DataFrame:
    def __init__(self, c, d=None, i=None):
        self.columns = c
        self.df = pd.DataFrame(columns=c, data=d, index=i)

    def __repr__(self):
        return f'DataFrame(columns={self.columns}, rows={len(self.df.index)})'

    def append(self, row):
        self.df = self.df.append(pd.DataFrame(row, columns=self.columns), ignore_index=True)

    def write(self, header=True, index=False, mode='w'):
        with open(config.data, mode) as file:
            self.df.to_csv(file, header=header, index=index)

    def _dict(self, dataframe=None):
        if dataframe is None:
            dataframe = self.df
        return dataframe.to_dict('list')

    def clear(self):
        self.df.drop(self.df.index, inplace=True)

    def isolate(self, column, place=False):
        return self.df.drop_duplicates(subset=column, keep='last', inplace=place)
