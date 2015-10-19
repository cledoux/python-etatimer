Wrapper around 
(python-progressbar)[https://github.com/WoLpH/python-progressbar] to provide a 
dead simple eta timer. Basically, wraps progressbar with my personally 
preferred defaults and manner of usage.

# Classes

### `EtaTimer(total, name="", stream=sys.stdout)`
Create a simple ETA Timer named `name` that tracks `total` number of operations 
and prints updates to the stream `stream`.

### `DummyEtaTimer()`
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

### `timer.tick()`
    
Mark that one processing item has been completed. 

If all items are processed, ding() will be automatically called.

The timer can be stopped early through manual calling of ding()

Can be used as an arbitrary callback function. Will accept and ignore any 
number of parameters.

### `timer.ding()`

Timer's done!

Prints final statistics. 

### `timer.finished`

Boolean indicating if time is finished.
