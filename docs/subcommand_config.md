# MILC config subcommand

This document explains how the available `config` subcommand works.

# Introduction

Configuration for MILC applications is a key/value system. Each key consists of a subcommand and an argument name separated by a period. This allows for a straightforward and direct translation between config keys and the arguments they set. You can provide your users with a subcommand for managing this configuration by importing the config subcommand:

`import milc.subcommand.config`

Read on to see how users can utilize this subcommand.

## Simple Example

As an example let's look at the command `my_cli foo --arg1 bar --arg2 bat`.

There are two command line arguments that could be read from configuration instead:

* `foo.arg1`
* `foo.arg2`

Let's set these now:

```
$ my_cli config foo.arg1=bar foo.arg2=bat
foo.arg1 None -> bar
foo.arg2 None -> bat
i Wrote configuration to '/Users/example/Library/Application Support/my_cli/my_cli.ini'
```

Now I can run `my_cli foo` without specifying `--arg1` and `--arg2` each time.

## Setting User Defaults

Sometimes you want to share a setting between multiple subcommands. For example, multiple commands take the argument `--arg1`. Rather than setting this value for every command you can set a user value which will be used by any command that takes that argument.

Example:

```
$ my_cli config user.arg1=baz
user.arg1: None -> baz
ℹ Wrote configuration to '/Users/example/Library/Application Support/my_cli/my_cli.ini'
```

# Subcommand reference (`config`)

The `config` subcommand is used to interact with the underlying configuration. When run with no argument it shows the current configuration. When arguments are supplied they are assumed to be configuration tokens, which are strings containing no spaces with the following form:

    <subcommand|general|default>[.<key>][=<value>]

## Setting Configuration Values

You can set configuration values by putting an equal sign (=) into your config key. The key must always be the full `<section>.<key>` form.

Example:

```
$ my_cli config default.arg1=default
default.arg1: None -> default
ℹ Wrote configuration to '/Users/example/Library/Application Support/my_cli/my_cli.ini'
```

## Reading Configuration Values

You can read configuration values for the entire configuration, a single key, or for an entire section. You can also specify multiple keys to display more than one value.

### Entire Configuration Example

    my_cli config

### Whole Section Example

    my_cli config general

### Single Key Example

    my_cli config general.verbose

### Multiple Keys Example

    my_cli config user general.verbose general.log_format

## Deleting Configuration Values

You can delete a configuration value by setting it to the special string `None`.

Example:

```
$ my_cli config general.log_format None
general.log_format: %H:%M:%S -> None
ℹ Wrote configuration to '/Users/example/Library/Application Support/my_cli/my_cli.ini'
```

## Multiple Operations

You can combine multiple read and write operations into a single command. They will be executed and displayed in order:

```
$ my_cli config foo user.arg1=default foo.arg2=None
foo.arg3=peep
user.arg1: None -> default
foo.arg2: bar -> None
ℹ Wrote configuration to '/Users/example/Library/Application Support/my_cli/my_cli.ini'
```
