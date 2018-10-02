"""py-clim - The CLI Context Manager
"""
from __future__ import division, print_function, unicode_literals
import argparse
import logging

class CLIM(object):
    """# CLI Context Manager

    CLIM is an opinionated framework for writing CLI apps. It optimizes for
    the most common unix tool pattern- small tools that are run from the
    command line but generally do not feature any user interaction while they
    run.

    This class wraps some standard python modules in nice ways for CLI tools.
    It provides a Context Manager that can be used to quickly and easily
    write tools that behave in the way endusers expect. It's meant to lightly
    wrap standard python modules with just enough framework to make writing
    simple scripts simple while allowing you to organically grow into large
    complex programs with hundreds of options.

    ## Simple Example:

        cli = CLIM('My useful CLI tool.')

        @cli.argument('-n', '--name', help='Name to greet', default='World')
        @cli.entrypoint
        def main(cli):
            cli.log.info('Hello, %s!', cli.args.name)

        if __name__ == '__main__':
            with cli:
                cli.run()

    # Basics of a CLIM app

    Start by instaniating a CLIM context manager and defining your entrypoint:

        cli = CLIM('My useful CLI tool')

        def main(cli):
            print('Hello, %s!' % cli.args.name)

    From here, you should setup your CLI environment. I typically prefer to
    do this behind a __main__ check.

        if __name__ == '__main__':
            cli.entrypoint(main)
            cli.add_argument('-n', '--name', help='Name to greet', default='World')

    Finally, invoke it as a context manager and use `cli.run()` to dispatch to
    your entrypoint (or a subcommand, if one has been specified.)

            with cli:
                cli.run()

    ## Complete CLIM script, using functions

        cli = CLIM('My useful CLI tool')

        def main(cli):
            print('Hello, %s!' % cli.args.name)

        if __name__ == '__main__':
            cli.entrypoint(main)
            cli.add_argument('-n', '--name', help='Name to greet', default='World')

            with cli:
                cli.run()

    # Using decorators instead

    If you prefer you can use decorators instead. This can help as your program
    grows by keeping the definition of arguments near the relevant entrypoint.
    Not that due to the way decorators are evaluated you need to place all
    `@cli.argument()` decorators above all other decorators.

        cli = CLIM('My useful CLI tool')

        @cli.argument('-n', '--name', help='Name to greet', default='World')
        @cli.entrypoint
        def main(cli):
            print('Hello, %s!' % cli.args.name)

        if __name__ == '__main__':
            with cli:
                cli.run()

    # Using Subcommands

    A command pattern for CLI tools is to have subcommands. For example,
    you see this in git with `git status` and `git pull`. CLIM supports
    this pattern using the built-in argparse subcommand functionality.

    You can register subcommands by using the `cli.subcommand(func)`
    function, or by decorating functions with `@cli.subcommand`. In
    either case the subcommand name will be the same as the name of the
    function.

    You can access the underlying subcommand instance in two ways-

        * Attribute access (`cli.<subcommand>`)
        * Dictionary access (`cli.subcommands['<subcommand>']`)

    You should generally prefer the attribute access. If there is a conflict
    with an existing attribute or the name is not a legal attribute name you
    will have to access it via the dictionary.

    When subcommands are not in use `cli.run()` will always be the same as
    `cli.entrypoint()`. When subcommands are in use `cli.run()` will be
    pointed to the proper command to run. If no valid subcommand is given on
    the command line it will point to `cli.entrypoint()`. If a valid
    subcommand is supplied it will point to `<subcommand>()`.

    Note: Python 2 does not support calling @cli.entrypoint when subcommands
    are in use. If you need to call @cli.entrypoint when a subcommand is not
    specified you will need to use python 3.

    ## Subcommand Example

        cli = CLIM('My useful CLI tool with subcommands.')

        @cli.argument('-c', '--comma', help='Include the comma in output', action='store_true')
        @cli.entrypoint
        def main(cli):
            cli.log.info('Hello%s World!', cli.args.comma)

        @cli.argument('-n', '--name', help='Name to greet', default='World')
        @cli.subcommand
        def hello(cli):
            '''Description of hello subcommand here.'''
            cli.log.info('Hello%s %s!', cli.args.comma, cli.args.name)

        def goodbye(cli):
            '''This will show up in --help output.'''
            cli.log.info('Goodbye%s %s!', cli.args.comma, cli.args.name)

        if __name__ == '__main__':
            # You can register subcommands using decorators as seen above,
            # or using functions like like this:
            cli.subcommand(goodbye)
            cli.goodbye.add_argument('-n', '--name', help='Name to bid farewell to', default='World')

            with cli:
                cli.args.comma = ',' if cli.args.comma else ''
                cli.run()  # Automatically picks between main(), hello() and goodbye()

    # More Docs!

    Details about the rest of the system can be found in the [docs/](docs/) directory.
    """
    def __init__(self, description, entrypoint=None, fromfile_prefix_chars='@', conflict_handler='resolve', **kwargs):
        self._entrypoint = entrypoint
        self._inside_context_manager = False

        # Setup argument handling
        kwargs['fromfile_prefix_chars'] = fromfile_prefix_chars
        kwargs['conflict_handler'] = conflict_handler
        self._arg_parser = argparse.ArgumentParser(description=description, **kwargs)
        self._subparsers = None
        self.add_argument = self._arg_parser.add_argument
        self.set_defaults = self._arg_parser.set_defaults
        self.print_usage = self._arg_parser.print_usage
        self.print_help = self._arg_parser.print_help
        self.subcommands = {}

        # Setup logging
        self.log_level = logging.INFO
        self.log = logging.getLogger(self.__class__.__name__)
        self.add_argument('-v', '--verbose', action='store_true', help='Make the logging more verbose.')
        self.add_argument('--datetime-fmt', default='%Y-%m-%d %H:%M:%S', help='Format string for datetimes')
        self.add_argument('--log-fmt', default='[%(levelname)s] [%(asctime)s] [file:%(pathname)s] [line:%(lineno)d] %(message)s', help='Format string for log output.')

    def add_subparsers(self, title='Sub-commands', **kwargs):
        if self._inside_context_manager:
            raise RuntimeError('You must run this before the with statement!')

        self._subparsers = self._arg_parser.add_subparsers(title=title, dest='subcommand', **kwargs)

    def argument(self, *args, **kwargs):
        """Decorator to call self.add_argument or self.<subcommand>.add_argument.
        """
        if self._inside_context_manager:
            raise RuntimeError('You must run this before the with statement!')

        def argument_function(handler):
            if handler is self._entrypoint:
                self.add_argument(*args, **kwargs)

            elif handler.__name__ in self.subcommands:
                self.subcommands[handler.__name__].add_argument(*args, **kwargs)

            else:
                raise RuntimeError('Decorated function is not entrypoint or subcommand!')

            return handler

        return argument_function

    def run(self):
        """Execute the entrypoint function.
        """
        if not self._inside_context_manager:
            raise RuntimeError('You must run this inside of a with statement!')

        if not self._entrypoint:
            raise RuntimeError('No entrypoint provided!')

        return self._entrypoint(self)

    def entrypoint(self, handler):
        """Set the entrypoint for when no subcommand is provided.
        """
        if self._inside_context_manager:
            raise RuntimeError('You must run this before the with statement!')

        self._entrypoint = handler

        return handler

    def subcommand(self, handler, name=None, **kwargs):
        """Register a subcommand.

        If name is not provided we use `handler.__name__`.
        """
        if self._inside_context_manager:
            raise RuntimeError('You must run this before the with statement!')

        if self._subparsers is None:
            self.add_subparsers()

        if not name:
            name = handler.__name__

        kwargs['help'] = handler.__doc__.split('\n')[0] if handler.__doc__ else None
        self.subcommands[name] = self._subparsers.add_parser(name, **kwargs)
        self.subcommands[name].set_defaults(func=handler)

        if name not in self.__dict__:
            self.__dict__[name] = self.subcommands[name]
        else:
            self.log.debug("Could not add subcommand '%s' to attributes, key already exists!", name)

        return handler

    def __enter__(self):
        self._inside_context_manager = True
        self.args = self._arg_parser.parse_args()

        if 'func' in self.args:
            self._entrypoint = self.args.func

        if self.args.verbose:
            self.log_level = logging.DEBUG

        logging.basicConfig(level=self.log_level, format=self.args.log_fmt, datefmt=self.args.datetime_fmt)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._inside_context_manager = False
        if exc_type is not None:
            logging.exception(exc_val)
            exit(255)


if __name__ == '__main__':
        cli = CLIM('My useful CLI tool with subcommands.')

        @cli.argument('-c', '--comma', help='Include the comma in output', action='store_true')
        @cli.entrypoint
        def main(cli):
            cli.log.info('Hello%s World!', cli.args.comma)

        @cli.argument('-n', '--name', help='Name to greet', default='World')
        @cli.subcommand
        def hello(cli):
            '''Description of hello subcommand here.'''
            cli.log.info('Hello%s %s!', cli.args.comma, cli.args.name)

        def goodbye(cli):
            '''This will show up in --help output.'''
            cli.log.info('Goodbye%s %s!', cli.args.comma, cli.args.name)

        if __name__ == '__main__':
            # You can register subcommands using decorators as seen above,
            # or using functions like like this:
            cli.subcommand(goodbye)
            cli.goodbye.add_argument('-n', '--name', help='Name to bid farewell to', default='World')

            with cli:
                cli.args.comma = ',' if cli.args.comma else ''
                cli.run()  # Automatically picks between main(), hello() and goodbye()
