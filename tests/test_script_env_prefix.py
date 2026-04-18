import os
import subprocess
import sys
from tempfile import mkstemp

from .common import check_assert, check_returncode


def _run(env_overrides=None, extra_args=None):
    """Run env_prefix_example with optional env var overrides and extra CLI args."""
    env = {**os.environ, 'PYTHONUTF8': '1', **(env_overrides or {})}
    cmd = [sys.executable, 'env_prefix_example', '--no-color', '--config-file', os.devnull] + (extra_args or [])
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', env=env)


def _run_noprefix(env_overrides=None, extra_args=None):
    """Run env_prefix_noprefix_example with optional env var overrides and extra CLI args."""
    env = {**os.environ, 'PYTHONUTF8': '1', **(env_overrides or {})}
    cmd = [sys.executable, 'env_prefix_noprefix_example', '--no-color', '--config-file', os.devnull] + (extra_args or [])
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', env=env)


def _run_subc(env_overrides=None, extra_args=None):
    """Run env_prefix_subcommand_example with optional env var overrides and extra CLI args."""
    env = {**os.environ, 'PYTHONUTF8': '1', **(env_overrides or {})}
    cmd = [sys.executable, 'env_prefix_subcommand_example', '--no-color', '--config-file', os.devnull] + (extra_args or [])
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', env=env)


def test_env_prefix_sets_required_arg():
    """Env var satisfies a required argument."""
    result = _run(env_overrides={'MYAPP_HOST': 'myhost'})
    check_returncode(result)
    check_assert(result, 'host=myhost' in result.stdout)


def test_argv_overrides_env_var():
    """CLI argv takes priority over env var."""
    result = _run(env_overrides={'MYAPP_HOST': 'envhost'}, extra_args=['--host', 'clihost'])
    check_returncode(result)
    check_assert(result, 'host=clihost' in result.stdout)


def test_no_env_prefix_feature_disabled():
    """Without env_prefix, omitting a required arg still fails."""
    # Run env_prefix_example without setting the env var — required arg unsatisfied
    result = _run()
    check_returncode(result, expected=2)


def test_env_prefix_typed_int():
    """Env var value is coerced to int via the argument's type function."""
    result = _run(env_overrides={'MYAPP_HOST': 'myhost', 'MYAPP_PORT': '9090'})
    check_returncode(result)
    check_assert(result, 'port=9090' in result.stdout)


def test_env_prefix_store_true_truthy():
    """Env var 'true' is parsed as True for store_true arguments."""
    result = _run(env_overrides={'MYAPP_HOST': 'myhost', 'MYAPP_VERBOSE': 'true'})
    check_returncode(result)
    check_assert(result, 'verbose=True' in result.stdout)


def test_env_prefix_store_true_falsy():
    """Env var 'false' is parsed as False for store_true arguments."""
    result = _run(env_overrides={'MYAPP_HOST': 'myhost', 'MYAPP_VERBOSE': 'false'})
    check_returncode(result)
    check_assert(result, 'verbose=False' in result.stdout)


def test_env_prefix_store_true_off_is_falsy():
    """Env var 'off' is parsed as False for store_true arguments."""
    result = _run(env_overrides={'MYAPP_HOST': 'myhost', 'MYAPP_VERBOSE': 'off'})
    check_returncode(result)
    check_assert(result, 'verbose=False' in result.stdout)


def test_env_prefix_empty_no_prefix():
    """env_prefix='' means env vars are consulted without any prefix."""
    result = _run_noprefix(env_overrides={'HOST': 'barehost'})
    check_returncode(result)
    check_assert(result, 'host=barehost' in result.stdout)


def test_provenance_env_var_source():
    """config_source reflects env var provenance."""
    result = _run(env_overrides={'MYAPP_HOST': 'provenancehost'})
    check_returncode(result)
    check_assert(result, 'host_source=env_var' in result.stdout)


def test_provenance_argv_source():
    """config_source shows 'argument' when value comes from argv."""
    result = _run(env_overrides={'MYAPP_HOST': 'envhost'}, extra_args=['--host', 'clihost'])
    check_returncode(result)
    check_assert(result, 'host_source=argument' in result.stdout)


def test_env_prefix_type_error_message():
    """Bad env var type produces a readable error at parse time, not a traceback at import time."""
    result = _run(env_overrides={'MYAPP_HOST': 'myhost', 'MYAPP_PORT': 'notanumber'})
    check_returncode(result, expected=2)
    check_assert(result, 'MYAPP_PORT' in result.stdout)
    check_assert(result, 'notanumber' in result.stdout)
    check_assert(result, 'Traceback' not in result.stdout)


def test_store_boolean_truthy_env_var():
    """Env var 'true' enables a store_boolean argument."""
    result = _run(env_overrides={'MYAPP_HOST': 'myhost', 'MYAPP_COLORS': 'true'})
    check_returncode(result)
    check_assert(result, 'colors=True' in result.stdout)


