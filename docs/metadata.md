# MILC Metadata

In order to initialize some things, such as the configuration file location and the version number reported by `--version`, MILC needs to know some basic information before the entrypoint is called. You can use `cli.milc_options()` to set this information.

Example:

```python
from milc import cli

cli.milc_options(name='Florzelbop', version='1.0.0', author='Jane Doe')
```

You should only do this once, and you should do it as early in your program's execution as possible.

!!! danger
    Do not import `set_metadata` and `cli` at the same time! When you run `set_metadata` the `cli` object will be replaced, but your existing import will continue to reference the old `cli` object.

## Custom Loggers

You can also use this to pass in custom loggers.

```python
from milc import set_metadata

from my_program import custom_logger

set_metadata(logger=custom_logger)

from milc import cli
```

## Deprecated: set_metadata()

Earlier versions of MILC used `milc.set_metadata` instead. This is still supported but will throw a Deprecation warning.
