import os
import sys

from .common import check_assert, check_command, check_returncode


def test_prerun_entrypoint_order_and_parameters():
    result = check_command(sys.executable, 'prerun_example', '--no-color', '--config-file', os.devnull)
    check_returncode(result)
    check_assert(result, result.stdout == 'plain:None\nconfigured:token:kwargs:None\nentrypoint\n')


def test_prerun_subcommand_order_and_parameters():
    result = check_command(sys.executable, 'prerun_example', '--no-color', '--config-file', os.devnull, 'hello')
    check_returncode(result)
    check_assert(result, result.stdout == 'plain:hello\nconfigured:token:kwargs:hello\nsubcommand\n')
