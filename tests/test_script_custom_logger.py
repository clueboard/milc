from .common import check_assert, check_command, check_returncode


def test_custom_logger():
    result = check_command('./custom_logger')
    check_returncode(result)
    check_assert(result, 'INFO:custom_logger:Hello Info World!' in result.stdout)
    check_assert(result, 'DEBUG:custom_logger:Hello Debug World!' in result.stdout)
