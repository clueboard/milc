#!/usr/bin/env python3
"""Display sparklines from a sequence of ints.
"""

from milc import cli

spark_chars = '▁▂▃▄▅▆▇█'


def sparkline(ints, int_min=None, int_max=None):
    """Display a sparkline from a sequence of ints.
    """
    int_min = int_min or min(ints)
    int_max = int_max or max(ints)
    int_range = int_max - int_min
    sparks = []

    for i in ints:
        if i is None:
            sparks.append(' ')

        if i < int_min or i > int_max:
            cli.log.debug('Skipping out of bounds value %s', i)
            continue

        spark_char = (i-int_min) / int_range * 8

        if spark_char > 7:
            spark_char = 7

        sparks.append(spark_chars[min([7, int((i-int_min) / int_range * 8)])])

    return ''.join(sparks)


if __name__ == '__main__':
    print(sparkline(list(range(101))))
