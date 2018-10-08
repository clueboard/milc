# Getting Started With MILC

MILC is a framework for writing CLI tools. It's goal is to make getting
started easy and to grow with your program as it grows. MILC is Batteries
Included- it gives you all the functionality that your users demand out of
the box. Argument parsing, configuration files, flexible and configurable log
output, ANSI colors, spinners, and other nicities are combined into one easy
to use module.

## Installation

TBD - MILC is not yet on pypi.

## MILC Tutorial

MILC works by registering functions as either the entrypoint or a subcommand.
The entrypoint can be thought of as your `main()`, or the place where program
execution begins. A minimal MILC program looks like this:

```python
#!/usr/bin/env python
from milc import MILC

cli = MILC('Greet a user.')

@cli.entrypoint
def main(cli):
    cli.print('{fg_green}Hello, World!')

if __name__ == '__main__':
    cli()
```

### Entrypoints

MILC does the work of setting up your execution environment, then it hands
off control to your entrypoint. There are two types of entrypoints in MILC-
the root entrypoint and subcommand entrypoints. When you think of subcommands
think of programs like git, where the first argument that doesn't start with
a dash indicates what mode the program is operating in.

MILC entrypoints are python callables that take a single argument- `cli`.
This is the `MILC()` object that you instaniate at the start of your program,
and for the most part is how you will interact with your user. You will also
call `cli()` to dispatch to the root or subcommand entrypoint, as determined
by the flags the user passes.

### Logging and Printing

MILC provides 2 mechanisms for outputting text to the user, and which one you
use depends a lot on the needs of your program. Both use the same API so
switching between them should be simple.

For writing to stdout you have `cli.print()`. This differs from the standard
python `print()` in two important ways- It supports tokens for colorizing your
text using ANSI, and it supports format strings in the same way as logging.
For writing to stderr and/or log files you have `cli.log`. You can use these
to output log messages at different levels so the CLI user can easily adjust
how much output they get. ANSI color tokens are also supported in log messages
on the console, and will be stripped out of log files for easy viewing.

You can still use python's built-in `print()` if you wish, but you will not
get ANSI or string formatting support.

### ANSI Color

