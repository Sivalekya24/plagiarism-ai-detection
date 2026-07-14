import time


class Timer:

    def __init__(self):
        self.start = time.perf_counter()

    def stop(self):

        end = time.perf_counter()

        return round(end - self.start, 4)