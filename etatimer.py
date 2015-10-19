from __future__ import division, absolute_import, with_statement
# Copyright (c) 2015 University of Louisiana at Lafayette.
# All rights reserved.

import sys
import time

from progressbar2 import ETA, AdaptiveETA, Percentage, StopWatch, SimpleProgress, format_updatable


class EtaTimer(object):
    """ Keep track of how much processing time is left.
    Initialize object with the number of items that need to be processed.  After
    every individual item is processed, call t.tick().  This function will keep
    an internal counter of items left and every inc ticks report estimated time
    left.

    When the internal counter reaches zero, ding() is automatically
    called and final statistics are reported. The timer can manually be stopped
    by a call to ding() as well.
    """
    def __init__(self, total, name="", stream=sys.stdout):
        """
        Arguments:
            total:  Total number of items that will need processing.
            stream:     File descriptor to write to
        """
        self.stream = stream
        # The current number of values already processed
        self.currval = 0
        # The total number of items to process.
        # Naming is weird to match expectations of adapted progressbar2 code.
        self.maxval = total
        self.start_time = time.time()
        self.seconds_elapsed = 0
        self.last_update_time = 0
        self.poll = 1
        self.eta_window = 0
        self._widgets = self._default_widgets()
        self.name = name
        self.write_update()

    @property
    def left(self):
        return self.maxval - self.currval

    def percentage(self):
        return self.currval * 100.0 / self.maxval

    @property
    def finished(self):
        return self.currval == self.maxval

    # backwards compatibility alias
    def done(self):
        return self.finished

    def write_update(self):
        self.fd.write('\r' + self._format_line())
        self.fd.flush()
        self.last_update_time = time.time()

    def tick(self, *args):
        """ Finished an item.
        The *args is so this can be used as an arbitrary callback
        """
        self.currval += 1
        self.seconds_elapsed = time.time() - self.start_time
        if self.finished:
            self.ding()
        else:
            # Only update once a second at most
            if time.time() - self.last_update_time > self.poll:
                self.write_update()

    def ding(self):
        """ Time's up. Ding! """
        self.seconds_elapsed = time.time() - self.start_time
        # Clear current line
        # If using the ANSI escape sequence is ever an issue, we
        # can start tracking the length of the last output line
        # and using \r to put the proper number of spaces over the line.
        self.fd.write('\r\x1b[K')
        self.write_update()
        self.fd.write('\n')

    # progressbar2 adapted code
    def _default_widgets(self):
        if self.eta_window == 0:
            eta = ETA()
        else:
            eta = AdaptiveETA(num_samples=self.eta_window)
        return [
            Percentage(), ' (', SimpleProgress(), ') ',
            StopWatch(), ' ', eta,
        ]

    def _format_line(self):
        if self.finished:
            # Ignore ETA if finished, already including StopWatch
            result = [format_updatable(widget, self)
                      for widget in self._widgets[:-2]]
        else:
            result = [format_updatable(widget, self)
                      for widget in self._widgets]

        return ''.join(result)


class DummyTimer(object):
    """ A mock of timer that does nothing.
    Exists as a default argument anytime timer is user.
    Allows for easy code.  Set this as the default argument,
    then simply pretend like you always have a timer.
    """
    finished = True

    def tick(self):
        pass

    def ding(self):
        pass

    def done(self):
        return True
