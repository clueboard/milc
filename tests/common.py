import os
import subprocess


def check_command(command, *args, input=None):
    cmd = [command, *args]
    env = {**os.environ, 'PYTHONUTF8': '1'}

    if input:
        return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', input=input, env=env)

    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', env=env)


def check_returncode(result, expected=0):
    """Print stdout if `result.returncode` does not match `expected`.
    """
    if result.returncode != expected:
        print('`%s` stdout:' % ' '.join(result.args))
        print(result.stdout)
        print('returncode:', result.returncode)
    assert result.returncode == expected


def check_assert(result, assertion):
    if not assertion:
        print('`%s` stdout:' % ' '.join(result.args))
        print(repr(result.stdout))
        print('returncode:', result.returncode)
        raise AssertionError
