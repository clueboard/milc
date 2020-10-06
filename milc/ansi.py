"""ANSI color support for MILC.
"""
import sys
import re
import logging
import colorama

from .emoji import EMOJI_LOGLEVELS

UNICODE_SUPPORT = sys.stdout.encoding.lower().startswith('utf')

# Regex was gratefully borrowed from kfir on stackoverflow:
# https://stackoverflow.com/a/45448194
ansi_regex = r'\x1b(' \
             r'(\[\??\d+[hl])|' \
             r'([=<>a-kzNM78])|' \
             r'([\(\)][a-b0-2])|' \
             r'(\[\d{0,2}[ma-dgkjqi])|' \
             r'(\[\d+;\d+[hfy]?)|' \
             r'(\[;?[hf])|' \
             r'(#[3-68])|' \
             r'([01356]n)|' \
             r'(O[mlnp-z]?)|' \
             r'(/Z)|' \
             r'(\d+)|' \
             r'(\[\?\d;\d0c)|' \
             r'(\d;\dR))'
ansi_escape = re.compile(ansi_regex, flags=re.IGNORECASE)
ansi_styles = (
    ('fg', colorama.ansi.AnsiFore()),
    ('bg', colorama.ansi.AnsiBack()),
    ('style', colorama.ansi.AnsiStyle()),
)
ansi_colors = {}

for prefix, obj in ansi_styles:
    for color in [x for x in obj.__dict__ if not x.startswith('_')]:
        ansi_colors[prefix + '_' + color.lower()] = getattr(obj, color)


def format_ansi(text):
    """Return a copy of text with certain strings replaced with ansi.
    """
    # Avoid .format() so we don't have to worry about the log content
    for color in ansi_colors:
        text = text.replace('{%s}' % color, ansi_colors[color])
    return text + ansi_colors['style_reset_all']


class ANSIFormatterMixin(object):
    """A log formatter mixin that inserts ANSI color.
    """
    def format(self, record):
        msg = super(ANSIFormatterMixin, self).format(record)
        return format_ansi(msg)


class ANSIStrippingMixin(object):
    """A log formatter mixin that strips ANSI.
    """
    def format(self, record):
        msg = super(ANSIStrippingMixin, self).format(record)
        record.levelname = ansi_escape.sub('', record.levelname)
        return ansi_escape.sub('', msg)


class EmojiLoglevelMixin(object):
    """A log formatter mixin that makes the loglevel an emoji on UTF capable terminals.
    """
    def format(self, record):
        if UNICODE_SUPPORT:
            record.levelname = EMOJI_LOGLEVELS[record.levelname].format(**ansi_colors)
        return super(EmojiLoglevelMixin, self).format(record)


class ANSIFormatter(ANSIFormatterMixin, logging.Formatter):
    """A log formatter that colorizes output.
    """
    pass


class ANSIStrippingFormatter(ANSIStrippingMixin, ANSIFormatterMixin, logging.Formatter):
    """A log formatter that strips ANSI
    """
    pass


class ANSIEmojiLoglevelFormatter(EmojiLoglevelMixin, ANSIFormatterMixin, logging.Formatter):
    """A log formatter that adds Emoji and ANSI
    """
    pass


class ANSIStrippingEmojiLoglevelFormatter(ANSIStrippingMixin, EmojiLoglevelMixin, ANSIFormatterMixin, logging.Formatter):
    """A log formatter that adds Emoji and strips ANSI
    """
    pass
