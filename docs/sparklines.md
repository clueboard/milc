# Sparklines

A sparkline is a tool for displaying numerical information in a very compact format. You can read more about the general concept on [the Wikipedia page](https://en.wikipedia.org/wiki/Sparkline) and read about Unicode sparklines specifically in [an article by Jon Udell](https://blog.jonudell.net/2021/08/05/the-tao-of-unicode-sparklines/).

## Usage

Basic usage of a sparkline is simple:

```python
from milc import sparkline

print(sparkline([5, 9, 2, 3, 6, 9, 3, 5, 6])
```

This will output the following text:

```
▆▃▄▇▄▆▇
```

## Whitespace

Any item in your sparkline sequence that is not a number (`int`, `float`, or `decimal.Decimal`) will be rendered as a blank space. It is recommended that you consistently use the same object for this purpose, I prefer `None`.

Input:

```python
from milc import sparkline

print(sparkline([3, 7, None, 2, 1])
```

Output:

```
▃█ ▂▁
```

## Color

MILC supports coloring your sparkline in two different ways. You can combine these for a total of 4 colors per sparkline.

### Negative and Positive Numbers

By default your sparkline will be un-colored for positive numbers and red for negative numbers. You can change the colors for these by passing the following parameters:

* `negative_color`
* `negative_reset`
* `positive_color`
* `positive_reset`

These accept [MILC color codes](ANSI.md#available-colors).

### Highlight Color

If you want to highlight datapoints that higher or lower than a threshold you can do so by passing in `highlight_low`, `highlight_high`, and the associated color codes. These accept [MILC color codes](ANSI.md#available-colors).

You will need to set a color for your highlight, one is not set by default. The correct arguments to pass for each are listed below. By default the reset codes are set to `{fg_reset}`. If you are setting other attributes too you will need to adjust this by passing the correct reset code as well.

* `highlight_low`: `highlight_low_color` and `highlight_low_reset`
* `highlight_high`: `highlight_high_color` and `highlight_high_reset`

## Optimization

If you need to optimize the performance of a sparkline, or you want to set the boundaries for your data, you can supply min and max values when creating your sparkline. This will avoid two iterations over the list to find min and max values.

```python
from milc import sparkline

print(sparkline([5, 9, 2, 3, 6, 9, 3, 5, 6], 2, 9)
```

Any values that fall outside your min and max will be ignored.
