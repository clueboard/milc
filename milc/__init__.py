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
__VERSION__ = '1.8.0'

import logging
import os
import sys
import warnings
from typing import Optional

from .emoji import EMOJI_LOGLEVELS
from .milc import MILC

if 'MILC_IGNORE_DEPRECATED' not in os.environ:
    for name in ('MILC_APP_NAME', 'MILC_APP_VERSION', 'MILC_APP_AUTHOR'):
        if name in os.environ:
            warnings.warn(f'Using environment variable {name} is deprecated and will not be supported in the future, please use set_metadata() instead.', stacklevel=2)

cli = MILC()


def set_metadata(
    *,
    name: Optional[str] = None,
    author: Optional[str] = None,
    version: Optional[str] = None,
    logger: Optional[logging.Logger] = None,
) -> MILC:
    """Set metadata about your program.

    This allows you to set the application's name, version, and/or author
    before executing your entrypoint. You can also pass your own logger here
    if you like.

    It's best to run this only once, and it must be run before you call `cli()`.
    """
    global cli

    if cli._inside_context_manager:
        raise RuntimeError('You must run set_metadata() before cli()!')

    cli = MILC(name, version, author, logger)

    return cli


# Extra stuff people can import
from ._sparkline import sparkline  # noqa
