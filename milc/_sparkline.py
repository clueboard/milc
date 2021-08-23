#!/usr/bin/env python3
"""Display sparklines from a sequence of numbers.
"""
from decimal import Decimal
from math import inf

from milc import cli

spark_chars = '▁▂▃▄▅▆▇█'


def is_number(i):
    """Returns true if i is a number. Used to filter non-numbers from a list.
    """
    return isinstance(i, (int, float, Decimal))


def sparkline(number_list, *, min_value=None, max_value=None, highlight_low=-inf, highlight_high=inf, highlight_low_color='', highlight_high_color='', negative_color='{fg_red}', positive_color='', highlight_low_reset='{fg_reset}', highlight_high_reset='{fg_reset}', negative_reset='{fg_reset}', positive_reset='{fg_reset}'):
    """Display a sparkline from a sequence of numbers.

    If you wish to exclude extreme values, or you want to limit the set of characters used, you can adjust `min_value` and `max_value` to your own values. Values between your actual min/max will exclude datapoints, while values outside your actual min/max will compress your data into fewer sparks.

    If you want to highlight data that is too low or too high you can use 'highlight_low' and `highlight_high` to set this. You will also need to set your colors, see below for more details.

    By default this function will display negative numbers in red and positive numbers in the system default color. You can use `negative_color`, `negative_reset`, `positive_color`, and `positive_reset` to change this behavior.

    If you wish to color your sparkline according to other rules it is recommended to generate it without color and then add color yourself.

    ### Arguments

        min_value
            The lowest value in your sparkline. If not provided it will be determined automatically.

        max_value
            The highest value in your sparkline. If not provided it will be determined automatically.

        highlight_low
            When a number is less than this value it will be highlighted with `highlight_low_color`.

        highlight_high
            When a number is greater than this value it will be highlighted with `highlight_high_color`.

        highlight_low_color
            A MILC or ANSI color code to apply to integers greater than highlight_low.

        highlight_high_color
            A MILC or ANSI color code to apply to integers greater than highlight_high.

        negative_color
            A MILC or ANSI color code to apply to integers less than 0.

        positive_color
            A MILC or ANSI color code to apply to integers greater than 0.

        highlight_low_reset
            A MILC or ANSI color code to reset the color code applied in `highlight_low_color`. This is usually `{fg_reset}`, `{bg_reset}`, or `{style_reset_all}`.

        highlight_high_reset
            A MILC or ANSI color code to reset the color code applied in `highlight_high_color`. This is usually `{fg_reset}`, `{bg_reset}`, or `{style_reset_all}`.

        negative_reset
            A MILC or ANSI color code to reset the color code applied in `negative_color`. This is usually `{fg_reset}`, `{bg_reset}`, or `{style_reset_all}`.

        positive_reset
            A MILC or ANSI color code to reset the color code applied in `positive_color`. This is usually `{fg_reset}`, `{bg_reset}`, or `{style_reset_all}`.
    """
    if min_value is None:
        min_value = min(filter(is_number, number_list))

    if max_value is None:
        max_value = max(filter(is_number, number_list))

    int_range = max_value - min_value
    sparks = []

    for i in number_list:
        # Handle non-numeric and out-of-bounds values
        if not is_number(i):
            sparks.append(' ')
            continue

        if i < min_value or i > max_value:
            cli.log.debug('Skipping out of bounds value %s', i)
            continue

        # Determine the bucket for this value
        spark_int = (i-min_value) / int_range * 8

        if spark_int > 7:
            spark_int = 7

        # Determine the color for this value
        color = positive_color
        reset = positive_reset

        if i < 0:
            color = negative_color
            reset = negative_reset

        if i < highlight_low:
            color = highlight_low_color
            reset = highlight_low_reset

        if i > highlight_high:
            color = highlight_high_color
            reset = highlight_high_reset

        if color == '':
            reset = ''

        # Add this spark to the list
        sparks.append(''.join((color, spark_chars[int(spark_int)], reset)))

    return ''.join(sparks)
