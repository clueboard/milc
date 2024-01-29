<a id="milc"></a>

# milc

<a id="milc.MILC"></a>

## MILC Objects

```python
class MILC(object)
```

MILC - An Opinionated Batteries Included Framework

<a id="milc.MILC.__init__"></a>

#### \_\_init\_\_

```python
def __init__(name: Optional[str] = None,
             version: Optional[str] = None,
             author: Optional[str] = None,
             logger: Optional[logging.Logger] = None) -> None
```

Initialize the MILC object.

<a id="milc.MILC.argv_name"></a>

#### argv\_name

```python
def argv_name() -> str
```

Returns the name of our program by examining argv.

<a id="milc.MILC.echo"></a>

#### echo

```python
def echo(text: str, *args: Any, **kwargs: Any) -> None
```

Print colorized text to stdout.

ANSI color strings (such as {fg_blue}) will be converted into ANSI
escape sequences, and the ANSI reset sequence will be added to all
strings.

If *args or **kwargs are passed they will be used to %-format the strings.

<a id="milc.MILC.run"></a>

#### run

```python
def run(command: Sequence[str],
        capture_output: bool = True,
        combined_output: bool = False,
        text: bool = True,
        **kwargs: Any) -> Any
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

<a id="milc.MILC.initialize_argparse"></a>

#### initialize\_argparse

```python
def initialize_argparse() -> None
```

Prepare to process arguments from sys.argv.

<a id="milc.MILC.print_help"></a>

#### print\_help

```python
def print_help(*args: Any, **kwargs: Any) -> None
```

Print a help message for the main program or subcommand, depending on context.

<a id="milc.MILC.print_usage"></a>

#### print\_usage

```python
def print_usage(*args: Any, **kwargs: Any) -> None
```

Print brief description of how the main program or subcommand is invoked, depending on context.

<a id="milc.MILC.log_deprecated_warning"></a>

#### log\_deprecated\_warning

```python
def log_deprecated_warning(item_type: str, name: str, reason: str) -> None
```

Logs a warning with a custom message if a argument or command is deprecated.

<a id="milc.MILC.add_argument"></a>

#### add\_argument

```python
def add_argument(*args: Any, **kwargs: Any) -> None
```

Wrapper to add arguments and track whether they were passed on the command line.

<a id="milc.MILC.initialize_logging"></a>

#### initialize\_logging

```python
def initialize_logging(logger: Optional[logging.Logger]) -> None
```

Prepare the defaults for the logging infrastructure.

<a id="milc.MILC.acquire_lock"></a>

#### acquire\_lock

```python
def acquire_lock(blocking: bool = True) -> bool
```

Acquire the MILC lock for exclusive access to properties.

<a id="milc.MILC.release_lock"></a>

#### release\_lock

```python
def release_lock() -> None
```

Release the MILC lock.

<a id="milc.MILC.find_config_file"></a>

#### find\_config\_file

```python
@lru_cache(maxsize=None)
def find_config_file() -> Path
```

Locate the config file.

<a id="milc.MILC.argument"></a>

#### argument

```python
def argument(*args: Any, **kwargs: Any) -> Callable[..., Any]
```

Decorator to call self.add_argument or self.<subcommand>.add_argument.

<a id="milc.MILC.parse_args"></a>

#### parse\_args

```python
def parse_args() -> None
```

Parse the CLI args.

<a id="milc.MILC.read_config_file"></a>

#### read\_config\_file

```python
def read_config_file() -> Tuple[Configuration, Configuration]
```

Read in the configuration file and return Configuration objects for it and the config_source.

<a id="milc.MILC.initialize_config"></a>

#### initialize\_config

```python
def initialize_config() -> None
```

Read in the configuration file and store it in self.config.

<a id="milc.MILC.merge_args_into_config"></a>

#### merge\_args\_into\_config

```python
def merge_args_into_config() -> None
```

Merge CLI arguments into self.config to create the runtime configuration.

<a id="milc.MILC.write_config_option"></a>

#### write\_config\_option

```python
def write_config_option(section: str, option: Any) -> None
```

Save a single config option to the config file.

<a id="milc.MILC.save_config"></a>

#### save\_config

```python
def save_config() -> None
```

Save the current configuration to the config file.

<a id="milc.MILC.__call__"></a>

#### \_\_call\_\_

```python
def __call__() -> Any
```

Execute the entrypoint function.

<a id="milc.MILC.entrypoint"></a>

#### entrypoint

```python
def entrypoint(description: str,
               deprecated: Optional[str] = None) -> Callable[..., Any]
```

Decorator that marks the entrypoint used when a subcommand is not supplied.

**Arguments**:

  description
  A one-line description to display in --help
  
  deprecated
  Deprecation message. When set the subcommand will marked as deprecated and this message will be displayed in the help output.

<a id="milc.MILC.add_subcommand"></a>

#### add\_subcommand

```python
def add_subcommand(handler: Callable[..., Any],
                   description: str,
                   hidden: bool = False,
                   deprecated: Optional[str] = None,
                   **kwargs: Any) -> Callable[..., Any]
```

Register a subcommand.

**Arguments**:

  
  handler
  The function to exececute for this subcommand.
  
  description
  A one-line description to display in --help
  
  hidden
  When True don't display this command in --help
  
  deprecated
  Deprecation message. When set the subcommand will be marked as deprecated
  and this message will be displayed in help output.

<a id="milc.MILC.subcommand"></a>

#### subcommand

```python
def subcommand(description: str,
               hidden: bool = False,
               **kwargs: Any) -> Callable[..., Any]
```

Decorator to register a subcommand.

**Arguments**:

  
  description
  A one-line description to display in --help
  
  hidden
  When True don't display this command in --help

<a id="milc.MILC.setup_logging"></a>

#### setup\_logging

```python
def setup_logging() -> None
```

Called by __enter__() to setup the logging configuration.

<a id="milc.MILC.is_spinner"></a>

#### is\_spinner

```python
def is_spinner(name: str) -> bool
```

Returns true if name is a valid spinner.

<a id="milc.MILC.add_spinner"></a>

#### add\_spinner

```python
def add_spinner(name: str, spinner: Dict[str, Union[int,
                                                    Sequence[str]]]) -> None
```

Adds a new spinner to the list of spinners.

A spinner is a dictionary with two keys:

    interval
        An integer that sets how long (in ms) to wait between frames.

    frames
        A list of frames for this spinner

<a id="milc.MILC.spinner"></a>

#### spinner

```python
def spinner(text: str,
            *args: Any,
            spinner: Optional[str] = None,
            animation: str = 'ellipsed',
            placement: str = 'left',
            color: str = 'blue',
            interval: int = -1,
            stream: Any = sys.stdout,
            enabled: bool = True,
            **kwargs: Any) -> Halo
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

