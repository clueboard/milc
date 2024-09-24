<a id="milc_interface"></a>

# milc\_interface

Public interface for MILC.

This is where the public interface for `cli` is kept. This allows us to reinstantiate MILC without having to recreate the cli object, as well as allowing us to have a well defined public API.

<a id="milc_interface.MILCInterface"></a>

## MILCInterface Objects

```python
class MILCInterface()
```

<a id="milc_interface.MILCInterface.echo"></a>

#### echo

```python
def echo(text: str, *args: Any, **kwargs: Any) -> None
```

Print colorized text to stdout.

ANSI color strings (such as {fg_blue}) will be converted into ANSI
escape sequences, and the ANSI reset sequence will be added to all
strings.

If *args or **kwargs are passed they will be used to %-format the strings.

<a id="milc_interface.MILCInterface.run"></a>

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

<a id="milc_interface.MILCInterface.print_help"></a>

#### print\_help

```python
def print_help(*args: Any, **kwargs: Any) -> None
```

Print a help message for the main program or subcommand, depending on context.

<a id="milc_interface.MILCInterface.print_usage"></a>

#### print\_usage

```python
def print_usage(*args: Any, **kwargs: Any) -> None
```

Print brief description of how the main program or subcommand is invoked, depending on context.

<a id="milc_interface.MILCInterface.add_argument"></a>

#### add\_argument

```python
def add_argument(*args: Any, **kwargs: Any) -> None
```

Wrapper to add arguments and track whether they were passed on the command line.

<a id="milc_interface.MILCInterface.acquire_lock"></a>

#### acquire\_lock

```python
def acquire_lock(blocking: bool = True) -> bool
```

Acquire the MILC lock for exclusive access to properties.

<a id="milc_interface.MILCInterface.release_lock"></a>

#### release\_lock

```python
def release_lock() -> None
```

Release the MILC lock.

<a id="milc_interface.MILCInterface.argument"></a>

#### argument

```python
def argument(*args: Any, **kwargs: Any) -> Callable[..., Any]
```

Decorator to add an argument to a MILC command or subcommand.

<a id="milc_interface.MILCInterface.save_config"></a>

#### save\_config

```python
def save_config() -> None
```

Save the current configuration to the config file.

<a id="milc_interface.MILCInterface.__call__"></a>

#### \_\_call\_\_

```python
def __call__() -> Any
```

Execute the entrypoint function.

<a id="milc_interface.MILCInterface.entrypoint"></a>

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

<a id="milc_interface.MILCInterface.subcommand"></a>

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

<a id="milc_interface.MILCInterface.add_spinner"></a>

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

<a id="milc_interface.MILCInterface.spinner"></a>

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

