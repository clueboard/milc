from os import unlink
from tempfile import NamedTemporaryFile

from .common import check_assert, check_command, check_returncode


def test_hello():
    result = check_command('./hello')
    check_returncode(result)
    check_assert(result, 'Hello, World, from cli.log.info!' in result.stdout)
    check_assert(result, 'Hello, World, from cli.echo!' in result.stdout)


def test_hello_help():
    result = check_command('./hello', '--help')
    check_returncode(result)
    check_assert(result, '[-n NAME]' in result.stdout)
    check_assert(result, '[--no-comma]' in result.stdout)


def test_hello_no_color():
    result = check_command('./hello', '--no-color')
    check_returncode(result)
    if 'ℹ' in result.stdout:
        check_assert(result, result.stdout == 'ℹ Hello, World, from cli.log.info!\nHello, World, from cli.echo!\n')
    else:
        check_assert(result, result.stdout == 'INFO Hello, World, from cli.log.info!\nHello, World, from cli.echo!\n')


def test_hello_no_color_no_unicode():
    result = check_command('./hello', '--no-color', '--no-unicode')
    check_returncode(result)
    check_assert(result, result.stdout == 'INFO Hello, World, from cli.log.info!\nHello, World, from cli.echo!\n')


def test_hello_no_color_no_comma():
    result = check_command('./hello', '--no-color', '--no-comma')
    check_returncode(result)
    check_assert(result, result.stdout == 'ℹ Hello World, from cli.log.info!\nHello World, from cli.echo!\n')


def test_hello_no_color_no_unicode_no_comma():
    result = check_command('./hello', '--no-color', '--no-unicode', '--no-comma')
    check_returncode(result)
    check_assert(result, result.stdout == 'INFO Hello World, from cli.log.info!\nHello World, from cli.echo!\n')


def test_hello_no_color_log_file():
    log_file = NamedTemporaryFile(delete=False)
    result = check_command('./hello', '--no-color', '--log-file', log_file.name)
    check_returncode(result)
    if 'ℹ' in result.stdout:
        check_assert(result, result.stdout == 'ℹ Hello, World, from cli.log.info!\nHello, World, from cli.echo!\n')
    else:
        check_assert(result, result.stdout == 'INFO Hello, World, from cli.log.info!\nHello, World, from cli.echo!\n')
    log_file_contents = log_file.read().decode('utf-8')
    log_file.close()
    unlink(log_file.name)
    if 'Hello, World, from cli.log.info!' not in log_file_contents:
        print('Log File Contents:')
        print(log_file_contents)
        print()
        raise AssertionError


def test_hello_no_color_no_unicode_log_file():
    log_file = NamedTemporaryFile(delete=False)
    result = check_command('./hello', '--no-color', '--no-unicode', '--log-file', log_file.name)
    check_returncode(result)
    check_assert(result, result.stdout == 'INFO Hello, World, from cli.log.info!\nHello, World, from cli.echo!\n')
    log_file_contents = log_file.read().decode('utf-8')
    log_file.close()
    unlink(log_file.name)
    if 'Hello, World, from cli.log.info!' not in log_file_contents:
        print('Log File Contents:')
        print(log_file_contents)
        print()
        raise AssertionError


def test_hello_no_color_verbose():
    result = check_command('./hello', '--no-color', '-v')
    check_returncode(result)
    if '☐' in result.stdout:
        check_assert(result, result.stdout == '☐ You used -v you lucky person!\nℹ Hello, World, from cli.log.info!\nHello, World, from cli.echo!\n')
    else:
        check_assert(result, result.stdout == 'DEBUG You used -v you lucky person!\nINFO Hello, World, from cli.log.info!\nHello, World, from cli.echo!\n')


def test_hello_no_color_no_unicode_verbose():
    result = check_command('./hello', '--no-color', '--no-unicode', '-v')
    check_returncode(result)
    check_assert(result, result.stdout == 'DEBUG You used -v you lucky person!\nINFO Hello, World, from cli.log.info!\nHello, World, from cli.echo!\n')
