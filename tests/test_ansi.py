"""Tests for milc/ansi.py

TODO:
    * skullydazed/anyone: Write tests for the log format classes
"""
import milc.ansi


def test_format_ansi():
    string = ''
    for color in milc.ansi.ansi_colors:
        string = string + '{' + color + '}'
    string = milc.ansi.format_ansi(string)

    assert string == '\x1b[30m\x1b[34m\x1b[36m\x1b[32m\x1b[90m\x1b[94m\x1b[96m\x1b[92m\x1b[95m\x1b[91m\x1b[97m\x1b[93m\x1b[35m\x1b[31m\x1b[39m\x1b[37m\x1b[33m\x1b[40m\x1b[44m\x1b[46m\x1b[42m\x1b[100m\x1b[104m\x1b[106m\x1b[102m\x1b[105m\x1b[101m\x1b[107m\x1b[103m\x1b[45m\x1b[41m\x1b[49m\x1b[47m\x1b[43m\x1b[1m\x1b[2m\x1b[22m\x1b[0m\x1b[0m'
