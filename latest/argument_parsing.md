# Argument Parsing

MILC exposes the full power of [argparse](https://docs.python.org/3/library/argparse.html) to you. It also extends argparse to make certain commonly used patterns easier to use.

# Reading Arguments

In most cases you will want to use [`cli.config`](configuration.md) to read your argument. For example:

    cli.config.general.verbose

In some cases (such as [`arg_only`](#arg_only)) you will need to access the arguments directly using `cli.args`. You can access these using either attribute or dictionary notation:

Attribute:

    cli.args.verbose

Dictionary:

    cli.args['verbose']

# Defining arguments

## Argument Decorators

Argument decorators (`@argument()`) are used to define command line flags that the user has passed. For the most part the arguments passed to this decorator are passed to [`ArgumentParser.add_argument()`](https://docs.python.org/3/library/argparse.html#the-add-argument-method) directly. As such you can use all of those method arguments with MILC's `@argument()` decorator.

### arg_only

Sometimes you want an argument to be a CLI flag only, and to not have a corresponding configuration option. With `arg_only=True` in your `@argument()` decorator this is possible. You will have to look in `cli.args` to find the value of that flag, it will not be populated to `cli.config`.

### completers

You can specify [argcomplete completers](https://kislyuk.github.io/argcomplete/#specifying-completers) for your arguments by passing `completers`. For more detail see the [argcomplete](argcomplete.md) page.

### deprecated

You can use the `deprecated` argument to mark a flag as deprecated. To use this you should set it to a string that will be displayed in --help. For example:

    @argument('--old', action='store_true', deprecated='Use --new instead', help='The old action for my command.')

This will result in the following help output:

    --old       The old action for my command. [Deprecated]: Use --new instead

### action: store_boolean

In addition to the normal set of `action=` arguments that you can pass to `@argument()`, you can also pass a new action called `store_boolean`. This action behaves like `store_true` except that it adds a corresponding `--no-<argument>` flag that the user can pass as well.
