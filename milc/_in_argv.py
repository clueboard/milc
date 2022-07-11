import sys


def _in_argv(argument):
    """Returns true if the argument is found is sys.argv.

    Since long options can be passed as either '--option value' or '--option=value' we need to check for both forms.
    """
    return _index_argv(argument) is not None

    return False


def _index_argv(argument):
    """Returns the location of the argument in sys.argv, or None.

    Since long options can be passed as either '--option value' or '--option=value' we need to check for both forms.
    """
    if argument.startswith('--'):
        for i, arg in enumerate(sys.argv):
            if arg.split('=')[0] == argument:
                return i
    else:
        for i, arg in enumerate(sys.argv):
            if arg.startswith(argument):
                return i

    return None
