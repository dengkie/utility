import threading
import math
import time

import utility.logging


class Slider(threading.Thread):
    """for gradually sliding the value of a given variable"""

    MIN = 0.0
    MAX = 1.0

    def __init__(self, initial, interval, step):
        self.log = utility.logging.get_logger(self)
        self.interval = interval
        self.step = step
        # callbacks
        self.when_stable = None
        self.when_changed = None
        # internal
        self._value = initial
        self._goal = initial
        self._is_sliding = False
        # threading
        self._slide_lock = threading.Lock()
        self._stop_flag = threading.Event()
        # init value
        self.value = initial
        super().__init__(daemon=True)

    def run(self):
        while not self._stop_flag.is_set():
            time.sleep(self.interval)
            # if unlock failed, skip till next loop
            if not self._slide_lock.acquire(blocking=False):
                msg = 'failed slide_lock acq during loop; will try next loop'
                self.log.debug(msg)
                continue
            # when stable, verify that the goal is actually reached
            if not self._is_sliding:
                if self.value == self._goal:
                    # not sliding and goal reached -- expected idle state
                    pass
                else:
                    # if goal not reached while not sliding, it's a problem
                    msg = 'not sliding & goal not reached; forcing v={} to g{}'
                    self.log.warning(msg.format(self.value, self._goal))
                    self.value = self._goal
            # when sliding, reach to goal
            else:
                diff = self._goal - self.value
                # if goal beyond reach of single step, then step one
                if abs(diff) > self.step:
                    self.value += math.copysign(self.step, diff)
                    self._slide_lock.release()
                # if goal within reach of single step, reach immediately
                else:
                    self.value = self._goal
                    self._is_sliding = False
                    # release lock BEFORE callback to prevent thread-lock
                    self._slide_lock.release()
                    if self.when_stable:
                        self.when_stable(self.value)
            # make sure lock is released
            if self._slide_lock.locked():
                self._slide_lock.release()

    def slide_to(self, goal):
        self._slide_lock.acquire(blocking=True)
        self._goal = goal
        self._is_sliding = True
        self._slide_lock.release()

    def stop_sliding(self, set_value_to=None):
        self._slide_lock.acquire(blocking=True)
        self._is_sliding = False
        if set_value_to is not None:
            self._value = set_value_to
        self._goal = self.value
        self._slide_lock.release()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if new_value != self._value:
            self._value = new_value
            if self.when_changed:
                self.when_changed(new_value)


if __name__ == '__main__':
    # a slider to change volume gradually, started at %0
    vol_slider = Slider(initial=0, interval=0.1, step=0.1)

    # prepare callbacks
    def on_vol_change(vol):
        print('setting system volume to %.2f' % vol)

    def on_vol_stable(vol):
        print('system volume stables at %.2f' % vol)

    vol_slider.when_changed = on_vol_change
    vol_slider.when_stable = on_vol_stable

    # remember to start slider thread
    vol_slider.start()

    # slide vol up to 100%
    vol_slider.slide_to(1.0)

    # peek to see vol in change
    time.sleep(0.5)
    print('- look, system volume at %.2f' % vol_slider.value)

    # wait while slider finishes its job
    time.sleep(1)
