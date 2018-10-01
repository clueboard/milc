"""PyCLIm - The CLI Context Manager
"""
from __future__ import division, print_function, unicode_literals
import argparse
import logging

class CLIM(object):
    """CLI Context Manager

    This class wraps some standard python modules in nice ways for CLI tools.

    Simple Example:

        cli = CLIM('My useful CLI tool.')

        @cli.entrypoint
        def main(cli):
            cli.log.info('Hello, World!')

        if __name__ == '__main__':
            with cli:
                cli.run()

    Subcommand Example:

        cli = CLIM('My useful CLI tool.')

        @cli.entrypoint
        def main(cli):
            cli.log.info('Hello, World!')

        @cli.subcommand
        def cmd1(cli):
            '''Description of cmd1 here.'''
            cli.log.info('Hello, Sub-Command 1!')

        def cmd2(cli):
            '''This will show up in --help output.'''
            cli.log.info('Hello, Sub-Command 2!')

        if __name__ == '__main__':
            # You can register subcommands using a decorator as seen above,
            # or using a function like like this:
            cli.subcommand(cmd2)

            with cli:
                # The run function will automatically pick between main(), cmd1() and cmd2()
                cli.run()  
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
        self.subcommands = None

        # Setup logging
        self.log_level = logging.INFO
        self.log = logging.getLogger(self.__class__.__name__)
        self.add_argument('-v', '--verbose', action='store_true', help='Make the logging more verbose.')
        self.add_argument('--datetime-fmt', default='%Y-%m-%d %H:%M:%S', help='Format string for datetimes')
        self.add_argument('--log-fmt', default='[%(levelname)s] [%(asctime)s] [file:%(pathname)s] [line:%(lineno)d] %(message)s', help='Format string for log output.')

    def __get__(self, obj, type=None):
        """Override to allow us to support accessing subcommands as attributes.
        """
        if hasattr(self, obj):
            return getattr(self, obj)

        if obj in self.subcommands:
            return self.subcommands[obj]

        raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, obj))

    def add_subparsers(self, title='Sub-commands', **kwargs):
        if self._inside_context_manager:
            raise RuntimeError('You must run this before the with statement!')

        self._subparsers = self._arg_parser.add_subparsers(title=title, dest='subcommand', **kwargs)
        self.subcommands = {}

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
    def main(cli):
        cli.log.info('Hello, World!')

    def cmd1(cli):
        """Command 1
        """
        cli.log.info('Hello, Sub-Command 1!')

    def cmd2(cli):
        """Command 2
        """
        cli.log.info('Hello, Sub-Command 2!')

    if __name__ == '__main__':
        cli = CLIM('My useful CLI tool.', main)

        cli.subcommand('cmd1', cmd1)
        cli.subcommand('cmd2', cmd2)

        with cli:
            # The run function will automatically pick between main(), cmd1(), and cmd2() based on the CLI arguments
            cli.run()
