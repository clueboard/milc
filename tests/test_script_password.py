from .common import check_command, check_returncode

# FIXME: Use something like this here: https://stackoverflow.com/questions/41542960/run-interactive-bash-with-popen-and-a-dedicated-tty-python
# def test_password_complexity():
#    result = check_command('./passwd_complexity', '--interactive', input='aA1! \n')
#    check_returncode(result)
#    assert 'Found 5 characters in the password!' in result.stdout
#    assert 'Found characters in 5 different character classes!' in result.stdout


def test_password_complexity_no_input():
    result = check_command('./passwd_complexity')
    check_returncode(result, 1)
    assert 'No password provided!' in result.stdout


# def test_password_confirm():
#    result = check_command('./passwd_confirm', '--interactive', input='a\na')
#    check_returncode(result)
#    assert 'Enter password:' in result.stdout
#    assert 'Confirm password:' in result.stdout


def test_password_confirm_no_input():
    result = check_command('./passwd_confirm')
    check_returncode(result, 1)
