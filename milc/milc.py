#!/usr/bin/env python3
# coding=utf-8
import argparse
import logging
import os
import shlex
import sys
from decimal import Decimal
from pathlib import Path
from tempfile import NamedTemporaryFile

try:
    from ConfigParser import RawConfigParser
except ImportError:
    from configparser import RawConfigParser

try:
    import thread
    import threading
except ImportError:
    thread = None

import argcomplete
import colorama
from appdirs import user_config_dir

from .ansi import ANSIEmojiLoglevelFormatter, ANSIStrippingFormatter, ansi_colors, format_ansi
from .configuration import Configuration, SubparserWrapper, get_argument_name, handle_store_boolean
from .attrdict import AttrDict


class MILC(object):
    """MILC - An Opinionated Batteries Included Framework
    """
    def __init__(self):
        """Initialize the MILC object.

            version
                The version string to associate with your CLI program
        """
        # Setup a lock for thread safety
        self._lock = threading.RLock() if thread else None

        # Define some basic info
        self.acquire_lock()
        self._config_store_true = []
        self._config_store_false = []
        self._description = None
        self._entrypoint = None
        self._inside_context_manager = False
        self.ansi = ansi_colors
        self.arg_only = {}
        self.config = self.config_source = None
        self.config_file = None
        self.default_arguments = {}
        self.version = 'unknown'
        self.release_lock()

        # Figure out our program name
        self.prog_name = sys.argv[0][:-3] if sys.argv[0].endswith('.py') else sys.argv[0]
        self.prog_name = os.environ.get('MILC_APP_NAME', os.path.basename(self.prog_name))

        # Initialize all the things
        self.read_config_file()
        self.initialize_argparse()
        self.initialize_logging()

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = self._arg_parser.description = value

    def echo(self, text, *args, **kwargs):
        """Print colorized text to stdout.

        ANSI color strings (such as {fg-blue}) will be converted into ANSI
        escape sequences, and the ANSI reset sequence will be added to all
        strings.

        If *args or **kwargs are passed they will be used to %-format the strings.
        """
        if args and kwargs:
            raise RuntimeError('You can only specify *args or **kwargs, not both!')

        args = args or kwargs
        text = format_ansi(text)

        print(text % args)

    def initialize_argparse(self):
        """Prepare to process arguments from sys.argv.
        """
        kwargs = {
            'fromfile_prefix_chars': '@',
            'conflict_handler': 'resolve',
        }

        self.acquire_lock()
        self.subcommands = {}
        self._subparsers = None
        self.argwarn = argcomplete.warn
        self.args = AttrDict()
        self._arg_parser = argparse.ArgumentParser(**kwargs)
        self.set_defaults = self._arg_parser.set_defaults
        self.print_usage = self._arg_parser.print_usage
        self.print_help = self._arg_parser.print_help
        self.release_lock()

    def completer(self, completer):
        """Add an argcomplete completer to this subcommand.
        """
        self._arg_parser.completer = completer

    def add_argument(self, *args, **kwargs):
        """Wrapper to add arguments and track whether they were passed on the command line.
        """
        if 'action' in kwargs and kwargs['action'] == 'store_boolean':
            return handle_store_boolean(self, *args, **kwargs)

        self.acquire_lock()

        self._arg_parser.add_argument(*args, **kwargs)
        if 'general' not in self.default_arguments:
            self.default_arguments['general'] = {}
        self.default_arguments['general'][get_argument_name(self, *args, **kwargs)] = kwargs.get('default')

        self.release_lock()

    def initialize_logging(self):
        """Prepare the defaults for the logging infrastructure.
        """
        self.acquire_lock()
        self.log_file = None
        self.log_file_mode = 'a'
        self.log_file_handler = None
        self.log_print = True
        self.log_print_to = sys.stderr
        self.log_print_level = logging.INFO
        self.log_file_level = logging.DEBUG
        self.log_level = logging.INFO
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.DEBUG)
        logging.root.setLevel(logging.DEBUG)
        self.release_lock()

        self.add_argument('-V', '--version', version=self.version, action='version', help='Display the version and exit')
        self.add_argument('-v', '--verbose', action='store_true', help='Make the logging more verbose')
        self.add_argument('--datetime-fmt', default='%Y-%m-%d %H:%M:%S', help='Format string for datetimes')
        self.add_argument('--log-fmt', default='%(levelname)s %(message)s', help='Format string for printed log output')
        self.add_argument('--log-file-fmt', default='[%(levelname)s] [%(asctime)s] [file:%(pathname)s] [line:%(lineno)d] %(message)s', help='Format string for log file.')
        self.add_argument('--log-file', help='File to write log messages to')
        self.add_argument('--color', action='store_boolean', default=True, help='color in output')
        self.add_argument('--config-file', help='The location for the configuration file')
        self.arg_only['config_file'] = ['general']

    def add_subparsers(self, title='Sub-commands', **kwargs):
        if self._inside_context_manager:
            raise RuntimeError('You must run this before the with statement!')

        self.acquire_lock()
        self._subparsers = self._arg_parser.add_subparsers(title=title, dest='subparsers', **kwargs)
        self.release_lock()

    def acquire_lock(self, blocking=True):
        """Acquire the MILC lock for exclusive access to properties.
        """
        if self._lock:
            self._lock.acquire(blocking)

    def release_lock(self):
        """Release the MILC lock.
        """
        if self._lock:
            self._lock.release()

    def find_config_file(self):
        """Locate the config file.
        """
        if self.config_file:
            return self.config_file

        if '--config-file' in sys.argv:
            return Path(sys.argv[sys.argv.index('--config-file') + 1]).expanduser().resolve()

        filedir = user_config_dir(appname=self.prog_name, appauthor=os.environ.get('MILC_APP_AUTHOR', self.prog_name.upper()))
        filename = '%s.ini' % self.prog_name
        return Path(filedir) / filename

    def argument(self, *args, **kwargs):
        """Decorator to call self.add_argument or self.<subcommand>.add_argument.
        """
        if self._inside_context_manager:
            raise RuntimeError('You must run this before the with statement!')

        def argument_function(handler):
            subcommand_name = handler.__name__.replace("_", "-")

            if kwargs.get('arg_only'):
                arg_name = get_argument_name(self, *args, **kwargs)

                if arg_name not in self.arg_only:
                    self.arg_only[arg_name] = []

                self.arg_only[arg_name].append(handler.__name__)
                del kwargs['arg_only']

            if handler is self._entrypoint:
                self.add_argument(*args, **kwargs)

            elif subcommand_name in self.subcommands:
                self.subcommands[subcommand_name].add_argument(*args, **kwargs)

            else:
                raise RuntimeError('Decorated function is not entrypoint or subcommand!')

            return handler

        return argument_function

    def parse_args(self):
        """Parse the CLI args.
        """
        if self.args:
            self.log.debug('Warning: Arguments have already been parsed, ignoring duplicate attempt!')
            return

        argcomplete.autocomplete(self._arg_parser)

        self.acquire_lock()
        for key, value in vars(self._arg_parser.parse_args()).items():
            self.args[key] = value

        if 'entrypoint' in self.args:
            self._entrypoint = self.args.entrypoint

        self.release_lock()

    def read_config_file(self):
        """Read in the configuration file and store it in self.config.
        """
        self.acquire_lock()
        self.config = Configuration()
        self.config_source = Configuration()
        self.config_file = self.find_config_file()

        if self.config_file and self.config_file.exists():
            config = RawConfigParser(self.config)
            config.read(str(self.config_file))

            # Iterate over the config file options and write them into self.config
            for section in config.sections():
                for option in config.options(section):
                    value = config.get(section, option)

                    # Coerce values into useful datatypes
                    if value.lower() in ['yes', 'true', 'on']:
                        value = True
                    elif value.lower() in ['no', 'false', 'off']:
                        value = False
                    elif value.lower() in ['none']:
                        continue
                    elif value.replace('.', '').isdigit():
                        if '.' in value:
                            value = Decimal(value)
                        else:
                            value = int(value)

                    self.config[section][option] = value
                    self.config_source[section][option] = 'config_file'

        self.release_lock()

    def merge_args_into_config(self):
        """Merge CLI arguments into self.config to create the runtime configuration.
        """
        self.acquire_lock()
        for argument in self.args:
            if argument in ('subparsers', 'entrypoint'):
                continue

            # Find the argument's section
            # Underscores in command's names are converted to dashes during initialization.
            # TODO(Erovia) Find a better solution
            entrypoint_name = self._entrypoint.__name__.replace("_", "-")
            if entrypoint_name in self.default_arguments and argument in self.default_arguments[entrypoint_name]:
                argument_found = True
                section = self._entrypoint.__name__
            if argument in self.default_arguments['general']:
                argument_found = True
                section = 'general'

            if not argument_found:
                raise RuntimeError('Could not find argument in `self.default_arguments`. This should be impossible!')
                exit(1)

            if argument not in self.arg_only or section not in self.arg_only[argument]:
                # Determine the arg value and source
                arg_value = getattr(self.args, argument)
                if argument in self._config_store_true and arg_value:
                    passed_on_cmdline = True
                elif argument in self._config_store_false and not arg_value:
                    passed_on_cmdline = True
                elif arg_value is not None:
                    passed_on_cmdline = True
                else:
                    passed_on_cmdline = False

                # Merge this argument into self.config
                if passed_on_cmdline and (argument in self.default_arguments['general'] or argument in self.default_arguments[entrypoint_name] or argument not in self.config[entrypoint_name]):
                    self.config[section][argument] = arg_value
                    self.config_source[section][argument] = 'argument'

        self.release_lock()

    def save_config(self):
        """Save the current configuration to the config file.
        """
        self.log.debug("Saving config file to '%s'", str(self.config_file))

        if not self.config_file:
            self.log.warning('%s.config_file file not set, not saving config!', self.__class__.__name__)
            return

        self.acquire_lock()

        # Generate a sanitized version of our running configuration
        config = RawConfigParser()
        for section_name, section in self.config.items():
            config.add_section(section_name)
            for option_name, value in section.items():
                if section_name == 'general':
                    if option_name in ['config_file']:
                        continue
                if value is not None:
                    config.set(section_name, option_name, str(value))

        # Write out the config file
        config_dir = self.config_file.parent
        if not config_dir.exists():
            config_dir.mkdir(parents=True, exist_ok=True)

        with NamedTemporaryFile(mode='w', dir=str(config_dir), delete=False) as tmpfile:
            config.write(tmpfile)

        # Move the new config file into place atomically
        if os.path.getsize(tmpfile.name) > 0:
            os.replace(tmpfile.name, str(self.config_file))
        else:
            self.log.warning('Config file saving failed, not replacing %s with %s.', str(self.config_file), tmpfile.name)

        # Housekeeping
        self.release_lock()
        self.log.info('Wrote configuration to %s', shlex.quote(str(self.config_file)))

    def __call__(self):
        """Execute the entrypoint function.
        """
        if not self._inside_context_manager:
            # If they didn't use the context manager use it ourselves
            with self:
                return self.__call__()

        if not self._entrypoint:
            raise RuntimeError('No entrypoint provided!')

        return self._entrypoint(self)

    def entrypoint(self, description):
        """Set the entrypoint for when no subcommand is provided.
        """
        if self._inside_context_manager:
            raise RuntimeError('You must run this before cli()!')

        self.acquire_lock()
        self.description = description
        self.release_lock()

        def entrypoint_func(handler):
            self.acquire_lock()
            self._entrypoint = handler
            self.release_lock()

            return handler

        return entrypoint_func

    def add_subcommand(self, handler, description, hidden=False, **kwargs):
        """Register a subcommand.

        Args:

            handler
                The function to exececute for this subcommand.

            description
                A one-line description to display in --help

            hidden
                When True don't display this command in --help
        """
        if self._inside_context_manager:
            raise RuntimeError('You must run this before the with statement!')

        if self._subparsers is None:
            self.add_subparsers(metavar="")

        name = handler.__name__.replace("_", "-")

        self.acquire_lock()
        if not hidden:
            self._subparsers.metavar = "{%s,%s}" % (self._subparsers.metavar[1:-1], name) if self._subparsers.metavar else "{%s%s}" % (self._subparsers.metavar[1:-1], name)
            kwargs['help'] = description
        self.subcommands[name] = SubparserWrapper(self, name, self._subparsers.add_parser(name, **kwargs))
        self.subcommands[name].set_defaults(entrypoint=handler)

        self.release_lock()

        return handler

    def subcommand(self, description, hidden=False, **kwargs):
        """Decorator to register a subcommand.

        Args:

            description
                A one-line description to display in --help

            hidden
                When True don't display this command in --help
        """
        def subcommand_function(handler):
            return self.add_subcommand(handler, description, hidden=hidden, **kwargs)

        return subcommand_function

    def setup_logging(self):
        """Called by __enter__() to setup the logging configuration.
        """
        if len(logging.root.handlers) != 0:
            # MILC is the only thing that should have root log handlers
            logging.root.handlers = []

        self.acquire_lock()

        if self.config['general']['verbose']:
            self.log_print_level = logging.DEBUG

        self.log_file = self.config['general']['log_file'] or self.log_file
        self.log_file_format = self.config['general']['log_file_fmt']
        self.log_file_format = ANSIStrippingFormatter(self.config['general']['log_file_fmt'], self.config['general']['datetime_fmt'])
        self.log_format = self.config['general']['log_fmt']

        if self.config.general.color:
            self.log_format = ANSIEmojiLoglevelFormatter(self.args.log_fmt, self.config.general.datetime_fmt)
        else:
            self.log_format = ANSIStrippingFormatter(self.args.log_fmt, self.config.general.datetime_fmt)

        if self.log_file:
            self.log_file_handler = logging.FileHandler(self.log_file, self.log_file_mode)
            self.log_file_handler.setLevel(self.log_file_level)
            self.log_file_handler.setFormatter(self.log_file_format)
            logging.root.addHandler(self.log_file_handler)

        if self.log_print:
            self.log_print_handler = logging.StreamHandler(self.log_print_to)
            self.log_print_handler.setLevel(self.log_print_level)
            self.log_print_handler.setFormatter(self.log_format)
            logging.root.addHandler(self.log_print_handler)

        self.release_lock()

    def __enter__(self):
        if self._inside_context_manager:
            self.log.debug('Warning: context manager was entered again. This usually means that self.__call__() was called before the with statement. You probably do not want to do that.')
            return

        self.acquire_lock()
        self._inside_context_manager = True
        self.release_lock()

        colorama.init()
        self.parse_args()
        self.merge_args_into_config()
        self.setup_logging()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.acquire_lock()
        self._inside_context_manager = False
        self.release_lock()

        if exc_type is not None and not isinstance(SystemExit(), exc_type):
            print(exc_type)
            logging.exception(exc_val)
            exit(255)
