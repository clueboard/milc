# MILC - An Opinionated Batteries-Included Python 3 CLI Framework

MILC is a framework for writing CLI applications in Python 3. It gives you all the features users expect from a modern CLI tool out of the box:

* CLI Argument Parsing, with or without subcommands
* Automatic tab-completion support through [argcomplete](https://github.com/kislyuk/argcomplete)
* Configuration file which can be overridden by CLI options
* ANSI color support- even on Windows- with [colorama](https://github.com/tartley/colorama)
* Logging to stderr and/or a file, with ANSI colors
* Easy method for printing to stdout with ANSI colors
* Labelling log output with colored emoji to easily distinguish message types
* Thread safety
