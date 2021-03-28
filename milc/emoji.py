"""Emoji used by MILC when outputting logs

| Log Level | Emoji |
|-----------|-------|
| `CRITICAL` | `{bg_red}{fg_white}¬_¬` |
| `ERROR` | `{fg_red}☒` |
| `WARNING` | `{fg_yellow}⚠` |
| `INFO` | `{fg_blue}ℹ` |
| `DEBUG` | `{fg_cyan}☐` |
| `NOTSET` | `{style_reset_all}¯\\_(o_o)_/¯` |
"""
EMOJI_LOGLEVELS = {
    'CRITICAL': '{bg_red}{fg_white}¬_¬',
    'ERROR': '{fg_red}☒',
    'WARNING': '{fg_yellow}⚠',
    'INFO': '{fg_blue}ℹ',
    'DEBUG': '{fg_cyan}☐',
    'NOTSET': '{style_reset_all}¯\\_(o_o)_/¯',
}
EMOJI_LOGLEVELS['FATAL'] = EMOJI_LOGLEVELS['CRITICAL']
EMOJI_LOGLEVELS['WARN'] = EMOJI_LOGLEVELS['WARNING']
