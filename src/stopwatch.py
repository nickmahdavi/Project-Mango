import time


class Stopwatch:
    def __init__(self):
        self.watches = {'main':time.perf_counter(), 'df':0, 'fetch':0}

    def reset(self, watch='main'):
        self.watches[watch] = time.perf_counter()

    def mark(self, round_to=3, watch='main'):
        return round(time.perf_counter() - self.watches[watch], round_to)
