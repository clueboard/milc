from .common import check_assert, check_command, check_returncode


def test_questions():
    result = check_command('./questions')
    check_returncode(result)
    check_assert(result, 'User has chosen to stop.' in result.stdout)
    check_assert(result, 'User is stopping.' in result.stdout)
    check_assert(result, 'Interesting answer: None' in result.stdout)


def test_questions_interactive():
    result = check_command('./questions', '--interactive', input='y\n2\nbecause\n')
    check_returncode(result)
    check_assert(result, 'User has chosen to continue.' in result.stdout)
    check_assert(result, 'User is not stopping.' in result.stdout)
    check_assert(result, 'Interesting answer: because' in result.stdout)


def test_questions_yes():
    result = check_command('./questions', '--yes')
    check_returncode(result)
    check_assert(result, 'User has chosen to continue.' in result.stdout)
    check_assert(result, 'User is stopping.' in result.stdout)
    check_assert(result, 'Interesting answer: None' in result.stdout)


def test_questions_no():
    result = check_command('./questions', '--no')
    check_returncode(result)
    check_assert(result, 'User has chosen to stop.' in result.stdout)
    check_assert(result, 'User is stopping.' in result.stdout)
    check_assert(result, 'Interesting answer: None' in result.stdout)
