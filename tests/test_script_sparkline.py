from .common import check_assert, check_command, check_returncode


def test_sparkline():
    result = check_command('./sparkline', '--no-color')
    check_returncode(result)
    check_assert(result, result.stdout == 'ℹ sparkline1: ▄▄▃▅ ▆▃█▂▁▁\nℹ sparkline2: ▁▁██\nℹ sparkline3: ▁▁▅▅██\n')
