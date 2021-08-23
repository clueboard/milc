<a id="_sparkline"></a>

# \_sparkline

Display sparklines from a sequence of numbers.

<a id="_sparkline.is_number"></a>

#### is\_number

```python
is_number(i)
```

Returns true if i is a number. Used to filter non-numbers from a list.

<a id="_sparkline.sparkline"></a>

#### sparkline

```python
sparkline(number_list, *, min_value=None, max_value=None, highlight_threshold=inf, highlight_color='', negative_color='{fg_red}', positive_color='', highlight_reset='{fg_reset}', negative_reset='{fg_reset}', positive_reset='{fg_reset}')
```

Display a sparkline from a sequence of numbers.

If you wish to exclude extreme values, or you want to limit the set of characters used, you can adjust `min_value` and `max_value` to your own values. Values between your actual min/max will exclude datapoints, while values outside your actual min/max will compress your data into fewer sparks.

If you want to highlight data that is too high you can use `highlight_threshold` to set this. Any number in your list that exceeds that threshold will be colored with `highlight_color`.

By default this function will display negative numbers in red and positive numbers in the system default color. You can use `negative_color`, `negative_reset`, `positive_color`, and `positive_reset` to change this behavior.

If you wish to color your sparkline according to other rules it is recommended to generate it without color and then add color yourself.

### Arguments

    min_value
        The lowest value in your sparkline. If not provided it will be determined automatically.

    max_value
        The highest value in your sparkline. If not provided it will be determined automatically.

    highlight_threshold
        When a number is greater than this value it will be highlighted with `highlight_color`.

    highlight_color
        A MILC or ANSI color code to apply to integers greater than highlight_threshold.

    negative_color
        A MILC or ANSI color code to apply to integers less than 0.

    positive_color
        A MILC or ANSI color code to apply to integers greater than 0.

    highlight_reset
        A MILC or ANSI color code to reset the color code applied in `highlight_color`. This is usually `{fg_reset}`, `{bg_reset}`, or `{style_reset_all}`.

    negative_reset
        A MILC or ANSI color code to reset the color code applied in `negative_color`. This is usually `{fg_reset}`, `{bg_reset}`, or `{style_reset_all}`.

    positive_reset
        A MILC or ANSI color code to reset the color code applied in `positive_color`. This is usually `{fg_reset}`, `{bg_reset}`, or `{style_reset_all}`.

