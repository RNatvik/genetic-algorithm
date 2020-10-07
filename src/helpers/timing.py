import time


class Timer:

    def __init__(self):
        self.t0 = time.time()

    def time(self, name: str, enable):
        if enable:
            t = time.time()
            dt = t - self.t0
            self.t0 = t
            print(f'{name}: {dt}')
