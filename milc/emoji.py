"""Emoji used by MILC when outputting logs

| Log Level | Emoji |
|-----------|-------|
| `CRITICAL` | `{bg_red}{fg_white}¬_¬{style_reset_all}` |
| `ERROR` | `{fg_red}☒{style_reset_all}` |
| `WARNING` | `{fg_yellow}⚠{style_reset_all}` |
| `INFO` | `{fg_blue}ℹ{style_reset_all}` |
| `DEBUG` | `{fg_cyan}☐{style_reset_all}` |
| `NOTSET` | `{style_reset_all}¯\\_(o_o)_/¯` |
"""
EMOJI_LOGLEVELS = {
    'CRITICAL': '{bg_red}{fg_white}¬_¬{style_reset_all}',
    'ERROR': '{fg_red}☒{style_reset_all}',
    'WARNING': '{fg_yellow}⚠{style_reset_all}',
    'INFO': '{fg_blue}ℹ{style_reset_all}',
    'DEBUG': '{fg_cyan}☐{style_reset_all}',
    'NOTSET': '{style_reset_all}¯\\_(o_o)_/¯'
}
EMOJI_LOGLEVELS['FATAL'] = EMOJI_LOGLEVELS['CRITICAL']
EMOJI_LOGLEVELS['WARN'] = EMOJI_LOGLEVELS['WARNING']
