<a name="attrdict"></a>

# attrdict

<a name="attrdict.AttrDict"></a>

## AttrDict Objects

```python
class AttrDict(object)
```

A dictionary that can also be accessed by attribute.

<a name="attrdict.AttrDict.__getitem__"></a>

#### \_\_getitem\_\_

```python
 | __getitem__(key)
```

Returns an item.

<a name="attrdict.SparseAttrDict"></a>

## SparseAttrDict Objects

```python
class SparseAttrDict(AttrDict)
```

A dictionary that can also be accessed by attribute.

This class never raises IndexError, instead it will return None if a
key does not yet exist.

<a name="attrdict.SparseAttrDict.__getitem__"></a>

#### \_\_getitem\_\_

```python
 | __getitem__(key)
```

Returns an item, creating it if it doesn't already exist

