import threading
import time


class Watcher(threading.Thread):
    """a thread watching for <checker> state to become true"""
    def __init__(self, checker, interval, callback):
        self.interval = interval
        self.checker = checker
        self.callback = callback
        self.watch_delay_counter = 0
        self._watch_flag = threading.Event()
        super().__init__(daemon=True)
        # auto start as actual checking in controlled by watch_flag
        self.start()

    def run(self):
        while True:
            time.sleep(self.interval)
            self._watch_flag.wait()
            if self.watch_delay_counter > 0:
                self.watch_delay_counter -= 1
                continue
            if self.checker():
                self.stop_watch()
                self.callback()

    def start_watch(self, delay_count=0):
        """start watching with after <delay_count> of intervals"""
        self.watch_delay_counter = delay_count
        self._watch_flag.set()

    def stop_watch(self):
        self.watch_delay_counter = 0
        self._watch_flag.clear()
