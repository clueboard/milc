# MILC - An Opinionated Batteries-Included Python 3 CLI Framework

MILC is a framework for writing CLI applications in Python 3.6+. It gives you all the features users expect from a modern CLI tool out of the box:

* CLI Argument Parsing, with or without subcommands
* Automatic tab-completion support through [argcomplete](https://github.com/kislyuk/argcomplete)
* Configuration file which can be overridden by CLI options
* ANSI color support- even on Windows- with [colorama](https://github.com/tartley/colorama)
* Logging to stderr and/or a file, with ANSI colors
* Easy method for printing to stdout with ANSI colors
* Labelling log output with colored emoji to easily distinguish message types
* Thread safety
* More than 60 built-in [spinners](https://github.com/manrajgrover/py-spinners) with the ability to add your own

## Getting Started

Read [the tutorial](tutorial.md) to learn how to use MILC.

## Reporting Bugs and Requesting Features

Please let us know about any bugs and/or feature requests you have: <https://github.com/clueboard/milc/issues>

## Short Example

```python
from milc import cli

@cli.argument('-c', '--comma', action='store_boolean', arg_only=True, default=True, help='comma in output')
@cli.argument('-n', '--name', default='World', help='Name to greet')
@cli.entrypoint('My useful CLI tool.')
def main(cli):
    comma = ',' if cli.args.comma else ''
    cli.log.info('Hello%s %s!', comma, cli.config.general.name)

if __name__ == '__main__':
    cli.run()
```

### Output

```
$ ./hello
ℹ Hello, World!
$ ./hello --no-unicode
INFO Hello, World!
$ ./hello --no-comma
ℹ Hello World!
$ ./hello -h
usage: hello [-h] [-V] [-v] [--datetime-fmt GENERAL_DATETIME_FMT]
             [--log-fmt GENERAL_LOG_FMT] [--log-file-fmt GENERAL_LOG_FILE_FMT]
             [--log-file GENERAL_LOG_FILE] [--color] [--no-color]
             [--config-file GENERAL_CONFIG_FILE] [--save-config]
             [-n GENERAL_NAME] [-c] [--no-comma]

Greet a user.

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         Display the version and exit
  -v, --verbose         Make the logging more verbose
  --datetime-fmt GENERAL_DATETIME_FMT
                        Format string for datetimes
  --log-fmt GENERAL_LOG_FMT
                        Format string for printed log output
  --log-file-fmt GENERAL_LOG_FILE_FMT
                        Format string for log file.
  --log-file GENERAL_LOG_FILE
                        File to write log messages to
  --color               Enable color in output
  --no-color            Disable color in output
  --unicode             Enable unicode loglevels
  --no-unicode          Disable unicode loglevels
  --interactive         Force interactive mode even when stdout is not a tty.
  --config-file GENERAL_CONFIG_FILE
                        The config file to read and/or write
  -n GENERAL_NAME, --name GENERAL_NAME
                        Name to greet
  -c, --comma           Enable comma in output
  --no-comma            Disable comma in output
```

# Breaking Changes

MILC follows [Semantic Versioning](https://semver.org/). You can see a list of why we made major or minor releases on the [Breaking Changes](breaking_changes.md) page.
