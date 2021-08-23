"""Unit tests for milc._sparkline.
"""
from milc import sparkline


def test_sparkline_simple():
    """Test a simple sparkline
    """
    assert sparkline([5, 9, 3, 15]) == '▂▅▁█'


def test_sparkline_corner1():
    """Test a common corner case
    """
    assert sparkline([0, 1, 19, 20]) == '▁▁██'


def test_sparkline_corner2():
    """Test a common corner case
    """
    assert sparkline([0, 999, 4000, 4999, 7000, 7999]) == '▁▁▅▅██'


def test_sparkline_negative():
    """Ensure that negative numbers are highlighted.
    """
    assert sparkline([-1, 0, 1]) == '{fg_red}▁{fg_reset}▅█'


def test_sparkline_negative_positive():
    """Ensure that negative and positive numbers are highlighted.
    """
    assert sparkline([-1, 0, 1], positive_color='{fg_green}') == '{fg_red}▁{fg_reset}{fg_green}▅{fg_reset}{fg_green}█{fg_reset}'


def test_sparkline_highlight_high():
    """Ensure that highlight high numbers are highlighted.
    """
    assert sparkline([0, 1, 2], highlight_high=1, highlight_high_color='{fg_magenta}') == '▁▅{fg_magenta}█{fg_reset}'


def test_sparkline_highlight_low():
    """Ensure that highlight low numbers are highlighted.
    """
    assert sparkline([0, 1, 2], highlight_low=1, highlight_low_color='{fg_magenta}') == '{fg_magenta}▁{fg_reset}▅█'


def test_whitespace():
    """Ensure that whitespace is properly inserted.
    """
    assert sparkline([0, None, 1]) == '▁ █'


def test_exclude():
    """Ensure that out-of-bounds values are excluded.
    """
    assert sparkline([-1, 0, None, 1, 2], min_value=0, max_value=1) == '▁ █'
