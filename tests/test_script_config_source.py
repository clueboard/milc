import os
from .common import check_assert, check_command, check_returncode

WITH_CONFIG_FILE = ('--config-file', 'config_source.config')
NO_CONFIG_FILE = ('--config-file',  os.path.devnull)

def test_config_source_config():
    result = check_command('./config_source', *WITH_CONFIG_FILE)
    check_returncode(result)
    check_assert(result, result.stdout == 'Hello, Config, from config_file!\n')


def test_config_source_no_config():
    result = check_command('./config_source', *NO_CONFIG_FILE)
    check_returncode(result)
    check_assert(result, result.stdout == 'Hello, World, from None!\n')


def test_config_source_name_no_config():
    result = check_command('./config_source', '--name', 'Test', *NO_CONFIG_FILE)
    check_returncode(result)
    check_assert(result, result.stdout == 'Hello, Test, from argument!\n')

def test_config_source_name_long_1arg_no_config():
    result = check_command('./config_source', '--name=Test', *NO_CONFIG_FILE)
    check_returncode(result)
    check_assert(result, result.stdout == 'Hello, Test, from argument!\n')

def test_config_source_name_short_1arg_no_config():
    result = check_command('./config_source', '-nTest', *NO_CONFIG_FILE)
    check_returncode(result)
    check_assert(result, result.stdout == 'Hello, Test, from argument!\n')

def test_config_source_name_short_2arg_no_config():
    result = check_command('./config_source', '-n', 'Test', *NO_CONFIG_FILE)
    check_returncode(result)
    check_assert(result, result.stdout == 'Hello, Test, from argument!\n')

def test_config_source_name():
    result = check_command('./config_source', '--name', 'Test', *WITH_CONFIG_FILE)
    check_returncode(result)
    check_assert(result, result.stdout == 'Hello, Test, from argument!\n')

def test_config_source_name_long_1arg():
    result = check_command('./config_source', '--name=Test', *WITH_CONFIG_FILE)
    check_returncode(result)
    check_assert(result, result.stdout == 'Hello, Test, from argument!\n')

def test_config_source_name_short_1arg():
    result = check_command('./config_source', '-nTest', *WITH_CONFIG_FILE)
    check_returncode(result)
    check_assert(result, result.stdout == 'Hello, Test, from argument!\n')

def test_config_source_name_short_2arg():
    result = check_command('./config_source', '-n', 'Test', *WITH_CONFIG_FILE)
    check_returncode(result)
    check_assert(result, result.stdout == 'Hello, Test, from argument!\n')
