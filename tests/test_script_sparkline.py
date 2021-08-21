from .common import check_assert, check_command, check_returncode


def test_sparkline():
    result = check_command('./sparkline')
    check_returncode(result)
    check_assert(result, 'ℹ sparkline1: ▁▂▁▃ ▄▁█▂▄▃\nℹ sparkline2: ▁▁██\nℹ sparkline3: ▁▁▅▅██')
