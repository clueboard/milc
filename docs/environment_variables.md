# Environment Variables

MILC can automatically populate argument values from environment variables. This lets users configure your program without passing flags every time, while still allowing CLI flags to override them.

# Enabling env_prefix

Set `env_prefix` in `cli.milc_options()` to opt in:

```python
from milc import cli

cli.milc_options(name='myapp', env_prefix='MYAPP')
```

This maps each `--flag` to an environment variable named `<PREFIX>_<FLAG>` (uppercase, hyphens replaced with underscores). For example, `--host` maps to `MYAPP_HOST`.

# Priority Order

When `env_prefix` is set, values are resolved in this order (highest to lowest):

1. Command-line argument (`--host myhost`)
2. Environment variable (`MYAPP_HOST=myhost`)
3. Config file (`[general] host = myhost`)
4. Default value

# Basic Example

```python
from milc import cli

cli.milc_options(name='myapp', env_prefix='MYAPP')

@cli.argument('--host', required=True, help='Hostname')
@cli.argument('--port', type=int, default=8080, help='Port number')
@cli.entrypoint('Start the server.')
def main(cli):
    cli.echo('Connecting to %s:%s', cli.config.general.host, cli.config.general.port)

if __name__ == '__main__':
    cli()
```

With this setup, all of these are equivalent:

```sh
# CLI flag
myapp --host db.example.com

# Environment variable
MYAPP_HOST=db.example.com myapp

# Config file
myapp config general.host=db.example.com
```

# Type Coercion

Environment variable values are always strings. MILC coerces them using the `type=` function from the argument definition:

```python
@cli.argument('--port', type=int, default=8080, help='Port number')
```

```sh
MYAPP_PORT=9090 myapp --host db.example.com
# cli.config.general.port == 9090  (int, not str)
```

If the value cannot be coerced, MILC exits with a readable error message:

```
error: environment variable MYAPP_PORT='notanumber' is not the correct type: invalid literal for int() with base 10: 'notanumber'
```

# Boolean Flags

`store_true` arguments accept truthy/falsy string values:

| Value | Result |
|-------|--------|
| `true`, `yes`, `1`, `on` | `True` |
| `false`, `no`, `0`, `off`, `-1`, `` | `False` |

```python
@cli.argument('--verbose', action='store_true', help='Verbose mode')
```

```sh
MYAPP_VERBOSE=true myapp --host db.example.com   # verbose=True
MYAPP_VERBOSE=false myapp --host db.example.com  # verbose=False
```

`store_false` arguments are not mapped to environment variables.

# Unsupported Argument Types

The following argument types are not supported and will silently ignore any matching environment variable:

* `store_false` — the `--no-X` half of `store_boolean` pairs
* `nargs='+'` / `nargs='*'` / `nargs='?'` / `nargs=argparse.REMAINDER` / `nargs=N` — `nargs='?'` is excluded because passing the flag with no value should use `const`, not the env var, and that distinction cannot be made reliably; the others cannot be reliably split from a single string
* `action='append'` — each env var value would become a string element rather than extending a list correctly

# Subcommand Scoping

Environment variables for subcommand arguments are scoped using the subcommand name as an additional prefix:

```
<PREFIX>_<SUBCOMMAND>_<FLAG>
```

```python
cli.milc_options(name='myapp', env_prefix='MYAPP')

@cli.argument('--host', default='global-default', help='Global hostname')
@cli.entrypoint('My app.')
def main(cli):
    cli.echo('host=%s', cli.config.general.host)

@cli.argument('--host', default='subc-default', help='Subcommand hostname')
@cli.subcommand('A subcommand.')
def deploy(cli):
    cli.echo('host=%s', cli.config.deploy.host)
```

| Env var | Affects |
|---------|---------|
| `MYAPP_HOST` | `--host` on the entrypoint |
| `MYAPP_DEPLOY_HOST` | `--host` on the `deploy` subcommand |

The two env vars are independent. `MYAPP_HOST` does not affect `deploy --host`, and vice versa.

# Empty Prefix

Setting `env_prefix=''` consults environment variables without any prefix:

```python
cli.milc_options(name='myapp', env_prefix='')
```

With this setting, `--host` maps to the env var `HOST`.

!!! warning
    An empty prefix maps flags to short, generic names (`HOST`, `PORT`, `USER`, `PATH`, etc.) that frequently collide with variables already set in the shell environment. For example, `USER` and `PATH` are set by virtually every shell session. Prefer a meaningful prefix like `MYAPP` to avoid silent, hard-to-diagnose value injection.

# Checking Provenance

Use `cli.config_source` to determine where a value came from:

```python
cli.config_source.general.host  # 'argument', 'env_var', 'config_file', or None
```

See [Configuration](configuration.md#where-did-a-value-come-from) for details.
