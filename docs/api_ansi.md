<a name=".ansi"></a>
## ansi

ANSI color support for MILC.

<a name=".ansi.format_ansi"></a>
#### format\_ansi

```python
format_ansi(text)
```

Return a copy of text with certain strings replaced with ansi.

<a name=".ansi.ANSIFormatter"></a>
### ANSIFormatter

```python
class ANSIFormatter(logging.Formatter)
```

A log formatter that inserts ANSI color.

<a name=".ansi.ANSIEmojiLoglevelFormatter"></a>
### ANSIEmojiLoglevelFormatter

```python
class ANSIEmojiLoglevelFormatter(ANSIFormatter)
```

A log formatter that makes the loglevel an emoji on UTF capable terminals.

<a name=".ansi.ANSIStrippingFormatter"></a>
### ANSIStrippingFormatter

```python
class ANSIStrippingFormatter(ANSIEmojiLoglevelFormatter)
```

A log formatter that strips ANSI.

