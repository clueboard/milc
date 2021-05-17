import os
import re
from tempfile import mkstemp

from .common import check_command, check_returncode


def test_example():
    result = check_command('./example', '-h')
    check_returncode(result)
    assert '{config,dashed-hello,hello,goodbye}' in result.stdout


def test_example_version():
    result = check_command('./example', '--version')
    check_returncode(result)
    assert re.match(r'[0-9]*\.[0-9]*\.[0-9]*', result.stdout)


def test_example_config():
    fd, tempfile = mkstemp()

    try:
        os.close(fd)

        # Check initial state
        result = check_command('./example', '--no-color', '--config-file', tempfile, 'config')
        check_returncode(result)
        assert result.stdout == ''

        # Set some values in the configuration
        result = check_command('./example', '--no-color', '--config-file', tempfile, 'config', 'general.name=Test', 'user.comma=true')
        check_returncode(result)
        assert 'general.name: World -> Test' in result.stdout
        assert 'user.comma: None -> true' in result.stdout

        # Make sure we get them back
        result = check_command('./example', '--no-color', '--config-file', tempfile, 'config')
        check_returncode(result)
        assert result.stdout == 'user.comma=True\nhello.comma=True\ngeneral.name=Test\n'

    finally:
        os.remove(tempfile)


def test_example_hello():
    result = check_command('./example', 'hello')
    check_returncode(result)
    assert result.stdout == 'Hello, World!\n'


def test_example_hello_help():
    result = check_command('./example', 'hello', '--help')
    check_returncode(result)
    assert '[--no-comma]' in result.stdout
    assert '[--print-help]' in result.stdout
    assert '[--print-usage]' in result.stdout


def test_example_hello_no_color():
    result = check_command('./example', '--no-color', 'hello')
    check_returncode(result)
    assert result.stdout == 'Hello, World!\n'


def test_example_hello_no_color_no_unicode():
    result = check_command('./example', '--no-color', '--no-unicode', 'hello')
    check_returncode(result)
    assert result.stdout == 'Hello, World!\n'


def test_example_hello_no_color_no_comma():
    result = check_command('./example', '--no-color', 'hello', '--no-comma')
    check_returncode(result)
    assert result.stdout == 'Hello World!\n'


def test_example_hello_no_color_no_unicode_no_comma():
    result = check_command('./example', '--no-color', '--no-unicode', 'hello', '--no-comma')
    check_returncode(result)
    assert result.stdout == 'Hello World!\n'


def test_example_dashed_hello():
    result = check_command('./example', 'dashed-hello')
    check_returncode(result)
    print(repr(result.stdout))
    assert result.stdout == 'Hello, dashed-subcommand World!\n'


def test_example_dashed_hello_dashed_name():
    result = check_command('./example', 'dashed-hello', '--dashed-name', 'Tester')
    check_returncode(result)
    print(repr(result.stdout))
    assert result.stdout == 'Hello, dashed-subcommand Tester!\n'