Using [Colorama](https://github.com/tartley/colorama) we can print colored
output to the screen. MILC's `cli.print()` and all of the `cli.log` methods
support color injection through the use of special tokens. Simply include
one of the tokens below in the text to be printed.

There are 9 ANSI colors that can be used as either foreground or background
colors. In addition there are 9 "extended" colors that are supported on most
modern terminals but may not be supported on some terminals.

| Color | Background | Extended Background | Foreground | Extended Foreground|
|-------|------------|---------------------|------------|--------------------|
| Black | {bg_black} | {bg_lightblack_ex} | {fg_black} | {fg_lightblack_ex} |
| Blue | {bg_blue} | {bg_lightblue_ex} | {fg_blue} | {fg_lightblue_ex} |
| Cyan | {bg_cyan} | {bg_lightcyan_ex} | {fg_cyan} | {fg_lightcyan_ex} |
| Green | {bg_green} | {bg_lightgreen_ex} | {fg_green} | {fg_lightgreen_ex} |
| Magenta | {bg_magenta} | {bg_lightmagenta_ex} | {fg_magenta} | {fg_lightmagenta_ex} |
| Red | {bg_red} | {bg_lightred_ex} | {fg_red} | {fg_lightred_ex} |
| White | {bg_white} | {bg_lightwhite_ex} | {fg_white} | {fg_lightwhite_ex} |
| Yellow | {bg_yellow} | {bg_lightyellow_ex} | {fg_yellow} | {fg_lightyellow_ex} |

There are also control sequences that can be used to change the behavior of
ANSI output:

| Control Sequences |
|-------------------|
| {style_bright} |
| {style_dim} |
| {style_normal} |
| {style_reset_all} |
| {bg_reset} |
| {fg_reset} |

### Configuration and Argument Parsing

MILC unifies arguments and configuration files. This unified config can be
accessed under `cli.config`. You can access this as attributes or
dictionaries. These two lines are equivalent, and will return True when the
user passes `-v` or `--verbose`:

    cli.config.general.verbose
    cli.config['general']['verbose']

Under the hood MILC uses
[ConfigParser](https://docs.python.org/2/library/configparser.html) to read
and write configuration files. If you are not familiar with ConfigParser this
is a sample config file:

```
[general]
verbose=true
```

MILC maps all of the arguments for the root entrypoint into the general
section. Subcommand arguments are mapped into their own section. We'll talk
about this more when we introduce subcommands, for now you just need to
understand that arguments are added to the general section.

Building on our program from earlier we can make our program more flexible
about who it is greeting by adding a new flag, `--name`, or `-n` for short:

```python
#!/usr/bin/env python
from milc import MILC

cli = MILC('Greet a user.')

@cli.argument('-n', '--name', help='Name to greet', default='World')
@cli.entrypoint
def main(cli):
    cli.print('{fg_green}Hello, %s!', cli.config.general.name)

if __name__ == '__main__':
    cli()
```

One important thing to note is that decorators are processed from the bottom
to the top. You must place `@cli.entrypoint` directly above the function
definition, and then place and `cli.argument()` decorators above that to
avoid a stack trace.

### Spinners

Sometimes you need to do some stuff that takes a while. You can just there
staring at a blinking cursor, or you can add a spinner for some nice feedback.
MILK includes more than 60 spinners thanks to
[halo](https://github.com/manrajgrover/halo).

To use it just instaniate `cli.spinner(text, spinner)`:

```
with cli.spinner(text="Hold on...", spinner="earth"):
    time.sleep(5)  # Or some other task that takes a long time
    cli.log.info('{fg_green}That was a nice nap')
```

This uses the same API as
[halo.Halo()](https://github.com/manrajgrover/halo#api) so you can refer to
that for more advanced usage.

### Subcommands

A lot of programs use a mode of operation where the first argument that
doesn't begin with `-` or `--` is a subcommand. Popular version control
programs such as `git` and `svn` are the most well known example of this
pattern. MILC uses argparser's native subcommand support to implement this
for you. To use it you designate functions as subcommand entrypoints using
`cli.subcommand`.

Let's extend our program from earlier to use subcommands:

```python
#!/usr/bin/env python
from milc import MILC

cli = MILC('Greet a user.')

@cli.argument('-n', '--name', help='Name to greet', default='World')
@cli.entrypoint
def main(cli):
    cli.log.info('No subcommand specified!')
    cli.print_usage()

@cli.subcommand
def hello(cli):
    cli.print('{fg_green}Hello, %s!', cli.config.general.name)

@cli.subcommand
def goodbye(cli):
    cli.print('{fg_blue}Goodbye, %s!', cli.config.general.name)

if __name__ == '__main__':
    cli()
```

### Configuration and Subcommands

Each subcommand gets its own section in the configuration. You can access a
subcommand's config with `cli.config.<subcommand>`. Options for the root
entrypoint can be found in the `cli.config.general` section of the config.

Let's finish up our program by adding some flags to hello and goodbye:

```python
#!/usr/bin/env python
from milc import MILC

cli = MILC('Greet a user.')

@cli.argument('-n', '--name', help='Name to greet', default='World')
@cli.entrypoint
def main(cli):
    cli.log.info('No subcommand specified!')
    cli.print_usage()

@cli.argument('--comma', help='comma in output', action='store_boolean', default=True)
@cli.subcommand
def hello(cli):
    comma = ',' if cli.config.hello.comma else ''
    cli.print('{fg_green}Hello%s %s!', comma, cli.config.general.name)

@cli.argument('-f', '--flag', help='Write it in a flag', action='store_true')
@cli.subcommand
def goodbye(cli):
    if cli.config.goodbye.flag:
        cli.log.debug('Drawing a flag.')
        colors = ('{bg_red}', '{bg_lightred_ex}', '{bg_lightyellow_ex}', '{bg_green}', '{bg_blue}', '{bg_magenta}')
        string = 'Goodbye, %s!' % cli.config.general.name
        for i, letter in enumerate(string):
            color = colors[i % len(colors)]
            cli.print(color + letter + ' '*39)
    else:
        cli.log.warning('Parting is such sweet sorrow.')
        cli.print('{fg_blue}Goodbye, %s!', cli.config.general.name)

if __name__ == '__main__':
    cli()
```

### Example Output

Now that we've written our program let's explore how it works, starting with
running it with no arguments.

![Simple Output](https://i.imgur.com/Ms3G8Aw.png)

We can demonstrate entering a subcommand here:

![Hello Output](https://i.imgur.com/a9RjE8S.png)

So far so good. Now let's take a look at the help output:

![Help Output](https://i.imgur.com/MR5TbHv.png)

Finally, let's combine it all together to demonstrate the use of both
general and subcommand flags:

![Flag Output](https://i.imgur.com/0aGFcKc.png)

## Doing More

Our program does a lot in only a few lines, but there's a lot more you can
do. Explore [the rest of the documentation](README.md) to see everything
MILC can do.
