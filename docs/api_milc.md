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
 | __init__()
```

Initialize the MILC object.

version
    The version string to associate with your CLI program

<a name="milc.MILC.echo"></a>
#### echo

```python
 | echo(text, *args, **kwargs)
```

Print colorized text to stdout.

ANSI color strings (such as {fg-blue}) will be converted into ANSI
escape sequences, and the ANSI reset sequence will be added to all
strings.

If *args or **kwargs are passed they will be used to %-format the strings.

<a name="milc.MILC.run"></a>
#### run

```python
 | run(command, *args, **kwargs)
```

Run a command with subprocess.run

The *args and **kwargs arguments get passed directly to `subprocess.run`.

<a name="milc.MILC.initialize_argparse"></a>
#### initialize\_argparse

```python
 | initialize_argparse()
```

Prepare to process arguments from sys.argv.

<a name="milc.MILC.completer"></a>
#### completer

```python
 | completer(completer)
```

Add an argcomplete completer to this subcommand.

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

Set the entrypoint for when no subcommand is provided.

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

