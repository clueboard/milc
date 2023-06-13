#!/usr/bin/env python3
# coding=utf-8
"""MILC - A CLI Framework

PYTHON_ARGCOMPLETE_OK

MILC is an opinionated framework for writing CLI apps. It optimizes for the
most common unix tool pattern- small tools that are run from the command
line and generally do not feature any user interaction while they run.

For more details see the MILC documentation:

    <https://github.com/clueboard/milc/tree/master/docs>
"""
__VERSION__ = '1.6.8'

import logging
import os
import sys
import warnings

from .emoji import EMOJI_LOGLEVELS
from .milc import MILC


def argv_name():
    """Returns the name of our program by examining argv.
    """
    app_name = sys.argv[0][:-3] if sys.argv[0].endswith('.py') else sys.argv[0]
    return os.path.split(app_name)[-1]


APP_NAME = os.environ.get('MILC_APP_NAME') or argv_name()
APP_VERSION = os.environ.get('MILC_APP_VERSION', 'unknown')
APP_AUTHOR = os.environ.get('MILC_APP_AUTHOR', APP_NAME.upper())

if 'MILC_IGNORE_DEPRECATED' not in os.environ:
    for name in ('MILC_APP_NAME', 'MILC_APP_VERSION', 'MILC_APP_AUTHOR'):
        if name in os.environ:
            warnings.warn(f'Using {name} is deprecated and will not be supported in the future, please use set_metadata() instead.', stacklevel=2)

logging.basicConfig(filename=os.devnull)  # Disable logging until we can configure it how the user wants

cli = MILC(APP_NAME, APP_VERSION, APP_AUTHOR)


def set_metadata(*, name=APP_NAME, author=APP_AUTHOR, version=APP_VERSION):
    """Set metadata about your program.

    This allows you to set the application's name, version, and/or author
    before executing your entrypoint. It's best to run this only once, and
    it must be run before you call `cli()`.
    """
    global APP_NAME, APP_VERSION, APP_AUTHOR, cli

    if cli._inside_context_manager:
        raise RuntimeError('You must run set_metadata() before cli()!')

    APP_NAME = name
    APP_VERSION = version
    APP_AUTHOR = author
    cli = MILC(name, version, author)


# Extra stuff people can import
from ._sparkline import sparkline  # noqa
