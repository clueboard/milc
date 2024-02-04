MILC comes with a robust logging system based on python's `logging` module. All you have to worry about are log messages, let MILC worry about presenting those messages to the user in configurable ways.

## Writing Log Entries

A python [Logger Object](https://docs.python.org/3/library/logging.html#logger-objects) is available as `cli.log`. You can use this to write messages at various log levels:

* `cli.log.debug()`
* `cli.log.info()`
* `cli.log.warning()`
* `cli.log.error()`
* `cli.log.critical()`
* `cli.log.exception()`

As is standard for the python logging module you can use [`printf`-style format string operations](https://docs.python.org/3/library/stdtypes.html#printf-style-string-formatting) with these. Example:

    log.info('Hello, %s!', cli.config.general.name)

ANSI color sequences are also available. For more information see the [ANSI Color](ANSI.md) page.

## Verbose Mode

All MILC programs have `-v` and `--verbose` flags by default. When this flag is passed `DEBUG` level messages will be printed to the screen.

If you want to use this flag in your program you can check `cli.config.general.verbose`. It is True when `-v`/`--verbose` is passed and False otherwise.

## Controlling Log Output

Users have several CLI arguments they can pass to control the output of logs. These are automatically added to your program, you do not have to do anything to make them available:

* `--datetime-fmt`, default: `%Y-%m-%d %H:%M:%S`
    * Default date/time format.
* `--log-fmt`, default: `%(levelname)s %(message)s`
    * Format string for printed log output
* `--log-file-fmt`, default: `[%(levelname)s] [%(asctime)s] [file:%(pathname)s] [line:%(lineno)d] %(message)s`
    * Format string for log file.
* `--log-file`, default: None
    * File to write log messages to
* `--color` and `--no-color`
    * Enable or disable ANSI color
* `--unicode` and `--no-unicode`
    * Enable or disable unicode icons

# Custom Loggers

You may want to bypass MILC's logging and use your own logger instead. To do this use `cli.milc_options(logger=<MyLogger>)`. This should be done before you call `cli()` or do anything else.

Example:

```python
import logging

from milc import cli


@cli.entrypoint('Hello, World!')
def hello(cli):
    cli.log.info('Hello, World!')

if __name__ == '__main__':
    my_logger = logging.getLogger('my-program')
    # Configure my_logger the way you want/need here

    cli.milc_options(logger=my_logger)
    cli()

```

!!! warning
    You should only call `cli.milc_options()` one time during your program's execution.
