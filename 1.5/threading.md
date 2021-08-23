# Thread Safety

MILC provides a locking mechanism you can interact with for thread safety. It will acquire and release that lock when changing any objects in memory. You can utilize this same mechanism in your own programs as needed. Under the hood it uses an [RLock object](https://docs.python.org/3.8/library/threading.html#rlock-objects) to do the locking.

## Acquire

You can use `cli.acquire_lock(blocking=True)` to prevent all write operations from happening. Other threads that want to make any changes will block until they can acquire the lock, so it's important not to hold the lock longer than necessary.

When invoked with the blocking argument set to False the call will always return right away. It will return True when the lock has been acquired and False otherwise.

## Release

The `cli.release_lock()` function will release the lock so another thread can acquire it.


