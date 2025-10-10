import time

class PerfTimer:
    
    timers = {}
    times = {}

    @staticmethod
    def start(name):
        PerfTimer.timers[name] = time.perf_counter()
        PerfTimer.times[name] = -1

    @staticmethod
    def end(name):
        PerfTimer.times[name] = time.perf_counter() - PerfTimer.timers[name]
        PerfTimer.timers[name] = None
        return PerfTimer.times[name]
    
    @staticmethod
    def get(name):
        return PerfTimer.times[name]

    @staticmethod
    def init(name):
        PerfTimer.times[name] = 0
        PerfTimer.timers[name] = 0

    def cont(name):
        if name in PerfTimer.times:
            PerfTimer.timers[name] = time.perf_counter() - PerfTimer.times[name]
        else:
            PerfTimer.timers[name] = time.perf_counter()

    def print_timers():
        for i, name in enumerate(PerfTimer.times):
            print(f"{name}: {PerfTimer.times[name]}")