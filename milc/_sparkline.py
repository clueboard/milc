#!/usr/bin/env python3
"""Display sparklines from a sequence of ints.
"""

from milc import cli

spark_chars = '▁▂▃▄▅▆▇█'


def is_int(i):
    """Returns true if i is an int. Used to filter non-ints from a list.
    """
    return isinstance(i, int)


def sparkline(ints, int_min=None, int_max=None, negative_color='{fg_red}', negative_reset='{fg_reset}', positive_color='', positive_reset='{fg_reset}'):
    """Display a sparkline from a sequence of ints.

    If you wish to exclude extreme values, or you want to limit the set of characters used, you can adjust `int_min` and `int_max` to your own values. Values between your actual min/max will exclude datapoints, while values outside your actual min/max will compress your data into fewer sparks.

    By default this function will display negative numbers in red and positive numbers in the system default color. You can use `negative_color`, `negative_reset`, `positive_color`, and `positive_reset` to change this behavior. If you wish to color your sparkline according to other rules it is recommended you modify it after generating it.

    ### Arguments

        int_min
            The lowest value in your sparkline. If not provided it will be determined automatically.

        int_max
            The highest value in your sparkline. If not provided it will be determined automatically.

        negative_color
            A MILC or ANSI color code to apply to integers less than 0.

        negative_reset
            A MILC or ANSI color code to reset the color code applied in `negative_color`.

        positive_color
            A MILC or ANSI color code to apply to integers greater than 0.

        positive_reset
            A MILC or ANSI color code to reset the color code applied in `positive_color`.
    """
    int_min = int_min or min(filter(is_int, ints))
    int_max = int_max or max(filter(is_int, ints))
    int_range = int_max - int_min
    sparks = []

    for i in ints:
        if not is_int(i):
            sparks.append(' ')
            continue

        if i < int_min or i > int_max:
            cli.log.debug('Skipping out of bounds value %s', i)
            continue

        spark_int = (i-int_min) / int_range * 8

        if spark_int > 7:
            spark_int = 7

        spark_char = spark_chars[int(spark_int)]
        color = negative_color if i < 0 else positive_color
        reset = negative_reset if i < 0 else positive_reset

        sparks.append(''.join((color, spark_char, reset)))

    return ''.join(sparks)
