<a id="_sparkline"></a>

# \_sparkline

Display sparklines from a sequence of numbers.

<a id="_sparkline.is_number"></a>

#### is\_number

```python
def is_number(i)
```

Returns true if i is a number. Used to filter non-numbers from a list.

<a id="_sparkline.sparkline"></a>

#### sparkline

```python
def sparkline(number_list,
              *,
              min_value=None,
              max_value=None,
              highlight_low=-inf,
              highlight_high=inf,
              highlight_low_color='',
              highlight_high_color='',
              negative_color='{fg_red}',
              positive_color='',
              highlight_low_reset='{fg_reset}',
              highlight_high_reset='{fg_reset}',
              negative_reset='{fg_reset}',
              positive_reset='{fg_reset}')
```

Display a sparkline from a sequence of numbers.

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

