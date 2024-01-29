<a id="configuration"></a>

# configuration

<a id="configuration.Configuration"></a>

## Configuration Objects

```python
class Configuration(AttrDict)
```

Represents the running configuration.

This class never raises IndexError, instead it will return None if a
section or option does not yet exist.

<a id="configuration.Configuration.__getitem__"></a>

#### \_\_getitem\_\_

```python
def __getitem__(key: Hashable) -> Any
```

Returns a config section, creating it if it doesn't exist yet.

<a id="configuration.ConfigurationSection"></a>

## ConfigurationSection Objects

```python
class ConfigurationSection(Configuration)
```

<a id="configuration.ConfigurationSection.__getitem__"></a>

#### \_\_getitem\_\_

```python
def __getitem__(key: Hashable) -> Any
```

Returns a config value, pulling from the `user` section as a fallback.
This is called when the attribute is accessed either via the get method or through [ ] index.

<a id="configuration.ConfigurationSection.__getattr__"></a>

#### \_\_getattr\_\_

```python
def __getattr__(key: str) -> Any
```

Returns the config value from the `user` section.
This is called when the attribute is accessed via dot notation but does not exist.

<a id="configuration.ConfigurationSection.__setattr__"></a>

#### \_\_setattr\_\_

```python
def __setattr__(key: str, value: Any) -> None
```

Sets dictionary value when an attribute is set.

<a id="configuration.SubparserWrapper"></a>

## SubparserWrapper Objects

```python
class SubparserWrapper(object)
```

Wrap subparsers so we can track what options the user passed.

<a id="configuration.SubparserWrapper.completer"></a>

#### completer

```python
def completer(completer: Any) -> None
```

Add an arpcomplete completer to this subcommand.

<a id="configuration.SubparserWrapper.add_argument"></a>

#### add\_argument

```python
def add_argument(*args: Any, **kwargs: Any) -> None
```

Add an argument for this subcommand.

This also stores the default for the argument in `self.cli.default_arguments`.

<a id="configuration.get_argument_strings"></a>

#### get\_argument\_strings

```python
def get_argument_strings(arg_parser: Any, *args: Any,
                         **kwargs: Any) -> List[str]
```

Takes argparse arguments and returns a list of argument strings or positional names.

<a id="configuration.get_argument_name"></a>

#### get\_argument\_name

```python
def get_argument_name(arg_parser: Any, *args: Any, **kwargs: Any) -> Any
```

Takes argparse arguments and returns the dest name.

<a id="configuration.handle_store_boolean"></a>

#### handle\_store\_boolean

```python
def handle_store_boolean(self: Any, *args: Any, **kwargs: Any) -> Any
```

Does the add_argument for action='store_boolean'.

