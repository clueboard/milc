"""Unit tests for milc.configuration.Configuration.
"""
import milc.configuration


def configuration_setup():
    """Setup a simple milc.configuration.Configuration object for testing.
    """
    config = milc.configuration.Configuration()
    config['a']['a'] = True
    config['a']['a'] = True
    config['a']['b'] = False
    config['user']['d'] = 'arbitrary string'
    config['user']['d'] = 'arbitrary string'

    return config


def test_Configuration_dictionary():
    """Test Configuration dictionary access
    """
    config = configuration_setup()

    assert config['a']['a'] is True
    assert config['a']['b'] is False
    assert config['a']['c'] is None


def test_Configuration_attribute():
    """Test Configuration attribute access
    """
    config = configuration_setup()

    assert config.a.a is True
    assert config.a.b is False
    assert config.a.c is None


def test_Configuration_iteration():
    """Make sure we can iterate over our stored volues.
    """
    config = configuration_setup()

    for section, section_dict in config.items():
        if section == 'a':
            for key, value in section_dict.items():
                if key == 'a':
                    assert value is True
                elif key == 'b':
                    assert value is False
                else:
                    raise KeyError('Unexpected key found in configuration: ' + section + '.' + key)
        elif section == 'user':
            for key, value in section_dict.items():
                if key == 'd':
                    assert value == 'arbitrary string'
                else:
                    raise KeyError('Unexpected key found in configuration: ' + section + '.' + key)
        else:
            raise KeyError('Unexpected section found in configuration: ' + section)


def test_Configuration_parent_fallback():
    """Make sure that we properly pull in the parent value when the local value doesn't exist.
    """
    config = configuration_setup()

    assert config.a.d == 'arbitrary string'
