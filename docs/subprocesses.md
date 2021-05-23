# Executing commands in a subprocess

MILC provides some tools to make running subcommands easier and more convienent to work with.

## Basic Subprocess Execution

You can use `cli.run()` to easily and safely run shell commands. The first argument to `cli.run()` should be an argument list, which is a list or tuple containing the command and any arguments you want to pass in. For example, if you wanted to run a git command you might build this argument list:

```python
git_cmd = ['git', '-C', '/srv/web/htdocs', 'pull']
```

This is all you need to do to run that command:

```python
p = cli.run(git_cmd)
```

This will return a [subprocess.CompletedProcess](https://docs.python.org/3/library/subprocess.html#subprocess.CompletedProcess) instance. You can examine attributes such as `p.returncode`, `p.stderr`, and `p.stdout` to see the fate of the process.

## Supported Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `command` | | A sequence of arguments for the command to be run. The first element is the command to be executed. |
| `capture_output` | `True` | When `False` output from the subprocess is written directly to STDOUT and STDERR. |
| `combined_output` | `False` | When `True` STDERR will be combined with STDOUT. |
| `text` | `True` | When `False` STDOUT and STDERR will return binary data. |
| `**kwargs` |  | Any unrecognized argument will be passed to `subprocess.run()` |

## Differences from subprocess.run

MILC's `cli.run()` differs from `subprocess.run()` in some important ways. 

### Windows Support

When running inside a windows console (Powershell, DOS, Cygwin, Msys2) there are some quirks that MILC attempts to handle but which you need to be aware of:

* Commands are always run in a subshell, so that non-executable files and POSIX paths work seemlessly.
* Windows leaves stdin in a broken state after executing a subprocess. To avoid this MILC adds `stdin=DEVNULL` to the `subprocess.run()` call. If you need stdin to work in your executed process you can pass `stdin=None`.

### Building argument lists

The most important way MILC differs from `subprocess.run()` is that it only accepts commands that have already been split into sequences. A lot of bugs are caused by mistakes in building command strings that are later split into a sequence of arguments in unexpected ways.

### Capture Output

By default `cli.run()` captures STDOUT and STDERR. If you'd like that output to be written to the terminal instead you can pass `capture_output=False`.

### Combining STDERR with STDOUT

If you'd like to combine STDOUT and STDERR into one stream (similar to the shell construct `2>&1`) you can pass `combined_output=True`.

### Text Encoding

By default STDOUT and STDERR will be opened as text. If you'd like these to be bytes instead of text you can pass `text=False`.

### Other Arguments

All other arguments are passed directly to [`subprocess.run()`](https://docs.python.org/3/library/subprocess.html#subprocess.run). You can use these to further tweak the behavior of your subprocesses.
