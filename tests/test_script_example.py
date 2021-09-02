import os
import re
from tempfile import mkstemp

from .common import check_assert, check_command, check_returncode


def test_example():
    result = check_command('./example', '-h')
    check_returncode(result)
    check_assert(result, '{config,dashed-hello,hello,goodbye,config-file}' in result.stdout)


def test_example_version():
    result = check_command('./example', '--version')
    check_returncode(result)
    check_assert(result, re.match(r'[0-9]*\.[0-9]*\.[0-9]*', result.stdout))


def test_example_config():
    fd, tempfile = mkstemp()

    try:
        os.close(fd)

        # Check initial state
        result = check_command('./example', '--no-color', '--config-file', tempfile, 'config')
        check_returncode(result)
        check_assert(result, result.stdout == '')

        # Set some values in the configuration
        result = check_command('./example', '--no-color', '--config-file', tempfile, 'config', 'general.name=Test', 'user.comma=true')
        check_returncode(result)
        check_assert(result, 'general.name: World -> Test' in result.stdout)
        check_assert(result, 'user.comma: None -> true' in result.stdout)

        # Make sure we get them back
        result = check_command('./example', '--no-color', '--config-file', tempfile, 'config')
        check_returncode(result)
        check_assert(result, result.stdout == 'general.name=Test\nhello.comma=True\nuser.comma=True\n')

    finally:
        os.remove(tempfile)


def test_numeric_arguments():
    fd, tempfile = mkstemp()

    try:
        os.close(fd)

        # Set the count
        result = check_command('./example', '--no-color', '--config-file', tempfile, 'config', 'hello.count=2')
        check_returncode(result)
        check_assert(result, 'hello.count: 1 -> 2' in result.stdout)

        # Make sure we get 2 prints
        result = check_command('./example', '--no-color', '--config-file', tempfile, 'hello')
        check_returncode(result)
        print(repr(result.stdout))
        check_assert(result, result.stdout == 'Hello, World!\nHello, World!\n')

        # Make sure we get 1 prints
        result = check_command('./example', '--no-color', '--config-file', tempfile, 'hello', '--count', '1')
        check_returncode(result)
        print(repr(result.stdout))
        check_assert(result, result.stdout == 'Hello, World!\n')

    finally:
        os.remove(tempfile)


def test_example_hello():
    result = check_command('./example', '--config-file', '/dev/null', 'hello')
    check_returncode(result)
    check_assert(result, result.stdout == 'Hello, World!\n')


def test_example_hello_help():
    result = check_command('./example', '--config-file', '/dev/null', 'hello', '--help')
    check_returncode(result)
    check_assert(result, '[--no-comma]' in result.stdout)
    check_assert(result, '[--print-help]' in result.stdout)
    check_assert(result, '[--print-usage]' in result.stdout)


def test_example_hello_no_color():
    result = check_command('./example', '--no-color', '--config-file', '/dev/null', 'hello')
    check_returncode(result)
    check_assert(result, result.stdout == 'Hello, World!\n')


def test_example_hello_no_color_no_unicode():
    result = check_command('./example', '--no-color', '--no-unicode', '--config-file', '/dev/null', 'hello')
    check_returncode(result)
    check_assert(result, result.stdout == 'Hello, World!\n')


def test_example_hello_no_color_no_comma():
    result = check_command('./example', '--no-color', '--config-file', '/dev/null', 'hello', '--no-comma')
    check_returncode(result)
    check_assert(result, result.stdout == 'Hello World!\n')


def test_example_hello_no_color_no_unicode_no_comma():
    result = check_command('./example', '--no-color', '--no-unicode', '--config-file', '/dev/null', 'hello', '--no-comma')
    check_returncode(result)
    check_assert(result, result.stdout == 'Hello World!\n')


def test_example_dashed_hello():
    result = check_command('./example', '--config-file', '/dev/null', 'dashed-hello')
    check_returncode(result)
    check_assert(result, result.stdout == 'Hello, dashed-subcommand World!\n')


def test_example_dashed_hello_dashed_name():
    result = check_command('./example', '--config-file', '/dev/null', 'dashed-hello', '--dashed-name', 'Tester')
    check_returncode(result)
    check_assert(result, result.stdout == 'Hello, dashed-subcommand Tester!\n')


def test_example_config_file():
    result = check_command('./example', 'config-file')
    check_returncode(result)
    lines = result.stdout.split('\n')
    filename = lines[0].split('=', 1)[1]
    filedir = lines[1].split('=', 1)[1]
    check_assert(result, len(lines) == 3)
    check_assert(result, filename.endswith('example.ini'))
    check_assert(result, filename.startswith(filedir))
