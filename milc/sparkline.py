#!/usr/bin/env python3
"""Display sparklines from a sequence of ints.
"""

spark_chars = '▁▂▃▄▅▆▇█'


def sparkline(ints, int_min=None, int_max=None):
    """Display a sparkline from a sequence of ints.
    """
    int_min = int_min or min(ints)
    int_max = int_max or max(ints)
    bucket_size = (int_max-int_min) / 8.0
    buckets = [i * bucket_size for i in range(8)]
    sparks = []

    for i in ints:
        if i < int_min:
            continue

        for bucket_num, bucket in enumerate(buckets):
            if i < bucket:
                sparks.append(spark_chars[bucket_num - 1])
                break

    return ''.join(sparks)


if __name__ == '__main__':
    print(sparkline(list(range(101))))
