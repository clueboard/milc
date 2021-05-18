from .common import check_command, check_returncode


def test_hello():
    result = check_command('./hello')
    check_returncode(result)
    assert 'Hello, World, from cli.log.info!' in result.stdout
    assert 'Hello, World, from cli.echo!' in result.stdout


def test_hello_help():
    result = check_command('./hello', '--help')
    check_returncode(result)
    assert '[-n NAME]' in result.stdout
    assert '[--no-comma]' in result.stdout


def test_hello_no_color():
    result = check_command('./hello', '--no-color')
    check_returncode(result)
    assert result.stdout == 'ℹ Hello, World, from cli.log.info!\nHello, World, from cli.echo!\n'


def test_hello_no_color_no_unicode():
    result = check_command('./hello', '--no-color', '--no-unicode')
    check_returncode(result)
    assert result.stdout == 'INFO Hello, World, from cli.log.info!\nHello, World, from cli.echo!\n'


def test_hello_no_color_no_comma():
    result = check_command('./hello', '--no-color', '--no-comma')
    check_returncode(result)
    assert result.stdout == 'ℹ Hello World, from cli.log.info!\nHello World, from cli.echo!\n'


def test_hello_no_color_no_unicode_no_comma():
    result = check_command('./hello', '--no-color', '--no-unicode', '--no-comma')
    check_returncode(result)
    assert result.stdout == 'INFO Hello World, from cli.log.info!\nHello World, from cli.echo!\n'


def test_hello_no_color_log_file():
    result = check_command('./hello', '--no-color', '--log-file', '/dev/stdout')
    check_returncode(result)
    assert result.stdout.startswith('[ℹ] ')
    assert result.stdout.endswith('Hello, World, from cli.log.info!\nℹ Hello, World, from cli.log.info!\nHello, World, from cli.echo!\n')


def test_hello_no_color_no_unicoe_log_file():
    result = check_command('./hello', '--no-color', '--no-unicode', '--log-file', '/dev/stdout')
    check_returncode(result)
    assert result.stdout.startswith('[INFO] ')
    assert result.stdout.endswith('Hello, World, from cli.log.info!\nINFO Hello, World, from cli.log.info!\nHello, World, from cli.echo!\n')


def test_hello_no_color_verbose():
    result = check_command('./hello', '--no-color', '-v')
    check_returncode(result)
    assert result.stdout == '☐ You used -v you lucky person!\nℹ Hello, World, from cli.log.info!\nHello, World, from cli.echo!\n'


def test_hello_no_color_no_unicode_verbose():
    result = check_command('./hello', '--no-color', '--no-unicode', '-v')
    check_returncode(result)
    assert result.stdout == 'DEBUG You used -v you lucky person!\nINFO Hello, World, from cli.log.info!\nHello, World, from cli.echo!\n'
