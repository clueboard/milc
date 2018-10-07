# MILC - An Opinionated Batteries-Included Python CLI Framework

MILC is a framework for writing CLI applications in Python. It gives you
all the features users expect from a modern CLI tool out of the box:

* CLI Argument Parsing, with or without subcommands
* Automatic tab-completion support through [argcomplete](https://github.com/kislyuk/argcomplete)
* Configuration file which can be overridden by CLI options
* ANSI color support- even on Windows- with [colorama](https://github.com/tartley/colorama)
* Logging to stderr and/or a file, with ANSI colors
* Easy method for printing to stdout with ANSI colors
* Labelling log output with colored emoji to easily distinguish message types
* Thread safety

## Short Example

```python
from milc import MILC

cli = MILC('My useful CLI tool.')

@cli.argument('-c', '--comma', help='comma in output', default=True, action='store_boolean')
@cli.argument('-n', '--name', help='Name to greet', default='World')
@cli.entrypoint
def main(cli):
    comma = ',' if cli.config.general.comma else ''
    cli.log.info('Hello%s %s!', comma, cli.config.general.name)

if __name__ == '__main__':
    cli.run()
```

Output:

```
$ ./hello
ℹ Hello, World!
$ ./hello --no-color
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

# Documentation

Documentation can be found in [docs/](docs/readme.md).

# Why MILC?

Because life is too short to integrate this stuff yourself, and writing
good CLI's with comprehensive functionality is hard.

Most of the other CLI frameworks are missing a piece of the puzzle. Maybe
they have argument parsing but no config file story. Maybe they have a
good story around arguments and config but don't handle logging at all.
You know that you're doing the same integration work that almost everyone
else is doing in their own app. Why do we duplicate so much effort?

MILC is my answer to that. It implements a common set of CLI tools that
pretty much every project I have ever worked on either needed or would
have benefited from. Included in MILC are answers to problems you didn't
know you had:

* Config file saving and parsing
* Automatically overriding config options with CLI arguments
* Automatic verbose (-v) support
* Automatic log support
* Built-in flags for formatting log messages and log date formats
* Support for boolean arguments (define --foo and get --no-foo for free)

You may not use all of these features yourself, but you will have users
who are very glad these options are available when they need them.

# FAQ

## Why add_argument() instead of parsing function signatures?

Because I believe in writing good CLI tools.

In researching modules before writing MILC I saw variations of the same 
story over and over. "I started with {Click,Docopt,Whatever} but after a 
while I ended up just going back to argparse." In pretty much every case 
as the complexity of their program grew they needed to do things argparse 
made easy and their framework made hard.

MILC attempts to solve this by embracing the complexity of argparse. It 
handles the drudgery of setting up argparse for you, but gives you the 
means to control that complexity when you need to.

If you care about writing good CLI tools (and I hope you do) you will want
more control over the behavior of your program than Click or Docopt give you.

## Why Not Some Other CLI Framework Instead?

Whenever you release a new framework the first question you'll be asked is
why you didn't just use one of the existing options instead. The initial
motivation for MILC was to provide a context manager, something the other
frameworks I've found don't do.

As I surveyed the other tools in this space I felt like there was a goldilox
problem. Frameworks like Click or Getopt are like your average sedan, great
for everyday use. There are a lot of simple frameworks like begins or plac
which are like bicycles, easy to hop on and take short trips with. There are
big expansive frameworks like Cement which are dump trucks or cargo haulers,
able to handle any job you throw at them if with enough effort. But what I
want is more like a cargo van. Big enough to haul around all the tools and
cargo I need for most jobs but easy to drive around like a sedan.

Below is a list of the existing tools I have looked at and why I feel they
don't fill the same need as MILC.

| Name | Argument Parsing | Python 2 Support | Config File | Logging | Subcommands | Subcommand Config | Last PyPi Release |
|------|------------------|------------------|-------------|---------|-------------|-------------------|-------------------|
| MILC | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | Never |
| [Argparse](#Argparse) | ✔ | ✔ | ✖ | ✖ | ✔ | ✖ | N/A |
| ConfigParser | ✖ | ✔ | ✔ | ✖ | ✔ | ✖ | N/A |
| logging | ✖ | ✔ | ✖ | ✔ | ✖ | ✖ | N/A |
| [Argvard](#Argvard) | ✔ | ✔ | ✖ | ✖ | ✔ | ✖ | 2014 |
| [Autocommand](#Autocommand) | ✔ | ✔ | ✖ | ✖ | ✔ | ✖ | 2017 |
| [Begins](#Begins) | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | 2014 |
| [Cement](#Cement) | ✔ | ✖ | ✔ | ✔ | ✔ | ✔ | 2018 |
| [Cliar](#Cliar) | ✔ | ✖ | ✖ | ✖ | ✔ | ✖ | 2018 |
| [Click](#Click) | ✔ | ✔ | ✖ | ✖ | ✔ | ✖ | 2018 |
| [Clize](#Clize) | ✔ | ✖ | ✖ | ✖ | ✔ | ✖ | 2018 |
| [Cogs](#Cogs) | ✔ | ✔ | ✖ | ✖ | ✔ | ✖ | 2018 |
| [Defopt](#Defopt) | ✔ | ✔ | ✖ | ✖ | ✔ | ✖ | 2017 |
| [Docopt](#Docopt) | ✔ | ✔ | ✖ | ✖ | ✔ | ✖ | 2014 |
| [Fire](#Fire) | ✔ | ✔ | ✖ | ✖ | ✔ | ✖ | 2018 |
| [Plac](#Plac) | ✔ | ✖ | ✖ | ✖ | ✖ | ✖ | 2018 |
| [Optutils](#Optutils) | ✔ | ✔ | ✖ | ✖ | ✔ | ✖ | 2015 |

### Argparse

The built-in argparse module is amazing- MILC uses it under the hood. Using
it directly as an enduser is complicated and error-prone however. The common
patterns mean you end up putting the definition of CLI arguments in a
different place from the code that uses those arguments.

### Argvard

<https://github.com/DasIch/argvard>

I like the argument parsing in Argvard a lot. It's almost exactly like 
MILC's. However, it has not been maintained in 5 years.

Argvard does not support a configuration file or logging.

### Autocommand

<https://github.com/Lucretiel/autocommand>

Autocommand is one of the newer "use type annotation to infer arguments"
modules. On the surface these seem good, but it leaves you in a place where
you inherently give up some flexibility. For example, with MILC you can
have some arguments that use `action='store_true'` and others that use
`action='store_boolean'`. With autocommand you have to use
`@autocommand(add_nos=True)` which generates `--no-<arg>` flags for
every argument that has a boolean as a default.

Autocommand does not support a configuration file or logging.

### Begins

<https://github.com/aliles/begins>

Begins is very interesting. It implements a lot of the things I want in a
lightweight way. But it still makes the app developer set up things like
logging and config file support. MILC is opinionated, it thinks every CLI
program should have that, along with ways for the end-user to control it.

Begins does not support a configuration file or logging.

### Cement

<https://builtoncement.com/>

Cement is a very heavy MVC framework for building CLI tools. It includes all
the functionality MILC provides and then some. If you're looking for an
MVC framework for your tool this is the one to pick. 

If you are looking for an MVC framework MILC probably isn't want you want.
Use Cement instead.

### Cliar

<https://moigagoo.github.io/cliar/>

This is an interesting library. The author makes some good points about
magic and DSL's. But it requires you to write a class for your CLI. Classes
are good, but not every tool should be a class.

Cliar does not support a configuration file or logging.

### Click

<https://github.com/pallets/click>

You'd have to be a fool or incredibly sure of yourself to compete against one
of Armin Ronacher's projects. :)

Click is great, and I borrowed the decorator concept from Flask before I saw
Click had done the same thing. It terms of how you use it there are a lot of
simularities between Click and MILC. 

Where Click and MILC part ways is in the underlying implementation. MILC
uses the recommended and built-in python modules whenver possible. Under the
hood MILC is just argparse, logging, ConfigParser, and other standard modules
abstracted just enough to make the right thing easy. Click on the other hand
uses optparser, which has been deprecated in favor of argparser, and handles
a lot of functionality itself rather than dispatching to included python
modules.

MILC does not insist upon a UTF-8 environment for Python 3 the way Click
does. I understand Click's stance here but I'm hoping that the ecosystem has
developed enough by now to make it no longer necessary. 

Whether you should use Click or MILC depends on the tradeoff you want to
make. Would you rather use the python modules everyone's already familiar with
or dive into a world of custom code that attempts to make everything cleaner
overall? Do you want one cohesive system or do you want to pull together
disparate plugins and modules to build the functionality you need?

Click does not support a configuration file or logging out of the box, but
there are [plugins](https://github.com/click-contrib) you can get to add this
and other functionality to Click.

### Clize

<https://github.com/epsy/clize>

Clize does not properly support python 2 anymore, at least for the things
that make Clize worth using. There are workarounds, but IMO those workarounds
are not worth the effort. If you are python3 only Clize may be worth a look.
It certainly has a nice approach with lots of mature and advanced 
functionality. 

Clize uses function annotation to work, which may or may not fit with how you
work. It also has a lot of arbitrary restrictions due to anotations, for
example alt functions don't work with argument aliases.

Clize does not support a configuration file or logging.

### Cogs

<https://bitbucket.org/prometheus/cogs>

Cogs seems interesting, but has its own dedicated CLI tool named `cogs`. You
don't create scripts directly but instead create python functions that `cogs`
will call. This is not a paradigm that I want to use.

Cogs does not include config file support.

### defopt

<https://github.com/evanunderscore/defopt>

Defopt is a great tool for turning functions into CLI's. Had I found this
earlier I may not have written MILC at all. But I have written MILC, and
there's some things I'm still not sure about. For example, I don't see a way
to have script handle both subcommand and non-subcommand operation.

Defopt does not support a configuration file or logging.

### docopt

<https://github.com/docopt/docopt>

Docopt has a large following, and some interesting ideas. But if you are
someone who does not like the idea of using comments to define behavior you
will not enjoy working with docopt.

Docopt has poor error handling. You have to do your own argument validation,
and even when Docopt knows the passed arguments are invalid it does not return
a useful error message to the user. The DSL for argument definition makes
it hard to compose Docopt programs.

Docopt does not support config files.

### Fire

<https://github.com/google/python-fire>

Fire is an interesting idea- turn any class into a CLI. Unfortunately this
is useful more as a tool for introspection than building a good CLI.

Fire does not support a configuration file or logging.

### Plac

<https://github.com/micheles/plac>

I like his idea about scaling down, and it's part of what drove me. But I don't want to go without functionality to scale down, I want MILC to work well for very small CLI tools.

Plac does not support a configuration file or logging.

### optutils

<https://github.com/timtadh/optutils>

There are some interesting ideas here, particularly integrating configuration
files with CLI options. But there's no log file support, and the framework
is incomplete.

Optutils does not support logging.
