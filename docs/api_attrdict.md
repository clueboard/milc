<a id="attrdict"></a>

# attrdict

<a id="attrdict.AttrDict"></a>

## AttrDict Objects

```python
class AttrDict(object)
```

A dictionary that can also be accessed by attribute.

<a id="attrdict.AttrDict.__getitem__"></a>

#### \_\_getitem\_\_

```python
def __getitem__(key: Any) -> Any
```

Returns an item.

<a id="attrdict.SparseAttrDict"></a>

## SparseAttrDict Objects

```python
class SparseAttrDict(AttrDict)
```

A dictionary that can also be accessed by attribute.

This class never raises IndexError, instead it will return None if a
key does not yet exist.

<a id="attrdict.SparseAttrDict.__getitem__"></a>

#### \_\_getitem\_\_

```python
def __getitem__(key: Any) -> Any
```

Returns an item, creating it if it doesn't already exist

