# coding=utf-8
import argparse
import logging
import os
import shlex
import subprocess
import sys
from configparser import RawConfigParser
from decimal import Decimal
from pathlib import Path
from platform import platform
from tempfile import NamedTemporaryFile
from types import TracebackType
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Sequence, Tuple, Type, TypeVar, Union

if TYPE_CHECKING:
    from argparse import _SubParsersAction

import threading

import argcomplete
import colorama
from halo import Halo
from platformdirs import user_config_dir
from spinners.spinners import Spinners
from typing_extensions import ParamSpec

from ._in_argv import _in_argv, _index_argv
from .ansi import MILCFormatter, ansi_colors, ansi_config, ansi_escape, format_ansi
from .attrdict import AttrDict
from .configuration import Configuration, SubparserWrapper, _collect_config_sections, _config_navigate, get_argument_name, get_argument_strings, handle_store_boolean

P = ParamSpec("P")
R = TypeVar("R")


class MILC(object):
    """MILC - An Opinionated Batteries Included Framework
    """
    def __init__(self, name: Optional[str] = None, author: Optional[str] = None, version: Optional[str] = None, logger: Optional[logging.Logger] = None, env_prefix: Optional[str] = None) -> None:
        """Initialize the MILC object.
        """
        # Set some defaults
        if not name:
            name = os.environ.get('MILC_APP_NAME') or self.argv_name()

        if not version:
            version = os.environ.get('MILC_APP_VERSION', 'unknown')

        if not author:
            author = os.environ.get('MILC_APP_AUTHOR', name.upper())

        # Setup a lock for thread safety
        self._lock = threading.RLock()

        # Define some basic info
        self.acquire_lock()
        self.prog_name = name
        self.version = version
        self.author = author
        self._config_store_true: List[str] = []
        self._config_store_false: List[str] = []
        self._entrypoint: Callable[..., Any] = lambda _: None
        self._spinners: Dict[str, Dict[str, Union[int, Sequence[str]]]] = {}
        self._subcommand = None
        self._inside_context_manager = False
        self.ansi = ansi_colors
        self.arg_only: Dict[str, List[str]] = {}
        self.config_file = self.find_config_file()
        self.default_arguments: Dict[str, Dict[str, Optional[str]]] = {}
        self.env_prefix = env_prefix
        self.env_vars_used: Dict[str, Dict[str, str]] = {}
        self._env_var_defaults: Dict[str, Dict[str, Any]] = {}
        self._env_var_errors: List[str] = []
        self.platform = platform()
        self.interactive = sys.stdin.isatty()
        self.release_lock()
        self._deprecated_arguments: Dict[str, str] = {}
        self._deprecated_commands: Dict[str, str] = {}

        # Initialize all the things
        self.initialize_config()
        self.initialize_argparse()
        self.initialize_logging(logger)
        self.initialize_arguments()

    @property
    def config_dir(self) -> Path:
        return self.config_file.parent

    @property
    def description(self) -> Optional[str]:
        return self._arg_parser.description

    @description.setter
    def description(self, value: str) -> None:
        self._arg_parser.description = value

    @property
    def subcommand_name(self) -> Optional[str]:
        """Returns the leaf CLI name of the active subcommand, e.g. 'add' for 'remote add'."""
        if self._subcommand is None:
            return None
        key = self._subcommand_keys.get(id(self._subcommand))
        return key.split('.')[-1] if key else self._subcommand.__name__

    @property
    def subcommand_path(self) -> Optional[List[str]]:
        """Returns the full subcommand path as a list, e.g. ['remote', 'add']."""
        if self._subcommand is None:
            return None
        key = self._subcommand_keys.get(id(self._subcommand))
        return key.split('.') if key else [self._subcommand.__name__]

    def argv_name(self) -> str:
        """Returns the name of our program by examining argv.
        """
        app_name = sys.argv[0][:-3] if sys.argv[0].endswith('.py') else sys.argv[0]

        return os.path.split(app_name)[-1]

    def echo(self, text: str, *args: Any, **kwargs: Any) -> None:
        """Print colorized text to stdout.

        ANSI color strings (such as {fg_blue}) will be converted into ANSI
        escape sequences, and the ANSI reset sequence will be added to all
        strings.

        If *args or **kwargs are passed they will be used to %-format the strings.
        """
        if args and kwargs:
            raise ValueError('You can only specify *args or **kwargs, not both!')

        # FIXME: For V2, when we can break backwards compatibility, format_ansi first and then do the %-formatting
        if args:
            text = format_ansi(text % args)
        elif kwargs:
            text = format_ansi(text % kwargs)
        else:
            text = format_ansi(text)

        if not self.config.general.color:
            text = ansi_escape.sub('', text)

        print(text)

    def run(
        self,
        command: Sequence[str],
        capture_output: bool = True,
        combined_output: bool = False,
        text: bool = True,
        **kwargs: Any,
    ) -> Any:  # FIXME: In python 3.10 we can use subprocess.CompletedProcess[bytes | str] instead
        """Run a command using `subprocess.run`, but using some different defaults.

        Unlike subprocess.run you must supply a sequence of arguments. You can use `shlex.split()` to build this from a string.

        The **kwargs arguments get passed directly to `subprocess.run`.

        Args:
            command
                A sequence where the first item is the command to run, and any remaining items are arguments to pass.

            capture_output
                Set to False to have output written to the terminal instead of being available in the returned `subprocess.CompletedProcess` instance.

            combined_output
                When true STDERR will be written to STDOUT. Equivalent to the shell construct `2>&1`.

            text
                Set to False to disable encoding and get `bytes()` from `.stdout` and `.stderr`.

        Note:
            On msys2/cygwin (Windows with an `MSYSTEM` environment variable set), the command is
            automatically wrapped in a subshell. stdin is also defaulted to `subprocess.DEVNULL`
            because subprocess calls in that environment leave stdin in a broken state, which
            causes interactive features like `cli.questions` to stop working. Pass `stdin=` explicitly
            to override this default.
        """
        # Sanity Checking
        if isinstance(command, str):
            raise TypeError('`command` must be a non-text sequence such as list or tuple.')

        if not capture_output and combined_output:
            raise ValueError("Can't use capture_output=False and combined_output=True at the same time.")

        # On msys2/cygwin windows platforms you have to execute the command
        # through a subshell. As well, after execution stdin is broken so
        # things like milc.questions no longer work. We pass
        # `stdin=subprocess.DEVNULL` by default to prevent that.
        # On native Windows (no MSYSTEM env var), subprocess.run works directly.
        if 'windows' in self.platform.lower() and os.environ.get('MSYSTEM'):
            safecmd = ' '.join(map(shlex.quote, command))
            shell = os.environ.get('SHELL', 'bash')
            command = [shell, '-c', safecmd]

            if 'stdin' not in kwargs:
                kwargs['stdin'] = subprocess.DEVNULL

        # Argument Processing
        if capture_output:
            kwargs['stdout'] = subprocess.PIPE
            kwargs['stderr'] = subprocess.PIPE

        if combined_output:
            kwargs['stderr'] = subprocess.STDOUT

        if text:
            kwargs['universal_newlines'] = True

        # Run the command
        self.log.debug('Running command: %s', command)

        return subprocess.run(command, **kwargs)

    def initialize_argparse(self) -> None:
        """Prepare to process arguments from sys.argv.
        """
        kwargs = {
            'fromfile_prefix_chars': '@',
            'conflict_handler': 'resolve',
        }

        self.acquire_lock()

        self.subcommands: Dict[str, Any] = {}
        self._subcommand_keys: Dict[int, str] = {}
        self._subparsers: Optional['_SubParsersAction[Any]'] = None
        self.argwarn = argcomplete.warn  # type: ignore[attr-defined]
        self.args = AttrDict()
        self.args_passed = AttrDict()
        self._arg_parser = argparse.ArgumentParser(**kwargs)  # type: ignore
        self.set_defaults = self._arg_parser.set_defaults

        self.release_lock()

    def print_help(self, *args: Any, **kwargs: Any) -> None:
        """Print a help message for the main program or subcommand, depending on context.
        """
        if self._subcommand:
            key = self._subcommand_keys.get(id(self._subcommand))
            if key and key in self.subcommands:
                self.subcommands[key].print_help(*args, **kwargs)
                return
        self._arg_parser.print_help(*args, **kwargs)

    def print_usage(self, *args: Any, **kwargs: Any) -> None:
        """Print brief description of how the main program or subcommand is invoked, depending on context.
        """
        if self._subcommand:
            key = self._subcommand_keys.get(id(self._subcommand))
            if key and key in self.subcommands:
                self.subcommands[key].print_usage(*args, **kwargs)
                return
        self._arg_parser.print_usage(*args, **kwargs)

    def log_deprecated_warning(self, item_type: str, name: str, reason: str) -> None:
        """Logs a warning with a custom message if an argument or command is deprecated.
        """
        self.log.warning("Warning: %s '%s' is deprecated:\n\t%s", item_type, name, reason)

    def add_argument(self, *args: Any, **kwargs: Any) -> None:
        """Wrapper to add arguments and track whether they were passed on the command line.
        """
        if 'action' in kwargs and kwargs['action'] == 'store_boolean':
            handle_store_boolean(self, *args, **kwargs)
            return

        arg_name = get_argument_name(self._arg_parser, *args, **kwargs)
        arg_strings = get_argument_strings(self._arg_parser, *args, **kwargs)

        # Handle tab completion
        completer = kwargs.get('completer')

        if 'completer' in kwargs:
            del kwargs['completer']

        self.acquire_lock()

        if completer:
            self._arg_parser.add_argument(*args, **kwargs).completer = completer  # type: ignore
        else:
            self._arg_parser.add_argument(*args, **kwargs)

        # Record the default for this argument
        if 'general' not in self.default_arguments:
            self.default_arguments['general'] = {}

        self.default_arguments['general'][arg_name] = kwargs.get('default')

        # Determine if it was passed on the command line
        if 'general' not in self.args_passed:
            self.args_passed['general'] = {}

        self.args_passed['general'][arg_name] = False

        for arg in arg_strings:
            if _in_argv(arg):
                self.args_passed['general'][arg_name] = True

        self.release_lock()

    def initialize_logging(self, logger: Optional[logging.Logger]) -> None:
        """Prepare the defaults for the logging infrastructure.
        """
        self.acquire_lock()

        if logger:
            self.milc_logger = False
            self.log = logger
        else:
            self.milc_logger = True
            self.log = logging.getLogger(self.__class__.__name__)
            self.log_file = None
            self.log_file_mode = 'a'
            self.log_file_handler: Optional[logging.FileHandler] = None
            self.log_print = True
            self.log_print_to = sys.stderr
            self.log_print_level = logging.INFO
            self.log_file_level = logging.INFO
            self.log_level = logging.INFO

            self.log.setLevel(logging.DEBUG)
            logging.root.setLevel(logging.DEBUG)

        self.release_lock()

        if self.milc_logger:
            self.add_argument('-v', '--verbose', action='store_true', help='Make the logging more verbose')
            self.add_argument('--datetime-fmt', default='%Y-%m-%d %H:%M:%S', help='Format string for datetimes')
            self.add_argument('--log-fmt', default='%(levelname)s %(message)s', help='Format string for printed log output')
            self.add_argument('--log-file-fmt', default='[%(levelname)s] [%(asctime)s] [file:%(pathname)s] [line:%(lineno)d] %(message)s', help='Format string for log file.')
            self.add_argument('--log-file-level', default='info', choices=['debug', 'info', 'warning', 'error', 'critical'], help='Logging level for log file.')
            self.add_argument('--log-file', help='File to write log messages to')
            self.add_argument('--color', action='store_boolean', default=ansi_config['color'], help='color in output')
            self.add_argument('--unicode', action='store_boolean', default=ansi_config['unicode'], help='unicode loglevels')

    def initialize_arguments(self) -> None:
        """Setup and add default arguments.
        """
        self.add_argument('-V', '--version', version=self.version, action='version', help='Display the version and exit')
        self.add_argument('--interactive', action='store_true', help='Force interactive mode even when stdout is not a tty.')
        self.add_argument('--config-file', help='The location for the configuration file')

        self.arg_only['config_file'] = ['general']

    def add_subparsers(self, title: str = 'Sub-commands', **kwargs: Any) -> None:
        if self._inside_context_manager:
            raise RuntimeError('You must run this before the with statement!')

        self.acquire_lock()
        self._subparsers = self._arg_parser.add_subparsers(title=title, dest='subparsers', **kwargs)
        self.release_lock()

    def acquire_lock(self, blocking: bool = True) -> bool:
        """Acquire the MILC lock for exclusive access to properties.
        """
        if self._lock:
            return self._lock.acquire(blocking)

        return True

    def release_lock(self) -> None:
        """Release the MILC lock.
        """
        if self._lock:
            self._lock.release()

    def find_config_file(self) -> Path:
        """Locate the config file.
        """
        config_file_index = _index_argv('--config-file')

        if config_file_index is not None:
            config_file_param = sys.argv[config_file_index]

            if '=' in config_file_param:
                # get the file name from the '=' assignment
                opt, config_file = config_file_param.split('=')

            else:
                # assume the file name is next space-sep arg
                if config_file_index + 1 >= len(sys.argv):
                    print('ERROR: --config-file requires a value.', file=sys.stderr)
                    sys.exit(1)
                config_file = sys.argv[config_file_index + 1]

            return Path(config_file).expanduser().resolve()

        filedir = user_config_dir(appname=self.prog_name, appauthor=self.author)
        filename = '%s.ini' % self.prog_name

        return Path(filedir, filename).resolve()

    def _handle_deprecated(self, arg_name: str, kwargs: Dict[str, Any]) -> None:
        """Called by self.argument: Mark an argument as deprecated, if necessary.
        """
        if 'deprecated' in kwargs:
            self._deprecated_arguments[arg_name] = kwargs['deprecated']
            if kwargs.get('help'):
                kwargs['help'] += f" [Deprecated]: {kwargs['deprecated']}"
            else:
                kwargs['help'] = f"[Deprecated]: {kwargs['deprecated']}"
            del kwargs['deprecated']

    def _apply_env_var_default(self, config_name: str, arg_name: str, args: Sequence[Any], kwargs: Dict[str, Any]) -> None:
        """Apply env var as default when env_prefix is set and a matching env var exists.
        """
        if self.env_prefix is None or not any(a.startswith('--') for a in args):
            return
        prefix = self.env_prefix + '_' if self.env_prefix != '' else ''
        if config_name == 'general':
            env_key = prefix + arg_name.replace('-', '_').upper()
        else:
            env_key = prefix + config_name.replace('-', '_').upper() + '_' + arg_name.replace('-', '_').upper()
        env_value = os.environ.get(env_key)
        if env_value is None:
            return
        action = kwargs.get('action')
        # store_false args are the --no-X half of store_boolean pairs; the store_boolean arg itself is already handled, so skip these entirely.
        if action == 'store_false':
            self.log.debug('Ignoring %s for --%s: store_false arguments do not support env var defaults', env_key, arg_name)
            return
        # List-producing and ambiguous-arity arguments are not supported — skip these.
        # Covers: nargs='+'/'*'/REMAINDER, nargs=N (integer), and action='append'.
        # nargs='?' is also excluded: passing the flag with no value should use const, not the env var, and that interaction is too subtle to handle reliably.
        nargs = kwargs.get('nargs')
        if nargs in ('+', '*', '?', argparse.REMAINDER) or isinstance(nargs, int) or action == 'append':
            self.log.debug('Ignoring %s for --%s: nargs=%r / action=%r arguments do not support env var defaults', env_key, arg_name, nargs, action)
            return
        type_fn = kwargs.get('type')
        if action in ('store_true', 'store_boolean'):
            resolved = env_value.lower() not in ('-1', '0', 'false', 'no', 'off', '')
        elif type_fn:
            try:
                resolved = type_fn(env_value)
            except (ValueError, TypeError) as e:
                self._env_var_errors.append(f"environment variable {env_key}={env_value!r} is not the correct type: {e}")
                return
        else:
            resolved = env_value
        # For boolean flags, argparse ignores default when another action already claimed the same dest, so we bypass it and apply the value in merge_args_into_config.
        # For other args we still need to set the default so argparse accepts required=False.
        if action not in ('store_true', 'store_boolean'):
            kwargs['default'] = resolved
        kwargs['required'] = False
        if config_name not in self.env_vars_used:
            self.env_vars_used[config_name] = {}
        self.env_vars_used[config_name][arg_name] = env_key
        if config_name not in self._env_var_defaults:
            self._env_var_defaults[config_name] = {}
        self._env_var_defaults[config_name][arg_name] = resolved

    def _handle_arg_parsing(self, config_name: str, arg_name: str, args: Sequence[Any], kwargs: Dict[str, Any]) -> None:
        """Called by self.argument: Parse this argument into the right datastructures.
        """
        arg_strings = get_argument_strings(self._arg_parser, *args, **kwargs)
        self._apply_env_var_default(config_name, arg_name, args, kwargs)

        if kwargs.get('arg_only'):
            if arg_name not in self.arg_only:
                self.arg_only[arg_name] = []

            self.arg_only[arg_name].append(config_name)
            del kwargs['arg_only']
        else:
            if config_name not in self.default_arguments:
                self.default_arguments[config_name] = {}

            self.default_arguments[config_name][arg_name] = kwargs.get('default')

            config_section = _config_navigate(self.config, config_name)
            if config_section[arg_name] is None:
                config_section[arg_name] = kwargs.get('default')

            if config_name not in self.args_passed:
                self.args_passed[config_name] = {}

            self.args_passed[config_name][arg_name] = False

            for arg in arg_strings:
                if _in_argv(arg):
                    self.args_passed[config_name][arg_name] = True

    def argument(self, *args: Any, **kwargs: Any) -> Callable[[Callable[P, R]], Callable[P, R]]:
        """Decorator to call self.add_argument or self.<subcommand>.add_argument.
        """
        if self._inside_context_manager:
            raise RuntimeError('You must run this before the with statement!')

        def argument_function(handler: Callable[P, R]) -> Callable[P, R]:
            dotted_key = self._subcommand_keys.get(id(handler))
            arg_name = get_argument_name(self._arg_parser, *args, **kwargs)

            self._handle_deprecated(arg_name, kwargs)

            if handler is self._entrypoint:
                self._handle_arg_parsing('general', arg_name, args, kwargs)
                self.add_argument(*args, **kwargs)

            elif dotted_key is not None and dotted_key in self.subcommands:
                self._handle_arg_parsing(dotted_key.replace('-', '_'), arg_name, args, kwargs)
                self.subcommands[dotted_key].add_argument(*args, **kwargs)

            else:
                raise RuntimeError('Decorated function is not entrypoint or subcommand!')

            return handler

        return argument_function

    def parse_args(self) -> None:
        """Parse the CLI args.
        """
        if self.args:
            self.log.debug('Warning: Arguments have already been parsed, ignoring duplicate attempt!')
            return

        argcomplete.autocomplete(self._arg_parser)

        self.acquire_lock()

        for key, value in vars(self._arg_parser.parse_args()).items():
            self.args[key] = value

        for error in self._env_var_errors:
            self._arg_parser.error(error)

        if 'entrypoint' in self.args:
            self._subcommand = self.args.entrypoint

        self.release_lock()

    def read_config_file(self) -> Tuple[Configuration, Configuration]:
        """Read in the configuration file and return Configuration objects for it and the config_source.
        """
        config = Configuration()
        config_source = Configuration()

        if self.config_file.exists():
            raw_config = RawConfigParser()
            raw_config.read(str(self.config_file))

            # Iterate over the config file options and write them into config.
            # Section names may be dotted (e.g. [remote.add]) for nested subcommands.
            for section in raw_config.sections():
                config_section = _config_navigate(config, section)
                config_source_section = _config_navigate(config_source, section)

                for option in raw_config.options(section):
                    value = raw_config.get(section, option)

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

                    config_section[option] = value
                    config_source_section[option] = 'config_file'

        return config, config_source

    def initialize_config(self) -> None:
        """Read in the configuration file and store it in self.config.
        """
        self.acquire_lock()
        self.config, self.config_source = self.read_config_file()
        self.release_lock()

    def merge_args_into_config(self) -> None:
        """Merge CLI arguments into self.config to create the runtime configuration.
        """
        self.acquire_lock()
        subcommand_name = None
        if self._subcommand is not None:
            dotted_key = self._subcommand_keys.get(
                id(self._subcommand),
                self._subcommand.__name__.replace('_', '-'),
            )
            subcommand_name = dotted_key.replace('-', '_')

        for argument in self.args:
            if argument in ('subparsers', 'entrypoint'):
                continue

            # Find the argument's section.
            # Prefer the active subcommand section when the argument was registered there,
            # since a subcommand arg with the same dest as a general arg should win.
            if subcommand_name and argument in self.default_arguments.get(subcommand_name, {}):
                section = subcommand_name
            elif argument in self.default_arguments.get('general', {}):
                section = 'general'
            else:
                section = subcommand_name

            if section is None:
                continue

            if argument not in self.arg_only or section not in self.arg_only[argument]:
                # Determine the arg value and source
                arg_value = getattr(self.args, argument)
                config_section = _config_navigate(self.config, section)
                config_source_section = _config_navigate(self.config_source, section)

                # Merge this argument into self.config
                if self.args_passed[section][argument] or (argument in self._config_store_true and arg_value) or (argument in self._config_store_false and not arg_value):
                    config_section[argument] = arg_value
                    config_source_section[argument] = 'argument'
                elif section in self.env_vars_used and argument in self.env_vars_used[section]:
                    # Env var overrides config file and default; use stored resolved value (not arg_value, since argparse may not have used our default for boolean flags)
                    if config_source_section[argument] == 'config_file':
                        self.log.debug('Environment variable %s overrides config file value for %s.%s', self.env_vars_used[section][argument], section, argument)
                    config_section[argument] = self._env_var_defaults[section][argument]
                    config_source_section[argument] = 'env_var'
                elif config_section[argument] is None:
                    # Capture the default value
                    config_section[argument] = arg_value

        self.release_lock()

    def _save_config_file(self, config: Configuration) -> None:
        """Write config to disk.
        """
        # Generate a sanitized version of our running configuration.
        # _collect_config_sections recurses into nested ConfigurationSection objects,
        # emitting (dotted_section_name, option_name, value) for every leaf.
        sane_config = RawConfigParser()
        for section_name, option_name, value in _collect_config_sections(config):
            if not sane_config.has_section(section_name):
                sane_config.add_section(section_name)
            config_source_section = _config_navigate(self.config_source, section_name)
            if config_source_section[option_name] == 'config_file' and value is not None:
                sane_config.set(section_name, option_name, str(value))

        if not self.config_dir.exists():
            self.config_dir.mkdir(parents=True, exist_ok=True)

        # Write the config file atomically.
        self.acquire_lock()
        tmpfile_name = None
        try:
            with NamedTemporaryFile(mode='w', dir=str(self.config_dir), delete=False) as tmpfile:
                tmpfile_name = tmpfile.name
                sane_config.write(tmpfile)

            if os.path.getsize(tmpfile_name) > 0:
                os.replace(tmpfile_name, str(self.config_file))
            else:
                self.log.warning('Config file saving failed, not replacing %s with %s.', str(self.config_file), tmpfile_name)
        finally:
            try:
                if tmpfile_name and os.path.exists(tmpfile_name):
                    os.unlink(tmpfile_name)
            finally:
                self.release_lock()

    def write_config_option(self, section: str, option: Any) -> None:
        """Save a single config option to the config file.
        """
        if not self.config_file:
            self.log.warning('%s.config_file not set, not saving config!', self.__class__.__name__)
            return

        config, config_source = self.read_config_file()

        if section in config and option in config[section] and config[section][option] is None:
            del config[section][option]
        else:
            config[section][option] = str(self.config[section][option])

        self._save_config_file(config)

        # Housekeeping
        self.log.info('Wrote configuration to %s', shlex.quote(str(self.config_file)))

    def save_config(self) -> None:
        """Save the current configuration to the config file.
        """
        self.log.debug("Saving config file to '%s'", str(self.config_file))

        if not self.config_file:
            self.log.warning('%s.config_file file not set, not saving config!', self.__class__.__name__)
            return

        # Write config to disk
        self._save_config_file(self.config)
        self.log.info('Wrote configuration to %s', shlex.quote(str(self.config_file)))

    def check_deprecated(self) -> None:
        entry_name = getattr(self._entrypoint, '__name__')

        if entry_name in self._deprecated_commands:
            msg = self._deprecated_commands[entry_name]
            self.log_deprecated_warning('Entrypoint', entry_name, msg)

        if self._subcommand:
            name = self._subcommand_keys.get(
                id(self._subcommand),
                self._subcommand.__name__.replace('_', '-'),
            )
            if name in self._deprecated_commands:
                msg = self._deprecated_commands[name]
                self.log_deprecated_warning('Subcommand', name, msg)

        deprecated_args_passed = [arg.split('=')[0].lstrip('-').replace('-', '_') for arg in sys.argv if arg.split('=')[0].lstrip('-').replace('-', '_') in self._deprecated_arguments]

        for arg in deprecated_args_passed:
            msg = self._deprecated_arguments[arg]
            self.log_deprecated_warning('Argument', arg, msg)

    def __call__(self) -> Any:
        """Execute the entrypoint function.
        """
        if not self._inside_context_manager:
            # If they didn't use the context manager use it ourselves
            with self:
                return self.__call__()

        self.check_deprecated()

        if self._subcommand:
            return self._subcommand(self)

        elif self._entrypoint is not None:
            return self._entrypoint(self)

        raise RuntimeError('No entrypoint provided!')

    def entrypoint(self, description: str, deprecated: Optional[str] = None) -> Callable[[Callable[P, R]], Callable[P, R]]:
        """Decorator that marks the entrypoint used when a subcommand is not supplied.
        Args:
            description
                A one-line description to display in --help

            deprecated
                Deprecation message. When set the subcommand will marked as deprecated and this message will be displayed in the help output.
        """
        if self._inside_context_manager:
            raise RuntimeError('You must run this before cli()!')

        self.acquire_lock()
        self.description = description
        self.release_lock()

        def entrypoint_func(handler: Callable[P, R]) -> Callable[P, R]:
            self.acquire_lock()

            if deprecated:
                self._deprecated_commands[getattr(handler, '__name__')] = deprecated
                self.description = f'{self.description} [Deprecated]: {deprecated}'

            self._entrypoint = handler
            self.release_lock()

            return handler

        return entrypoint_func

    def add_subcommand(
        self,
        handler: Callable[P, R],
        description: str,
        hidden: bool = False,
        deprecated: Optional[str] = None,
        parent: Optional[Callable[..., Any]] = None,
        name: Optional[str] = None,
        **kwargs: Any,
    ) -> Callable[P, R]:
        """Register a subcommand.

        Args:

            handler
                The function to execute for this subcommand.

            description
                A one-line description to display in --help

            hidden
                When True don't display this command in --help

            deprecated
                Deprecation message. When set the subcommand will be marked as deprecated
                and this message will be displayed in help output.

            parent
                The parent subcommand function. When provided, this subcommand is registered
                as a child of that subcommand (enabling nested commands like 'prog remote add').
                Must be a function object previously registered as a subcommand.

            name
                Override the CLI token for this subcommand. Defaults to the handler's
                function name in kebab-case.
        """
        if self._inside_context_manager:
            raise RuntimeError('You must run this before the with statement!')

        if parent is not None:
            if not callable(parent):
                raise TypeError("'parent' must be a function object, not a string.")
            parent_key = self._subcommand_keys.get(id(parent))
            if parent_key is None:
                raise ValueError(f"Parent function '{getattr(parent, '__name__', repr(parent))}' is not a registered subcommand.")
            parent_wrapper = self.subcommands[parent_key]
            target_subparsers = parent_wrapper.get_child_subparsers()
            cli_name = name or getattr(handler, '__name__').replace('_', '-')
            dotted_key = f"{parent_key}.{cli_name}"
        else:
            if self._subparsers is None:
                self.add_subparsers(metavar="")
            assert self._subparsers is not None
            target_subparsers = self._subparsers
            cli_name = name or getattr(handler, '__name__').replace('_', '-')
            dotted_key = cli_name

        # Pre-register config sections so hierarchical access never returns None.
        # Use underscore form for config paths (hyphens can't be Python identifiers).
        config_path = dotted_key.replace('-', '_')
        _config_navigate(self.config, config_path)
        _config_navigate(self.config_source, config_path)

        if deprecated:
            self._deprecated_commands[dotted_key] = deprecated
            description += f' [Deprecated]: {deprecated}'

        self.acquire_lock()

        if parent is None and not hidden and self._subparsers is not None:
            if self._subparsers.metavar:
                self._subparsers.metavar = "{%s,%s}" % (self._subparsers.metavar[1:-1], cli_name)
            else:
                self._subparsers.metavar = "{%s}" % cli_name

        kwargs['help'] = description

        self.subcommands[dotted_key] = SubparserWrapper(self, config_path, target_subparsers.add_parser(cli_name, **kwargs))
        self.subcommands[dotted_key].set_defaults(entrypoint=handler)
        self._subcommand_keys[id(handler)] = dotted_key

        self.release_lock()

        return handler

    def subcommand(self, description: str, hidden: bool = False, parent: Optional[Callable[..., Any]] = None, name: Optional[str] = None, **kwargs: Any) -> Callable[[Callable[P, R]], Callable[P, R]]:
        """Decorator to register a subcommand.

        Args:

            description
                A one-line description to display in --help

            hidden
                When True don't display this command in --help

            parent
                The parent subcommand function. When provided, this subcommand is registered
                as a child of that subcommand.

            name
                Override the CLI token for this subcommand.
        """
        def subcommand_function(handler: Callable[P, R]) -> Callable[P, R]:
            return self.add_subcommand(handler, description, hidden=hidden, parent=parent, name=name, **kwargs)

        return subcommand_function

    def setup_logging(self) -> None:
        """Called by __enter__() to setup the logging configuration.
        """
        if self.milc_logger:
            if len(logging.root.handlers) != 0:
                # MILC is the only thing that should have root log handlers
                logging.root.handlers = []

            self.acquire_lock()

            if self.config.general.verbose:
                self.log_print_level = logging.DEBUG

            ansi_config['color'] = self.config.general.color
            ansi_config['unicode'] = self.config.general.unicode

            self.log_file = self.config.general.log_file or self.log_file
            self.log_file_format = MILCFormatter(self.config.general.log_file_fmt, self.config.general.datetime_fmt)
            self.log_file_level = getattr(logging, self.config.general.log_file_level.upper())
            self.log_format = MILCFormatter(self.config.general.log_fmt, self.config.general.datetime_fmt)

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

    def __enter__(self) -> Any:
        if self._inside_context_manager:
            self.log.debug('Warning: context manager was entered again. This usually means that self.__call__() was called before the with statement. You probably do not want to do that.')
            return

        self.acquire_lock()
        self._inside_context_manager = True
        self.release_lock()

        colorama.init()
        self.parse_args()
        self.merge_args_into_config()

        if self.config.general.interactive:
            self.interactive = True

        self.setup_logging()

        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.acquire_lock()
        self._inside_context_manager = False
        self.release_lock()

        if exc_type is not None and not issubclass(exc_type, (SystemExit, KeyboardInterrupt)):
            self.log.error('%s: %s', exc_type.__name__, exc_val)
            sys.exit(255)

    def is_spinner(self, name: str) -> bool:
        """Returns true if name is a valid spinner.
        """
        return name in Spinners.__members__ or name in self._spinners

    def add_spinner(self, name: str, spinner: Dict[str, Union[int, Sequence[str]]]) -> None:
        """Adds a new spinner to the list of spinners.

        A spinner is a dictionary with two keys:

            interval
                An integer that sets how long (in ms) to wait between frames.

            frames
                A list of frames for this spinner
        """
        if self.is_spinner(name):
            raise ValueError(f'Spinner "{name}" already exists!')

        if not isinstance(spinner, dict):
            raise ValueError('The spinner must be a dictionary!')

        if 'interval' not in spinner or 'frames' not in spinner:
            raise ValueError('The spinner must have `interval` and `frames` keys!')

        self._spinners[name] = spinner

    def spinner(
        self,
        text: str,
        *args: Any,
        spinner: Optional[Union[str, Dict[str, Union[int, Sequence[str]]]]] = None,
        animation: str = 'ellipsed',
        placement: str = 'left',
        color: str = 'blue',
        interval: int = -1,
        stream: Any = sys.stdout,
        enabled: bool = sys.stdout.isatty(),
        **kwargs: Any,
    ) -> Halo:
        """Create a spinner object for showing activity to the user.

        This uses halo <https://github.com/ManrajGrover/halo> behind the scenes, most of the arguments map to Halo objects 1:1.

        There are 3 basic ways to use this:

        * Instantiating a spinner and then using `.start()` and `.stop()` on your object.
        * Using a context manager (`with cli.spinner(...):`)
        * Decorate a function (`@cli.spinner(...)`)

        #### Instantiating a spinner

        ```python
        spinner = cli.spinner(text='Loading', spinner='dots')
        spinner.start()

        # Do something here

        spinner.stop()
        ```

        #### Using a context manager

        ```python
        with cli.spinner(text='Loading', spinner='dots'):
            # Do something here
        ```

        #### Decorate a function

        ```python
        @cli.spinner(text='Loading', spinner='dots')
        def long_running_function():
            # Do something here
        ```

        ### Arguments

            text
                The text to display next to the spinner. ANSI color strings
                (such as {fg_blue}) will be converted into ANSI escape
                sequences, and the ANSI reset sequence will be added to the
                end of the string.

                If *args or **kwargs are passed they will be used to
                %-format the text.

            spinner
                The name of the spinner to use, or a dict with `interval`
                (int, ms) and `frames` (list of str) keys to use directly
                as the spinner definition. Available names are here:
                <https://raw.githubusercontent.com/sindresorhus/cli-spinners/dac4fc6571059bb9e9bc204711e9dfe8f72e5c6f/spinners.json>

            animation
                The animation to apply to the text if it doesn't fit the
                terminal. One of `ellipsed`, `bounce`, `marquee`.

            placement
                Which side of the text to display the spinner on. One of
                `left`, `right`.

            color
                Color of the spinner. One of `blue`, `grey`, `red`, `green`,
                `yellow`, `magenta`, `cyan`, `white`

            interval
                How long in ms to wait between frames. Defaults to the spinner interval (recommended.)

            stream
                Stream to write the output. Defaults to sys.stdout.

            enabled
                Enable or disable the spinner. Defaults to `sys.stdout.isatty()`.
        """
        spinner_obj: Any = None

        if isinstance(spinner, dict):
            spinner_name = ''
            spinner_obj = spinner
        elif spinner in self._spinners:
            spinner_name = ''
            spinner_obj = self._spinners[spinner]
        else:
            spinner_name = spinner or 'line'  # FIXME: Grab one of the ascii spinners at random instead of line

        if args:
            text = format_ansi(text % args)
        elif kwargs:
            text = format_ansi(text % kwargs)
        else:
            text = format_ansi(text)

        return Halo(
            text=text,
            spinner=spinner_name or spinner_obj,
            animation=None if animation == 'ellipsed' else animation,
            placement=placement,
            color=color,
            interval=interval,
            stream=stream,
            enabled=enabled,
        )
