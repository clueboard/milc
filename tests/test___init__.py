"""Test the few things inside the `milc/__init__.py` file.
"""
import semver

import milc

EMOJI_LEVELS = ('CRITICAL', 'ERROR', 'FATAL', 'WARN', 'WARNING', 'INFO', 'DEBUG', 'NOTSET')


def test_version():
    """Make sure that version matches semver.
    """
    assert semver.VersionInfo.isvalid(milc.__VERSION__)


def test_emojis():
    """Make sure the emoji list is populated.
    """
    for emoji in milc.EMOJI_LOGLEVELS:
        if emoji not in EMOJI_LEVELS:
            raise KeyError(emoji)


def test_cli():
    """Make sure the cli is available.
    """
    assert milc.cli
