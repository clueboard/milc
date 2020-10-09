from milc import cli


def check_command(command, *args):
    cmd = [command] + list(args)
    return cli.run(cmd, combined_output=True)


def check_returncode(result, expected=0):
    """Print stdout if `result.returncode` does not match `expected`.
    """
    if result.returncode != expected:
        print('`%s` stdout:' % ' '.join(result.args))
        print(result.stdout)
        print('returncode:', result.returncode)
    assert result.returncode == expected


def test_hello():
    result = check_command('./hello')
    check_returncode(result)
    assert result.stdout == '\x1b[34mℹ\x1b[0m Hello, World, from cli.log.info!\x1b[0m\nHello, World, from cli.echo!\n'


def test_hello_help():
    result = check_command('./hello', '--help')
    check_returncode(result)
    assert '[-n NAME]' in result.stdout
    assert '[--no-comma]' in result.stdout


def test_hello_no_color():
    result = check_command('./hello', '--no-color')
    check_returncode(result)
    assert result.stdout == 'ℹ Hello, World, from cli.log.info!\nHello, World, from cli.echo!\n'


def test_hello_no_color_no_comma():
    result = check_command('./hello', '--no-color', '--no-comma')
    check_returncode(result)
    assert result.stdout == 'ℹ Hello World, from cli.log.info!\nHello World, from cli.echo!\n'


def test_hello_no_color_log_file():
    result = check_command('./hello', '--no-color', '--log-file', '/dev/stdout')
    check_returncode(result)
    assert result.stdout.startswith('[INFO] ')
    assert result.stdout.endswith('Hello, World, from cli.log.info!\nℹ Hello, World, from cli.log.info!\nHello, World, from cli.echo!\n')


def test_hello_no_color_verbose():
    result = check_command('./hello', '--no-color', '-v')
    check_returncode(result)
    assert result.stdout == '☐ You used -v you lucky person!\nℹ Hello, World, from cli.log.info!\nHello, World, from cli.echo!\n'
