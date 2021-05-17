from milc import cli


def check_command(command, *args, input=None):
    cmd = [command] + list(args)
    return cli.run(cmd, combined_output=True, input=input)


def check_returncode(result, expected=0):
    """Print stdout if `result.returncode` does not match `expected`.
    """
    if result.returncode != expected:
        print('`%s` stdout:' % ' '.join(result.args))
        print(result.stdout)
        print('returncode:', result.returncode)
    assert result.returncode == expected
