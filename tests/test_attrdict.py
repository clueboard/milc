"""Unit tests for milc.attrdict.
"""
import milc.attrdict


def attrdict_setup(attrdict=milc.attrdict.AttrDict):
    """Setup a simple AttrDict object for testing.
    """
    simple_dict = attrdict()
    simple_dict['a'] = True
    simple_dict['b'] = False

    return simple_dict


def test_AttrDict_dictionary():
    """Test AttrDict dictionary access
    """
    simple_dict = attrdict_setup()
    assert simple_dict['a'] is True
    assert simple_dict['b'] is False


def test_AttrDict_attribute():
    """Test AttrDict attribute access
    """
    simple_dict = attrdict_setup()
    assert simple_dict.a is True
    assert simple_dict.b is False


def test_AttrDict_invalid_dictionary():
    """Make sure invalid dictionary keys raise KeyError
    """
    simple_dict = attrdict_setup()

    try:
        simple_dict['c']
        raise KeyError('Should not be able to access non-existent key "c".')
    except KeyError:
        pass


def test_AttrDict_invalid_attribute():
    """Make sure invalid attributes raise KeyError
    """
    simple_dict = attrdict_setup()

    try:
        simple_dict.c
        raise KeyError('Should not be able to access non-existent attribute "c".')
    except KeyError:
        pass


def test_AttrDict_iteration():
    """Make sure we can iterate over our stored volues.
    """
    for key, value in attrdict_setup().items():
        if key == 'a':
            assert value is True
        elif key == 'b':
            assert value is False
        else:
            raise KeyError('Unexpected key found in attrdict: ' + key)


def test_SparseAttrDict_dictionary():
    """Test SparseAttrDict dictionary access.
    """
    simple_dict = attrdict_setup(milc.attrdict.SparseAttrDict)

    assert simple_dict['a'] is True
    assert simple_dict['b'] is False
    assert simple_dict['c'] is None


def test_SparseAttrDict_attribute():
    """Test SparseAttrDict attribute access.
    """
    simple_dict = attrdict_setup(milc.attrdict.SparseAttrDict)

    assert simple_dict.a is True
    assert simple_dict.b is False
    assert simple_dict.c is None
