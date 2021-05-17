from .common import check_command, check_returncode


def test_questions():
    result = check_command('./questions')
    check_returncode(result)
    assert 'User has chosen to stop.' in result.stdout
    assert 'User is stopping.' in result.stdout
    assert 'Interesting answer: None' in result.stdout


def test_questions_interactive():
    result = check_command('./questions', '--interactive', input='y\n2\nbecause\n')
    check_returncode(result)
    assert 'User has chosen to continue.' in result.stdout
    assert 'User is not stopping.' in result.stdout
    assert 'Interesting answer: because' in result.stdout


def test_questions_yes():
    result = check_command('./questions', '--yes')
    check_returncode(result)
    assert 'User has chosen to continue.' in result.stdout
    assert 'User is stopping.' in result.stdout
    assert 'Interesting answer: None' in result.stdout


def test_questions_no():
    result = check_command('./questions', '--no')
    check_returncode(result)
    assert 'User has chosen to stop.' in result.stdout
    assert 'User is stopping.' in result.stdout
    assert 'Interesting answer: None' in result.stdout
