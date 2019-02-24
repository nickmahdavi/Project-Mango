import signal


class Handler:
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
    def __init__(self):
        self.killed = self.receivedSignal = False
        for signum in self.catchSignals:
            signal.signal(signum, self.handler)

    def handler(self, signum, frame):
        self.lastSignum = signum
        self.lastSignal = Handler.signalNames[Handler.catchSignals.index(signum)]
        self.killed = True

        if signum in [2, 3, 15]:
            self.receivedSignal = True
