"""Test milc.questions
"""
from unittest.mock import patch

import milc.questions


@patch('builtins.input', return_value='y', autospec=True)
@patch('builtins.print', autospec=True)
def test_yesno_y(mock_inputs, mock_outputs):
    """Make sure an answer of 'y' returns True
    """
    answer = milc.questions.yesno('')
    assert answer is True


@patch('builtins.input', return_value='n', autospec=True)
@patch('builtins.print', autospec=True)
def test_yesno_n(mock_inputs, mock_outputs):
    """Make sure an answer of 'n' returns False
    """
    assert milc.questions.yesno('') is False


@patch('builtins.input', return_value='', autospec=True)
@patch('builtins.print', autospec=True)
def test_yesno_default(mock_inputs, mock_outputs):
    """Make sure a blank answer returns True
    """
    assert milc.questions.yesno('', default=True) is True


@patch('builtins.input', return_value='hi', autospec=True)
@patch('builtins.print', autospec=True)
def test_question(mock_inputs, mock_outputs):
    """Make sure we get 'hi' back from the input.
    """
    assert milc.questions.question('') == 'hi'


@patch('builtins.input', return_value='', autospec=True)
@patch('builtins.print', autospec=True)
def test_question_default(mock_inputs, mock_outputs):
    """Make sure a blank answer returns True
    """
    assert milc.questions.question('', default=True) is True


@patch('builtins.input', return_value='1', autospec=True)
@patch('builtins.print', autospec=True)
def test_choice_1(mock_inputs, mock_outputs):
    """Make we get back the right answer.
    """
    assert milc.questions.choice('', [True, False, 'hi']) is True


@patch('builtins.input', return_value='3', autospec=True)
@patch('builtins.print', autospec=True)
def test_choice_3(mock_inputs, mock_outputs):
    """Make we get back the right answer.
    """
    assert milc.questions.choice('', [True, False, 'hi']) == 'hi'


@patch('builtins.input', return_value='', autospec=True)
@patch('builtins.print', autospec=True)
def test_choice_default(mock_inputs, mock_outputs):
    """Make we get back the right answer.
    """
    assert milc.questions.choice('', [True, False, 'hi'], default=2) == 'hi'
