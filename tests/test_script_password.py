from .common import check_assert, check_command, check_returncode

# FIXME: Use something like this here: https://stackoverflow.com/questions/41542960/run-interactive-bash-with-popen-and-a-dedicated-tty-python
# def test_password_complexity():
#    result = check_command('./passwd_complexity', '--interactive', input='aA1! \n')
#    check_returncode(result)
#    check_assert(result, 'Found 5 characters in the password!' in result.stdout)
#    check_assert(result, 'Found characters in 5 different character classes!' in result.stdout)


def test_password_complexity_no_input():
    result = check_command('./passwd_complexity')
    check_returncode(result, 1)
    check_assert(result, 'No password provided!' in result.stdout)


# def test_password_confirm():
#    result = check_command('./passwd_confirm', '--interactive', input='a\na')
#    check_returncode(result)
#    check_assert(result, 'Enter password:' in result.stdout)
#    check_assert(result, 'Confirm password:' in result.stdout)


def test_password_confirm_no_input():
    result = check_command('./passwd_confirm')
    check_returncode(result, 1)
