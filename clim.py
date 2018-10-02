"""py-clim - The CLI Context Manager

CLIM is an opinionated framework for writing CLI apps. It optimizes for the
most common unix tool pattern- small tools that are run from the command
line but generally do not feature any user interaction while they run.

Using CLIM will give your script all of these features with no work for you:

* CLI Argument Parsing, with or without subcommands
* Performance improvement from putting your code inside a function
  <https://stackoverflow.com/questions/11241523/why-does-python-code-run-faster-in-a-function>
* Config file support, with config options overridden by command line flags
* Logging to stderr and/or a file
* Thread safe! (Note: This needs more eyes looking at it to ensure thread safety.)
"""
from __future__ import division, print_function, unicode_literals
import argparse
import logging
import sys

try:
    import thread
    import therading
except ImportError:
    thread = None

class CLIM(object):
    """# CLI Context Manager

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
        self.version = 'unknown'

        # Setup a lock for thread safety and hold it until initialization is complete
        self._lock = threading.RLock() if thread else None
        self.acquire_lock()

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
        self.log_file = None
        self.log_file_mode = 'a'
        self.log_file_handler = None
        self.log_print = True
        self.log_print_to = sys.stderr
        self.log_print_level = logging.INFO
        self.log_file_level = logging.DEBUG
        self.log_level = logging.INFO
        self.log = logging.getLogger(self.__class__.__name__)
        self.add_argument('-V', '--version', action='store_true', help="Display the program's version and exit")
        self.add_argument('-v', '--verbose', action='store_true', help='Make the logging more verbose')
        self.add_argument('--datetime-fmt', default='%Y-%m-%d %H:%M:%S', help='Format string for datetimes')
        self.add_argument('--log-fmt', default='[%(levelname)s] %(message)s', help='Format string for printed log output')
        self.add_argument('--log-file-fmt', default='[%(levelname)s] [%(asctime)s] [file:%(pathname)s] [line:%(lineno)d] %(message)s', help='Format string for log file.')
        self.add_argument('--log-file', help='File to write log messages to')

        # Release the lock
        self.release_lock()

    def add_subparsers(self, title='Sub-commands', **kwargs):
        if self._inside_context_manager:
            raise RuntimeError('You must run this before the with statement!')

        self.acquire_lock()
        self._subparsers = self._arg_parser.add_subparsers(title=title, dest='subcommand', **kwargs)
        self.release_lock()

    def acquire_lock(self):
        """Acquire the CLIM lock for exclusive access to properties.
        """
        if self._lock:
            self._lock.acquire()

    def release_lock(self):
        """Release the CLIM lock.
        """
        if self._lock:
            self._lock.release()

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

        self.acquire_lock()
        self._entrypoint = handler
        self.release_lock()

        return handler

    def subcommand(self, handler, name=None, **kwargs):
        """Register a subcommand.

        If name is not provided we use `handler.__name__`.
        """
        if self._inside_context_manager:
            raise RuntimeError('You must run this before the with statement!')

        if self._subparsers is None:
            self.add_subparsers()

        self.acquire_lock()

        if not name:
            name = handler.__name__

        kwargs['help'] = handler.__doc__.split('\n')[0] if handler.__doc__ else None
        self.subcommands[name] = self._subparsers.add_parser(name, **kwargs)
        self.subcommands[name].set_defaults(func=handler)

        if name not in self.__dict__:
            self.__dict__[name] = self.subcommands[name]
        else:
            self.log.debug("Could not add subcommand '%s' to attributes, key already exists!", name)

        self.release_lock()

        return handler

    def setup_logging(self):
        """Called by __enter__() to setup the logging configuration.
        """
        if len(logging.root.handlers) != 0:
            # This is not a design decision. This is what I'm doing for now until I can examine and think about this situation in more detail.
            raise RuntimeError('CLIM should be the only system installing root log handlers!')

        self.acquire_lock()

        self.log_format = logging.Formatter(self.args.log_fmt, self.args.datetime_fmt)
        self.log_file_format = logging.Formatter(self.args.log_file_fmt, self.args.datetime_fmt)

        if self.log_file:
            self.log_file_handler = logging.FileHandler(self.log_file, self.log_file_mode)
            self.log_file_handler.setFormatter(self.log_file_format)
            self.log_file_handler.setLevel(self.log_file_level)
            logging.root.addHandler(self.log_file_handler)

        if self.log_print:
            self.log_print_handler = logging.StreamHandler(self.log_print_to)
            self.log_print_handler.setFormatter(self.log_format)
            self.log_print_handler.setLevel(self.log_print_level)
            logging.root.addHandler(self.log_print_handler)

        logging.root.setLevel(self.log_level)

        self.release_lock()

    def __enter__(self):
        self.acquire_lock()
        self._inside_context_manager = True
        self.args = self._arg_parser.parse_args()

        if self.args.version:
            print('%s version %s' % (sys.argv[0], self.version))
            exit(0)

        if 'func' in self.args:
            self._entrypoint = self.args.func

        if self.args.verbose:
            self.log_print_level = logging.DEBUG

        self.log_file = self.args.log_file or self.log_file
        self.log_file_format = self.args.log_file_fmt
        self.log_format = self.args.log_fmt

        self.release_lock()
        self.setup_logging()

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
