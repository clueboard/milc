# Sparklines

A sparkline is a tool for displaying numerical information in a very compact format. You can read more about them in [an article by Jon Udell](https://blog.jonudell.net/2021/08/05/the-tao-of-unicode-sparklines/).

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

## Optimization

If you need to optimize the performance of a sparkline, or you want to set the boundaries for your data, you can supply min and max values when creating your sparkline:

```python
from milc import sparkline

print(sparkline([5, 9, 2, 3, 6, 9, 3, 5, 6], 2, 9)
```

Any values that fall outside your min and max will be ignored.
