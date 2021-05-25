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
    check_assert(result, result.stdout == 'ℹ Hello, World, from cli.log.info!\nHello, World, from cli.echo!\n')


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
    result = check_command('./hello', '--no-color', '--log-file', '/dev/stdout')
    check_returncode(result)
    check_assert(result, result.stdout.startswith('[ℹ] '))
    check_assert(result, result.stdout.endswith('Hello, World, from cli.log.info!\nℹ Hello, World, from cli.log.info!\nHello, World, from cli.echo!\n'))


def test_hello_no_color_no_unicoe_log_file():
    result = check_command('./hello', '--no-color', '--no-unicode', '--log-file', '/dev/stdout')
    check_returncode(result)
    check_assert(result, result.stdout.startswith('[INFO] '))
    check_assert(result, result.stdout.endswith('Hello, World, from cli.log.info!\nINFO Hello, World, from cli.log.info!\nHello, World, from cli.echo!\n'))


def test_hello_no_color_verbose():
    result = check_command('./hello', '--no-color', '-v')
    check_returncode(result)
    check_assert(result, result.stdout == '☐ You used -v you lucky person!\nℹ Hello, World, from cli.log.info!\nHello, World, from cli.echo!\n')


def test_hello_no_color_no_unicode_verbose():
    result = check_command('./hello', '--no-color', '--no-unicode', '-v')
    check_returncode(result)
    check_assert(result, result.stdout == 'DEBUG You used -v you lucky person!\nINFO Hello, World, from cli.log.info!\nHello, World, from cli.echo!\n')
