# Configuration

MILC supports a config file out of the box. The format and structure of this file is exposed through `cli.config` and tied to command line arguments. If your program uses subcommands you can add a `config` subcommand with a single import.

# Structure

MILC uses [ConfigParser](https://docs.python.org/3/library/configparser.html) to store configuration values. We've mapped the section names to subcommands, and values passed as CLI arguments will be automatically populated to keys named after the argument.

Configuration options for the main `cli.entrypoint()` are set in `cli.config.general`. If you do not have any subcommands you will find all of your config options here.

For nested subcommands (e.g. `prog remote add`), configuration sections mirror the command path:

```python
cli.config.remote.add.url        # attribute access
cli.config['remote']['add']['url']  # dict access
```

# Reading Config Values

You can read config values using either attribute or dictionary notation. If a key does not exist in the configuration you will get `None` as the value.

Attribute:

    cli.config.general.verbose

Dictionary:

    cli.config['general']['verbose']

# Setting Config Values

You can create new values by simply assigning to them. This only works with dictionary notation.

    cli.config['general']['verbose'] = True

# Writing Configuration Files

Use `cli.save_config()` to save the user's configuration file. It will be written to the location specified by `cli.config_file`.

# Configuration File Location

MILC uses [platformdirs](https://github.com/tox-dev/platformdirs) to determine the configuration file location. You can set your application's name and author by using `cli.milc_options()`:

```python
from milc import cli

cli.milc_options(name='Florzelbop', version='1.0.0', author='Jane Doe')
```

This will (usually) result in the following config file locations:

* Linux: `~/.config/Florzelbop`
* macOS: `~/Library/Application Support/Florzelbop`
* Windows: `C:\Users\<User>\AppData\Local\Florzelbop\Florzelbop`

# Where Did A Value Come From?

Sometimes you need to know how a configuration value was set. You can use `cli.config_source` to find out.


    >>> cli.config_source.general.verbose
    'argument'

The possible values returned are:

* `'argument'`
  * The value was passed as a CLI argument
* `'env_var'`
  * The value was read from an environment variable (see [Environment Variables](environment_variables.md))
* `'config_file'`
  * The value was read from the config file
* `None`
  * The value is the argument default

# Automatic Type Inference

Under the hood all configuration options are stored as plain text. MILC converts your config values into appropriate data types when it can figure out how.

* Booleans
    * `yes`, `true`, and `on` evaluate to True.
    * `no`, `false`, and `off` evaluate to False.
* None
    * Values set to None are considered deleted, and will be removed from the config file
* Integers
    * Numbers without a decimal are converted to `int()`
* Decimal Numbers
    * Numbers with a decimal are converted to `decimal.Decimal()`
