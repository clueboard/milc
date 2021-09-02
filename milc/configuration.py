from .attrdict import AttrDict


class Configuration(AttrDict):
    """Represents the running configuration.

    This class never raises IndexError, instead it will return None if a
    section or option does not yet exist.
    """
    def __getitem__(self, key):
        """Returns a config section, creating it if it doesn't exist yet.
        """
        if key not in self._data:
            self._data[key] = ConfigurationSection(self)

        return self._data[key]


class ConfigurationSection(Configuration):
    def __init__(self, parent, *args, **kwargs):
        super(ConfigurationSection, self).__init__(*args, **kwargs)
        self._parent = parent

    def __getitem__(self, key):
        """Returns a config value, pulling from the `user` section as a fallback.
        This is called when the attribute is accessed either via the get method or through [ ] index.
        """
        if key in self._data and self._data.get(key) is not None:
            return self._data[key]

        elif key in self._parent.user:
            return self._parent.user[key]

        return None

    def __getattr__(self, key):
        """Returns the config value from the `user` section.
        This is called when the attribute is accessed via dot notation but does not exist.
        """
        if key[0] != '_' and key in self._parent['user']:
            return self._parent['user'][key]

        return None

    def __setattr__(self, key, value):
        """Sets dictionary value when an attribute is set.
        """
        super().__setattr__(key, value)

        if key[0] != '_':
            self._data[key] = value


class SubparserWrapper(object):
    """Wrap subparsers so we can track what options the user passed.
    """
    def __init__(self, cli, submodule, subparser):
        self.cli = cli
        self.submodule = submodule
        self.subparser = subparser

        for attr in dir(subparser):
            if not hasattr(self, attr):
                setattr(self, attr, getattr(subparser, attr))

    def completer(self, completer):
        """Add an arpcomplete completer to this subcommand.
        """
        self.subparser.completer = completer

    def add_argument(self, *args, **kwargs):
        """Add an argument for this subcommand.

        This also stores the default for the argument in `self.cli.default_arguments`.
        """
        if kwargs.get('action') == 'store_boolean':
            # Store boolean will call us again with the enable/disable flag arguments
            return handle_store_boolean(self, *args, **kwargs)

        completer = None

        if kwargs.get('completer'):
            completer = kwargs['completer']
            del kwargs['completer']

        self.cli.acquire_lock()
        argument_name = get_argument_name(self.cli._arg_parser, *args, **kwargs)

        if completer:
            self.subparser.add_argument(*args, **kwargs).completer = completer
        else:
            self.subparser.add_argument(*args, **kwargs)

        if kwargs.get('action') == 'store_false':
            self.cli._config_store_false.append(argument_name)

        if kwargs.get('action') == 'store_true':
            self.cli._config_store_true.append(argument_name)

        if self.submodule not in self.cli.default_arguments:
            self.cli.default_arguments[self.submodule] = {}

        self.cli.default_arguments[self.submodule][argument_name] = kwargs.get('default')
        self.cli.release_lock()


def get_argument_strings(arg_parser, *args, **kwargs):
    """Takes argparse arguments and returns a list of argument strings or positional names.
    """
    try:
        return arg_parser._get_optional_kwargs(*args, **kwargs)['option_strings']
    except ValueError:
        return [arg_parser._get_positional_kwargs(*args, **kwargs)['dest']]


def get_argument_name(arg_parser, *args, **kwargs):
    """Takes argparse arguments and returns the dest name.
    """
    try:
        return arg_parser._get_optional_kwargs(*args, **kwargs)['dest']
    except ValueError:
        return arg_parser._get_positional_kwargs(*args, **kwargs)['dest']


def handle_store_boolean(self, *args, **kwargs):
    """Does the add_argument for action='store_boolean'.
    """
    disabled_args = None
    disabled_kwargs = kwargs.copy()
    disabled_kwargs['action'] = 'store_false'
    disabled_kwargs['dest'] = get_argument_name(getattr(self, 'cli', self)._arg_parser, *args, **kwargs)
    disabled_kwargs['help'] = 'Disable ' + kwargs['help']
    kwargs['action'] = 'store_true'
    kwargs['help'] = 'Enable ' + kwargs['help']

    for flag in args:
        if flag[:2] == '--':
            disabled_args = ('--no-' + flag[2:],)
            break

    self.add_argument(*args, **kwargs)
    self.add_argument(*disabled_args, **disabled_kwargs)

    return (args, kwargs, disabled_args, disabled_kwargs)
