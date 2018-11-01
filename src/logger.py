import config
import signal
import logging


class Handler:
    def __init__(self):
        self.killed = self.receivedSignal = False
        catchSignals = [1,
                        2,
                        3,
                        10,
                        11,
                        12,
                        15
                        ]
        signalNames = ['SIGHUP',
                       'SIGINT',
                       'SIGQUIT',
                       'SIGBUS',
                       'SIGUSR1',
                       'SIGUSR2',
                       'SIGTERM'
                       ]

        for signum in catchSignals:
            signal.signal(signum, self.handler)

    def handler(self, signum, frame):
        self.lastSignum = signum
        self.lastSignal = signalNames[catchSignals.index(signum)]
        self.killed = True

        if signum in [2, 3, 15]:
            self.receivedSignal = True


class Logger:
    def log(self, text):
        logging.info(text)

    def write(self, data):
        with open(config.data, 'a') as writefile:
            writefile.write(f'{str(data)}')
