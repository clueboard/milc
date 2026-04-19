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
__VERSION__ = '1.11.0'

import logging
import os
import sys
import warnings
from typing import Any, Optional

from .emoji import EMOJI_LOGLEVELS
from .milc import MILC
from .milc_interface import MILCInterface

cli = MILCInterface()

# Extra stuff people can import
from ._sparkline import sparkline  # noqa
