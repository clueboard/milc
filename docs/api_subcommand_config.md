<a id="subcommand.config"></a>

# subcommand.config

Read and write configuration settings

<a id="subcommand.config.print_config"></a>

#### print\_config

```python
def print_config(section, key)
```

Print a single config setting to stdout.

<a id="subcommand.config.show_config"></a>

#### show\_config

```python
def show_config()
```

Print the current configuration to stdout.

<a id="subcommand.config.parse_config_token"></a>

#### parse\_config\_token

```python
def parse_config_token(config_token)
```

Split a user-supplied configuration-token into its components.

<a id="subcommand.config.set_config"></a>

#### set\_config

```python
def set_config(section, option, value)
```

Set a config key in the running config.

<a id="subcommand.config.config"></a>

#### config

```python
@milc.cli.argument('-a',
                   '--all',
                   action='store_true',
                   help='Show all configuration options.')
@milc.cli.argument('-ro',
                   '--read-only',
                   arg_only=True,
                   action='store_true',
                   help='Operate in read-only mode.')
@milc.cli.argument('configs',
                   nargs='*',
                   arg_only=True,
                   help='Configuration options to read or write.')
@milc.cli.subcommand("Read and write configuration settings.")
def config(cli)
```

Read and write config settings.

This script iterates over the config_tokens supplied as argument. Each config_token has the following form:

    section[.key][=value]

If only a section (EG 'compile') is supplied all keys for that section will be displayed.

If section.key is supplied the value for that single key will be displayed.

If section.key=value is supplied the value for that single key will be set.

If section.key=None is supplied the key will be deleted.

No validation is done to ensure that the supplied section.key is actually used by a subcommand.

