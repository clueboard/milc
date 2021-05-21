<a name="configuration"></a>
# configuration

<a name="configuration.Configuration"></a>
## Configuration Objects

```python
class Configuration(AttrDict)
```

Represents the running configuration.

This class never raises IndexError, instead it will return None if a
section or option does not yet exist.

<a name="configuration.Configuration.__getitem__"></a>
#### \_\_getitem\_\_

```python
 | __getitem__(key)
```

Returns a config section, creating it if it doesn't exist yet.

<a name="configuration.ConfigurationSection"></a>
## ConfigurationSection Objects

```python
class ConfigurationSection(Configuration)
```

<a name="configuration.ConfigurationSection.__getitem__"></a>
#### \_\_getitem\_\_

```python
 | __getitem__(key)
```

Returns a config value, pulling from the `user` section as a fallback.
This is called when the attribute is accessed either via the get method or through [ ] index.

<a name="configuration.ConfigurationSection.__getattr__"></a>
#### \_\_getattr\_\_

```python
 | __getattr__(key)
```

Returns the config value from the `user` section.
This is called when the attribute is accessed via dot notation but does not exist.

<a name="configuration.ConfigurationSection.__setattr__"></a>
#### \_\_setattr\_\_

```python
 | __setattr__(key, value)
```

Sets dictionary value when an attribute is set.

<a name="configuration.SubparserWrapper"></a>
## SubparserWrapper Objects

```python
class SubparserWrapper(object)
```

Wrap subparsers so we can track what options the user passed.

<a name="configuration.SubparserWrapper.completer"></a>
#### completer

```python
 | completer(completer)
```

Add an arpcomplete completer to this subcommand.

<a name="configuration.SubparserWrapper.add_argument"></a>
#### add\_argument

```python
 | add_argument(*args, **kwargs)
```

Add an argument for this subcommand.

This also stores the default for the argument in `self.cli.default_arguments`.

<a name="configuration.get_argument_name"></a>
#### get\_argument\_name

```python
get_argument_name(self, *args, **kwargs)
```

Takes argparse arguments and returns the dest name.

<a name="configuration.handle_store_boolean"></a>
#### handle\_store\_boolean

```python
handle_store_boolean(self, *args, **kwargs)
```

Does the add_argument for action='store_boolean'.

