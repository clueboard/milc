from .common import check_command, check_returncode


def test_example_hello():
    result = check_command('./example', 'hello')
    check_returncode(result)
    assert result.stdout == 'Hello World!\n'


def test_example_goodbye():
    result = check_command('./example', 'goodbye')
    check_returncode(result)
    assert result.stdout == '\x1b[33m⚠\x1b[0m Parting is such sweet sorrow.\x1b[0m\nGoodbye, World!\n'


def test_example_goodbye_help():
    result = check_command('./example', 'goodbye', '--help')
    check_returncode(result)
    assert '[-f]' in result.stdout
    assert 'Write it in a flag' in result.stdout


def test_example_goodbye_flag():
    result = check_command('./example', '--no-color', 'goodbye', '-f')
    check_returncode(result)
    assert result.stdout == 'G                                       \no                                       \no                                       \nd                                       \nb                                       \ny                                       \ne                                       \n,                                       \n                                        \nW                                       \no                                       \nr                                       \nl                                       \nd                                       \n!                                       \n'
