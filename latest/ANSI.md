# Working With ANSI In Your Script

MILC supports colorizing your output with ANSI colors. You can colorize the
text both for log output and when `cli.echo()`ing directly.

## Colorizing Log Output

If you are using the built-in log facility it couldn't be easier- just add
curly-braced delimited color names to your log strings. They will
automatically output color or not as appropriate.

### Colored Log Example

```python
cli.log.error('{bg_red}{fg_white}Could not open file %s!', filename)
```

## Colorizing Printed Output

You can use `cli.echo()` to print strings to stdout in the same way as
`cli.log`. Just add the ANSI token below to your string to colorize your
output.

### Colored Print Example

```python
text = '{bg_blue}{fg_white}|___|\\___|{style_reset_all} ' \
       '{bg_red}{fg_white}SHARK ATTACK!'
cli.echo(text)
```

## Available Colors

Colors prefixed with 'fg' will affect the foreground (text) color. Colors
prefixed with 'bg' will affect the background color. The included
`milc-color` command will show you what the colors look like in your
terminal.

| Color | Background | Extended Background | Foreground | Extended Foreground|
|-------|------------|---------------------|------------|--------------------|
| Black | {bg_black} | {bg_lightblack_ex} | {fg_black} | {fg_lightblack_ex} |
| Blue | {bg_blue} | {bg_lightblue_ex} | {fg_blue} | {fg_lightblue_ex} |
| Cyan | {bg_cyan} | {bg_lightcyan_ex} | {fg_cyan} | {fg_lightcyan_ex} |
| Green | {bg_green} | {bg_lightgreen_ex} | {fg_green} | {fg_lightgreen_ex} |
| Magenta | {bg_magenta} | {bg_lightmagenta_ex} | {fg_magenta} | {fg_lightmagenta_ex} |
| Red | {bg_red} | {bg_lightred_ex} | {fg_red} | {fg_lightred_ex} |
| White | {bg_white} | {bg_lightwhite_ex} | {fg_white} | {fg_lightwhite_ex} |
| Yellow | {bg_yellow} | {bg_lightyellow_ex} | {fg_yellow} | {fg_lightyellow_ex} |

There are also control sequences that can be used to change the behavior of
ANSI output:

| Control Sequences |
|-------------------|
| {style_bright} |
| {style_dim} |
| {style_normal} |
| {style_reset_all} |
| {bg_reset} |
| {fg_reset} |
