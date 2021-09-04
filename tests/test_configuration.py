"""Unit tests for milc.configuration.
"""
import argparse

import milc.configuration

arg_parser = argparse.ArgumentParser(description='Minimal argparser.')


def test_get_argument_names_optional():
    """Make sure we can get optional names from get_argument_strings.
    """
    assert milc.configuration.get_argument_name(arg_parser, '-v', '--verbose') == 'verbose'


def test_get_argument_names_positional():
    """Make sure we can get positional names from get_argument_strings.
    """
    assert milc.configuration.get_argument_name(arg_parser, 'files') == 'files'


def test_get_argument_strings_optional():
    """Make sure we can get optional names from get_argument_strings.
    """
    assert milc.configuration.get_argument_strings(arg_parser, '-v', '--verbose') == ['-v', '--verbose']


def test_get_argument_strings_positional():
    """Make sure we can get positional names from get_argument_strings.
    """
    assert milc.configuration.get_argument_strings(arg_parser, 'files') == ['files']
