#!/usr/bin/env python3
# coding=utf-8
"""MILC - A CLI Framework

PYTHON_ARGCOMPLETE_OK

MILC is an opinionated framework for writing CLI apps. It optimizes for the
most common unix tool pattern- small tools that are run from the command
line but generally do not feature any user interaction while they run.

For more details see the MILC documentation:

    <https://github.com/clueboard/milc/tree/master/docs>
"""
__VERSION__ = '1.0.4'

import logging
import os

from .emoji import EMOJI_LOGLEVELS
from .milc import MILC

# Disable logging until we can configure it how the user wants
logging.basicConfig(stream=os.devnull)

cli = MILC()
