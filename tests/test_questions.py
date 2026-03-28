"""Unit tests for milc.questions."""
import milc.questions


def test_format_prompt_no_args():
    """Ensure prompts without format args are returned unchanged (no ValueError for %% in prompt)."""
    assert milc.questions._format_prompt('Are you 50% sure?', (), {}) == 'Are you 50% sure?'


def test_format_prompt_with_args():
    """Ensure positional args are applied to the prompt."""
    assert milc.questions._format_prompt('Hello %s!', ('world',), {}) == 'Hello world!'


def test_format_prompt_with_kwargs():
    """Ensure keyword args are applied to the prompt."""
    assert milc.questions._format_prompt('Hello %(name)s!', (), {'name': 'world'}) == 'Hello world!'
