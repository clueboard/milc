# Configuration

MILC supports a config file out of the box. The format and structure of this file is exposed through `cli.config` and tied to command line arguments. If your program uses subcommands you can add a `config` subcommand with a single import.

# Structure

MILC uses [ConfigParser](https://docs.python.org/3/library/configparser.html) to store configuration values. We've mapped the section names to subcommands, and values passed as CLI arguments will be automatically populated to keys named after the argument.

Configuration options for the main `cli.entrypoint()` are set in `cli.config.general`. If you do not have any subcommands you will find all of your config options here.

# Reading Config Values

You can read config values using either attribute or dictionary notation. If a key does not exist in the configuration you will get `None` as the value.

Attribute:

    cli.config.general.verbose

Dictionary:

    cli.config['general']['verbose']

# Setting Config Values

You can create new values by simply assigning to them. This only with dictionary notation.

    cli.config['general']['verbose'] = True

# Writing Configuration Files

Use `cli.save_config()` to save the user's configuration file. It will be written to the location specified by `cli.config_file`.

# Configuration File Location

MILC uses [appdirs](https://github.com/ActiveState/appdirs) to determine the configuration file location. You can set your application's name and author by using `milc.set_metadata`:

```python
from milc import set_metadata

set_metadata('Florzelbop', '1.0.0', 'Jane Doe')
```

This will (usually) result in the following config file locations:

* Linux: `~/.local/share/Florzelbop`
* macOS: `~/Library/Application Support/Florzelbop`
* Windows: `C:\Documents and Settings\<User>\Application Data\Local Settings\Florzelbop Jane Doe\hello`

# Where Did A Value Come From?

Sometimes you need to know how a configuration value was set. You can use `cli.config_source` to find out.


    >>> cli.config_source.general.verbose
    'argument'

The possible values returned are:

* `'argument'`
  * The value was passed as an argument
* `'config_file'`
  * The value was read from the config file
* `'default'`
  * This is the default value

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
