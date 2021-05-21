<a name="milc"></a>
# milc

<a name="milc.MILC"></a>
## MILC Objects

```python
class MILC(object)
```

MILC - An Opinionated Batteries Included Framework

<a name="milc.MILC.__init__"></a>
#### \_\_init\_\_

```python
 | __init__(name, version, author)
```

Initialize the MILC object.

<a name="milc.MILC.echo"></a>
#### echo

```python
 | echo(text, *args, **kwargs)
```

Print colorized text to stdout.

ANSI color strings (such as {fg_blue}) will be converted into ANSI
escape sequences, and the ANSI reset sequence will be added to all
strings.

If *args or **kwargs are passed they will be used to %-format the strings.

<a name="milc.MILC.run"></a>
#### run

```python
 | run(command, capture_output=True, combined_output=False, text=True, **kwargs)
```

Run a command using `subprocess.run`, but using some different defaults.

Unlike subprocess.run you must supply a sequence of arguments. You can use `shlex.split()` to build this from a string.

The **kwargs arguments get passed directly to `subprocess.run`.

**Arguments**:

  command
  A sequence where the first item is the command to run, and any remaining items are arguments to pass.
  
  capture_output
  Set to False to have output written to the terminal instead of being available in the returned `subprocess.CompletedProcess` instance.
  
  combined_output
  When true STDERR will be written to STDOUT. Equivalent to the shell construct `2>&1`.
  
  text
  Set to False to disable encoding and get `bytes()` from `.stdout` and `.stderr`.

<a name="milc.MILC.initialize_argparse"></a>
#### initialize\_argparse

```python
 | initialize_argparse()
```

Prepare to process arguments from sys.argv.

<a name="milc.MILC.print_help"></a>
#### print\_help

```python
 | print_help(*args, **kwargs)
```

Print a help message for the main program or subcommand, depending on context.

<a name="milc.MILC.print_usage"></a>
#### print\_usage

```python
 | print_usage(*args, **kwargs)
```

Print brief description of how the main program or subcommand is invoked, depending on context.

<a name="milc.MILC.add_argument"></a>
#### add\_argument

```python
 | add_argument(*args, **kwargs)
```

Wrapper to add arguments and track whether they were passed on the command line.

<a name="milc.MILC.initialize_logging"></a>
#### initialize\_logging

```python
 | initialize_logging()
```

Prepare the defaults for the logging infrastructure.

<a name="milc.MILC.acquire_lock"></a>
#### acquire\_lock

```python
 | acquire_lock(blocking=True)
```

Acquire the MILC lock for exclusive access to properties.

<a name="milc.MILC.release_lock"></a>
#### release\_lock

```python
 | release_lock()
```

Release the MILC lock.

<a name="milc.MILC.find_config_file"></a>
#### find\_config\_file

```python
 | find_config_file()
```

Locate the config file.

<a name="milc.MILC.argument"></a>
#### argument

```python
 | argument(*args, **kwargs)
```

Decorator to call self.add_argument or self.<subcommand>.add_argument.

<a name="milc.MILC.parse_args"></a>
#### parse\_args

```python
 | parse_args()
```

Parse the CLI args.

<a name="milc.MILC.read_config_file"></a>
#### read\_config\_file

```python
 | read_config_file(config_file)
```

Read in the configuration file and return Configuration objects for it and the config_source.

<a name="milc.MILC.initialize_config"></a>
#### initialize\_config

```python
 | initialize_config()
```

Read in the configuration file and store it in self.config.

<a name="milc.MILC.merge_args_into_config"></a>
#### merge\_args\_into\_config

```python
 | merge_args_into_config()
```

Merge CLI arguments into self.config to create the runtime configuration.

<a name="milc.MILC.write_config_option"></a>
#### write\_config\_option

```python
 | write_config_option(section, option)
```

Save a single config option to the config file.

<a name="milc.MILC.save_config"></a>
#### save\_config

```python
 | save_config()
```

Save the current configuration to the config file.

<a name="milc.MILC.__call__"></a>
#### \_\_call\_\_

```python
 | __call__()
```

Execute the entrypoint function.

<a name="milc.MILC.entrypoint"></a>
#### entrypoint

```python
 | entrypoint(description)
```

Decorator that marks the entrypoint used when a subcommand is not supplied.

<a name="milc.MILC.add_subcommand"></a>
#### add\_subcommand

```python
 | add_subcommand(handler, description, hidden=False, **kwargs)
```

Register a subcommand.

**Arguments**:

  
  handler
  The function to exececute for this subcommand.
  
  description
  A one-line description to display in --help
  
  hidden
  When True don't display this command in --help

<a name="milc.MILC.subcommand"></a>
#### subcommand

```python
 | subcommand(description, hidden=False, **kwargs)
```

Decorator to register a subcommand.

**Arguments**:

  
  description
  A one-line description to display in --help
  
  hidden
  When True don't display this command in --help

<a name="milc.MILC.setup_logging"></a>
#### setup\_logging

```python
 | setup_logging()
```

Called by __enter__() to setup the logging configuration.

<a name="milc.MILC.is_spinner"></a>
#### is\_spinner

```python
 | is_spinner(name)
```

Returns true if name is a valid spinner.

<a name="milc.MILC.add_spinner"></a>
#### add\_spinner

```python
 | add_spinner(name, spinner)
```

Adds a new spinner to the list of spinners.

A spinner is a dictionary with two keys:

    interval
        An integer that sets how long (in ms) to wait between frames.

    frames
        A list of frames for this spinner

<a name="milc.MILC.spinner"></a>
#### spinner

```python
 | spinner(text, *args, *, spinner=None, animation='ellipsed', placement='left', color='blue', interval=-1, stream=sys.stdout, enabled=True, **kwargs)
```

Create a spinner object for showing activity to the user.

This uses halo <https://github.com/ManrajGrover/halo> behind the scenes, most of the arguments map to Halo objects 1:1.

There are 3 basic ways to use this:

* Instantiating a spinner and then using `.start()` and `.stop()` on your object.
* Using a context manager (`with cli.spinner(...):`)
* Decorate a function (`@cli.spinner(...)`)

#### Instantiating a spinner

```python
spinner = cli.spinner(text='Loading', spinner='dots')
spinner.start()

# Do something here

spinner.stop()
```

#### Using a context manager

```python
with cli.spinner(text='Loading', spinner='dots'):
    # Do something here
```

#### Decorate a function

```python
@cli.spinner(text='Loading', spinner='dots')
def long_running_function():
    # Do something here
```

### Arguments

    text
        The text to display next to the spinner. ANSI color strings
        (such as {fg_blue}) will be converted into ANSI escape
        sequences, and the ANSI reset sequence will be added to the
        end of the string.

        If *args or **kwargs are passed they will be used to
        %-format the text.

    spinner
        The name of the spinner to use. Available names are here:
        <https://raw.githubusercontent.com/sindresorhus/cli-spinners/dac4fc6571059bb9e9bc204711e9dfe8f72e5c6f/spinners.json>

    animation
        The animation to apply to the text if it doesn't fit the
        terminal. One of `ellipsed`, `bounce`, `marquee`.

    placement
        Which side of the text to display the spinner on. One of
        `left`, `right`.

    color
        Color of the spinner. One of `blue`, `grey`, `red`, `green`,
        `yellow`, `magenta`, `cyan`, `white`

    interval
        How long in ms to wait between frames. Defaults to the spinner interval (recommended.)

    stream
        Stream to write the output. Defaults to sys.stdout.

    enabled
        Enable or disable the spinner. Defaults to `True`.

