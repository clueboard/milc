# Executing commands in a subprocess

MILC provides some tools to make running subcommands easier and more convienent to work with.

## Basic Subprocess Execution

You can use `cli.run()` to easily and safely run shell commands. The first argument to `cli.run()` should be an argument list, which is a list or tuple containing the command and any arguments you want to pass in. For example, if you wanted to run a git command you might build this argument list:

```python
git_cmd = ['git', '-C', '/srv/web/htdocs', 'pull']
```

This is all you need to do to run a that command:

```python
p = cli.run(git_cmd)
```

This will return a [subprocess.CompletedProcess](https://docs.python.org/3/library/subprocess.html#subprocess.CompletedProcess) instance. You can examine attributes such as `p.returncode`, `p.stderr`, and `p.stdout` to see the fate of the process.

## Tweaking behavior

MILC's `cli.run()` differs from `subprocess.run()` in some important ways. 

### Building argument lists

The most important way is that MILC only accepts commands that have already been split into sequences. A lot of bugs are caused by mistakes in building command strings that are later split into a sequence of arguments in unexpected ways.

### Capture Output

By default `cli.run()` captures STDOUT and STDERR. If you'd like that output to be written to the terminal instead you can pass `capture_output=False`.

### Combine STDERR with STDOUT

If you'd like to combine STDOUT and STDERR into one stream (similar to the shell construct `2>&1`) you can pass `combined_output=True`.

### Text Encoding

By default STDOUT and STDERR will be opened as text. If you'd like these to be bytes instead of text you can pass `text=False`.

### Other Arguments

All other arguments are passed directly to [`subprocess.run()`](https://docs.python.org/3/library/subprocess.html#subprocess.run). You can use these to further tweak the behavior of your subprocesses.
