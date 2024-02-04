# MILC Metadata

In order to initialize some things, such as the configuration file location and the version number reported by `--version`, MILC needs to know some basic information before the entrypoint is called. You can use `cli.milc_options()` to set this information.

Example:

```python
from milc import cli

cli.milc_options(name='Florzelbop', version='1.0.0', author='Jane Doe')
```

You should only do this once, and you should do it as early in your program's execution as possible.

!!! warning
    If you have spread your program among several files, or you are using `milc.subcommand.config`, you need to use `cli.milc_options()` before you import those modules.

## Custom Loggers

You can also use this to pass in custom loggers.

```python
from milc import cli

from my_program import custom_logger

cli.milc_options(logger=custom_logger)
```

## Deprecated: set_metadata()

Earlier versions of MILC used `milc.set_metadata` instead. This is still supported but will throw a Deprecation warning.
