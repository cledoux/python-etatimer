This is meant to be a super simple drop in for tracking progress.

This is, in essence, a wrapper around [progressbar2][1] with my personally 
preferred defaults and ways of doing things.

If you need anything even slightly more complicated than what EtaTimer 
provides, I recommend looking at the progressbar2 module instead.

[1]: https://github.com/WoLpH/python-progressbar

# Quickstart
    from etatimer import EtaTimer
    import time

    x = range(5)
    t = Timer(len(x))
    for i in x:
        t.tick()
        time.sleep(1)

# Classes

## `EtaTimer(total, name="", stream=sys.stdout)`
Create a simple ETA Timer named `name` that tracks `total` number of operations 
and prints updates to the stream `stream`.

## `DummyEtaTimer()`
Timer that supports same API as EtaTimer, but does nothing. Allows for code 
that must always pass a timer, but doesn't always have information needed for 
creating an EtaTimer.

Example: If a file is not seekable, we can't determine the number of lines.

    if infile.seekable():
        timer = ETATimer(sum(1 for i in infile))
        infile.seek(0, 0)
    else:
        timer = DummyTimer()
    process_file(infile, timer)

# API

## `timer.tick()`
    
Mark that one processing item has been completed. 

If all items are processed, ding() will be automatically called.

The timer can be stopped early through manual calling of ding()

Can be used as an arbitrary callback function. Will accept and ignore any 
number of parameters.

## `timer.ding()`

Timer's done!

Prints final statistics. 

## `timer.finished`

Boolean indicating if time is finished.
