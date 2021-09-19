from .common import check_assert, check_command, check_returncode


def test_config_source():
    result = check_command('./config_source')
    check_returncode(result)
    check_assert(result, result.stdout == 'Hello, World, from None!\n')


def test_config_source_name():
    result = check_command('./config_source', '--name', 'World')
    check_returncode(result)
    check_assert(result, result.stdout == 'Hello, World, from argument!\n')
