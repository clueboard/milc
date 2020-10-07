<a name="ansi"></a>
# ansi

ANSI color support for MILC.

<a name="ansi.format_ansi"></a>
#### format\_ansi

```python
format_ansi(text)
```

Return a copy of text with certain strings replaced with ansi.

<a name="ansi.ANSIFormatterMixin"></a>
## ANSIFormatterMixin Objects

```python
class ANSIFormatterMixin(object)
```

A log formatter mixin that inserts ANSI color.

<a name="ansi.ANSIStrippingMixin"></a>
## ANSIStrippingMixin Objects

```python
class ANSIStrippingMixin(object)
```

A log formatter mixin that strips ANSI.

<a name="ansi.EmojiLoglevelMixin"></a>
## EmojiLoglevelMixin Objects

```python
class EmojiLoglevelMixin(object)
```

A log formatter mixin that makes the loglevel an emoji on UTF capable terminals.

<a name="ansi.ANSIFormatter"></a>
## ANSIFormatter Objects

```python
class ANSIFormatter(ANSIFormatterMixin,  logging.Formatter)
```

A log formatter that colorizes output.

<a name="ansi.ANSIStrippingFormatter"></a>
## ANSIStrippingFormatter Objects

```python
class ANSIStrippingFormatter(ANSIStrippingMixin,  ANSIFormatterMixin,  logging.Formatter)
```

A log formatter that strips ANSI

<a name="ansi.ANSIEmojiLoglevelFormatter"></a>
## ANSIEmojiLoglevelFormatter Objects

```python
class ANSIEmojiLoglevelFormatter(EmojiLoglevelMixin,  ANSIFormatterMixin,  logging.Formatter)
```

A log formatter that adds Emoji and ANSI

<a name="ansi.ANSIStrippingEmojiLoglevelFormatter"></a>
## ANSIStrippingEmojiLoglevelFormatter Objects

```python
class ANSIStrippingEmojiLoglevelFormatter(ANSIStrippingMixin,  EmojiLoglevelMixin,  ANSIFormatterMixin,  logging.Formatter)
```

A log formatter that adds Emoji and strips ANSI

