# MILC Metadata

In order to initialize some things, such as the configuration file location and the version number reported by `--version`, MILC needs to know some basic information before you import `cli`. If you need to set the program's name, author name, and/or version number do it like this:

```python
from milc import set_metadata

set_metadata('Florzelbop', '1.0.0', 'Jane Doe')

from milc import cli
```

You should only do this once, and you should do it as early in your program's execution as possible.

!!! danger
    Do not import `set_metadata` and `cli` at the same time! When you run `set_metadata` the `cli` object will be replaced, but your existing import will continue to reference the old `cli` object.

## Environment based setup

Earlier versions of MILC used the environment variables `MILC_APP_NAME`, `MILC_APP_VERSION`, and `MILC_AUTHOR_NAME` to set this information. While this is supported in MILC 1.4.x it will throw a `DeprecationWarning` and will be removed in a later version of MILC.

You can supress this warning by setting the environment variable `MILC_IGNORE_DEPRECATED`.
