# MILC - An Opinionated Batteries-Included Python 3 CLI Framework

MILC is a framework for writing CLI applications in Python 3.6+. It gives you
all the features users expect from a modern CLI tool out of the box:

* CLI Argument Parsing, with or without subcommands
* Automatic tab-completion support through [argcomplete](https://github.com/kislyuk/argcomplete)
* Configuration file which can be overridden by CLI options
* ANSI color support- even on Windows- with [colorama](https://github.com/tartley/colorama)
* Logging to stderr and/or a file, with ANSI colors
* Easy method for printing to stdout with ANSI colors
* Labeling log output with colored emoji to easily distinguish message types
* Thread safety
* More than 60 built-in [spinners](https://github.com/manrajgrover/py-spinners) with the ability to add your own

# Installation

MILC is available on pypi, you can use pip to install it:

    python3 -m pip install milc

# ChangeLog and Breaking Changes

MILC follows [Semantic Versioning](https://semver.org/). You can view the [full changelog](https://github.com/clueboard/milc/blob/master/CHANGELOG.rst), or you can see a list of why we made major or minor releases on the [Breaking Changes](https://milc.clueboard.co/#/breaking_changes) page.

# Documentation

Full documentation is on the web: <https://milc.clueboard.co/>

## Reporting Bugs and Requesting Features

Please let us know about any bugs and/or feature requests you have: <https://github.com/clueboard/milc/issues>

## Short Example

```python
from milc import cli

@cli.argument('-c', '--comma', arg_only=True, action='store_boolean', default=True, help='comma in output')
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
  --config-file GENERAL_CONFIG_FILE
                        The config file to read and/or write
  --save-config         Save the running configuration to the config file
  -n GENERAL_NAME, --name GENERAL_NAME
                        Name to greet
  -c, --comma           Enable comma in output
  --no-comma            Disable comma in output
```

# Why MILC?

Because life is too short to integrate this stuff yourself, and writing
good CLIs with comprehensive functionality is harder than it needs to be.

Most of the other CLI frameworks are missing a piece of the puzzle. Maybe
they have argument parsing but no config file story. Maybe they have a
good story around arguments and config but don't handle logging at all.
You know that you're doing the same integration work that almost everyone
else is doing in their own app. Why do we duplicate so much effort?

MILC is my answer to that. It implements a common set of CLI tools that
pretty much every project I have ever worked on either needed or would
have benefited from. Included in MILC are answers to problems you didn't
know you have:

* Config file saving and parsing
* Automatically overriding config options with CLI arguments
* Automatic verbose (-v) support
* Automatic log support
* Built-in flags for formatting log messages and log date formats
* Support for boolean arguments (define --foo and get --no-foo for free)
* Battle tested and used by hundreds of users every single day

You may not use all of these features yourself, but you will have users
who are very glad these options are available when they need them.

# Contributing

Contributions are welcome! You don't need to open an issue first, if
you've developed a new feature or fixed a bug in MILC simply open
a PR and we'll review it.

Please follow this checklist before submitting a PR:

* [ ] Format your code: `yapf -i -r .`
* [ ] Generate docs: `./generate_docs`
* [ ] Add any new doc files to the `nav` section of `mkdocs.yml`
* [ ] Run tests: `./ci_tests`

# FAQ

## What does MILC stand for?

MILC was originally the CLI Context Manager, or CLI Manager, but CLICM was too close to [click](https://click.palletsprojects.com/) and CLIM was already taken on PyPi. Reversing CLIM gave me a name I liked and had opportunities for puns, so I went with it.

## Why decorators instead of parsing function signatures?

Because I believe in writing good CLI tools.

Before writing MILC I saw variations of the same story over and over. "I
started with {Click,Docopt,Whatever} but after a while I ended up just
going back to argparse." In pretty much every case as the complexity of
their program grew they needed to do things argparse made easy and their
framework made hard.

MILC attempts to solve this by embracing the complexity of argparse. It
handles the drudgery of setting up argparse for you, but gives you an
elegant means to control that complexity when you need to. When your
CLI framework relies on parsing function signatures you are necessarily
limited in what you can do. Function annotations make this a little
better but they are not a full solution to the problem.

If you care about writing good CLI tools (and I hope you do) you will want
more control over the behavior of your program than Click or Docopt give you.

## Why Not Some Other CLI Framework Instead?

Whenever you release a new framework the first question you'll be asked is
why you didn't just use one of the existing options instead.

As I surveyed the other tools I found that most of them only solve part of
the problem, not the whole problem. Those that solve the whole problem are
very hard to use or get started with, or are otherwise very heavyweight. I
wanted a comprehensive framework that was easy to get started with.

If you'd like to see how MILC compares to other tools see
[COMPARISONS.md](COMPARISONS.md).
