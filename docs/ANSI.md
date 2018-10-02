# Working With ANSI In Your Script

CLIM supports colorizing your output with ANSI colors. You can colorize the
text both for log output and when `print()`ing directly.

## Colorizing Log Output

If you are using the built-in log facility it couldn't be easier- just add curly-braced delimited color names to your log strings. They will automatically output color or not as appropriate.

### Colored Log Example

    cli.log.error('{bg_red}{fg_white}Could not open file %s!', filename)

## Colorizing print()

If you want to colorize output yourself you will find a dictionary of ANSI
colors in `cli.ansi`. You can use this to colorize text in whatever way you'd
like.

NOTE: Make sure you end all your printed output with
`cli.ansi['style_reset_all']` or you may find yourself with a funky and/or
broken terminal after your program exits.

## Colored Print Example

    text = '{bg_blue}{fg_white}|___|\\___|{style_reset_all} ' \
           '{bg_red}{fg_white}SHARK ATTACK!{style_reset_all}'
    print(text.format(**cli.ansi))

## Available Colors

Colors prefixed with 'fg' will affect the foreground (text) color. Colors
prefixed with 'bg' will affect the background color. Colors prefixed with
style affect how bright the text will be, except for `{style_reset_all}`
which resets the text back to the terminal's default colors.

* {fg_black}
* {fg_blue}
* {fg_cyan}
* {fg_green}
* {fg_lightblack_ex}
* {fg_lightblue_ex}
* {fg_lightcyan_ex}
* {fg_lightgreen_ex}
* {fg_lightmagenta_ex}
* {fg_lightred_ex}
* {fg_lightwhite_ex}
* {fg_lightyellow_ex}
* {fg_magenta}
* {fg_red}
* {fg_reset}
* {fg_white}
* {fg_yellow}
* {bg_black}
* {bg_blue}
* {bg_cyan}
* {bg_green}
* {bg_lightblack_ex}
* {bg_lightblue_ex}
* {bg_lightcyan_ex}
* {bg_lightgreen_ex}
* {bg_lightmagenta_ex}
* {bg_lightred_ex}
* {bg_lightwhite_ex}
* {bg_lightyellow_ex}
* {bg_magenta}
* {bg_red}
* {bg_reset}
* {bg_white}
* {bg_yellow}
* {style_bright}
* {style_dim}
* {style_normal}
* {style_reset_all}