def test_store_boolean_falsy_env_var():
    """Env var 'false' disables a store_boolean argument."""
    result = _run(env_overrides={'MYAPP_HOST': 'myhost', 'MYAPP_COLORS': 'false'})
    check_returncode(result)
    check_assert(result, 'colors=False' in result.stdout)


def test_store_boolean_cli_overrides_env_var():
    """Passing --no-colors on CLI overrides a truthy env var."""
    result = _run(env_overrides={'MYAPP_HOST': 'myhost', 'MYAPP_COLORS': 'true'}, extra_args=['--no-colors'])
    check_returncode(result)
    check_assert(result, 'colors=False' in result.stdout)


def test_env_prefix_type_error_help_reachable():
    """--help is reachable even when a type-coercion env var error is pending."""
    result = _run(env_overrides={'MYAPP_HOST': 'myhost', 'MYAPP_PORT': 'notanumber'}, extra_args=['--help'])
    check_returncode(result)
    check_assert(result, 'usage' in result.stdout.lower())


def test_subcommand_env_var_uses_section_prefix():
    """Subcommand --host reads MYAPP_SUBC_HOST, not MYAPP_HOST."""
    result = _run_subc(env_overrides={'MYAPP_HOST': 'global', 'MYAPP_SUBC_HOST': 'subchost'}, extra_args=['subc'])
    check_returncode(result)
    check_assert(result, 'subc_host=subchost' in result.stdout)


def test_entrypoint_env_var_not_leaked_to_subcommand():
    """MYAPP_HOST set for entrypoint does not affect subcommand --host."""
    result = _run_subc(env_overrides={'MYAPP_HOST': 'global'}, extra_args=['subc'])
    check_returncode(result)
    check_assert(result, 'subc_host=subc-default' in result.stdout)


def test_entrypoint_env_var_with_subcommand_present():
    """MYAPP_HOST still applies to the entrypoint's --host even when a subcommand is run."""
    result = _run_subc(env_overrides={'MYAPP_HOST': 'global'})
    check_returncode(result)
    check_assert(result, 'host=global' in result.stdout)


def test_nargs_env_var_ignored():
    """nargs='+' arguments are not populated from env vars — default is used."""
    result = _run(env_overrides={'MYAPP_HOST': 'myhost', 'MYAPP_TAGS': 'a b c'})
    check_returncode(result)
    check_assert(result, 'tags=[]' in result.stdout)


def test_nargs_cli_still_works():
    """nargs='+' arguments still work when passed on the CLI."""
    result = _run(env_overrides={'MYAPP_HOST': 'myhost'}, extra_args=['--tags', 'x', 'y'])
    check_returncode(result)
    check_assert(result, "tags=['x', 'y']" in result.stdout)


def test_nargs_int_env_var_ignored():
    """nargs=N (integer) arguments are not populated from env vars — default is used."""
    result = _run(env_overrides={'MYAPP_HOST': 'myhost', 'MYAPP_PAIR': 'a b'})
    check_returncode(result)
    check_assert(result, 'pair=[]' in result.stdout)


def test_append_action_env_var_ignored():
    """action='append' arguments are not populated from env vars — default is used."""
    result = _run(env_overrides={'MYAPP_HOST': 'myhost', 'MYAPP_LABEL': 'foo'})
    check_returncode(result)
    check_assert(result, 'label=[]' in result.stdout)


def test_nargs_question_mark_env_var_ignored():
    """nargs='?' arguments are not populated from env vars — default is used."""
    result = _run(env_overrides={'MYAPP_HOST': 'myhost', 'MYAPP_OUTPUT': 'file.txt'})
    check_returncode(result)
    check_assert(result, 'output=None' in result.stdout)


def test_nargs_remainder_env_var_ignored():
    """nargs=argparse.REMAINDER arguments are not populated from env vars — default is used."""
    result = _run(env_overrides={'MYAPP_HOST': 'myhost', 'MYAPP_REST': 'a b c'})
    check_returncode(result)
    check_assert(result, 'rest=[]' in result.stdout)


def test_env_var_overrides_config_file():
    """Env var takes priority over a value written to the config file."""
    fd, tempfile = mkstemp()
    try:
        os.close(fd)
        with open(tempfile, 'w') as f:
            f.write('[general]\nhost = "confighost"\n')
        env = {**os.environ, 'PYTHONUTF8': '1', 'MYAPP_HOST': 'envhost'}
        result = subprocess.run(
            [sys.executable, 'env_prefix_example', '--no-color', '--config-file', tempfile],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            env=env,
        )
        check_returncode(result)
        check_assert(result, 'host=envhost' in result.stdout)
        check_assert(result, 'host_source=env_var' in result.stdout)
    finally:
        os.remove(tempfile)
