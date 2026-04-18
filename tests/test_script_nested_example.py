import os
import sys
from tempfile import mkstemp

from .common import check_assert, check_command, check_returncode


# ---------------------------------------------------------------------------
# Top-level help
# ---------------------------------------------------------------------------

def test_top_level_help_lists_only_top_level_subcommands():
    """Top-level --help metavar must NOT include grandchild commands."""
    result = check_command(sys.executable, 'nested_example', '--help')
    check_returncode(result)
    # Top-level subcommands appear in the metavar
    check_assert(result, 'remote' in result.stdout)
    check_assert(result, 'sub1' in result.stdout)
    check_assert(result, 'sub2' in result.stdout)
    check_assert(result, 'info' in result.stdout)
    # Grandchild names must not bleed into the top-level metavar block
    # (they may appear elsewhere in help text, so just check the metavar line)
    first_line = result.stdout.split('\n')[0]
    check_assert(result, 'remote.add' not in first_line)


# ---------------------------------------------------------------------------
# Parent fallback handlers
# ---------------------------------------------------------------------------

def test_remote_no_child_runs_fallback():
    """Invoking a parent subcommand without a child runs its handler."""
    result = check_command(sys.executable, 'nested_example', '--config-file', os.devnull, 'remote')
    check_returncode(result)
    # remote() calls cli.print_help() which outputs usage; just verify no crash
    check_assert(result, result.returncode == 0)


def test_remote_help_lists_child_commands():
    result = check_command(sys.executable, 'nested_example', 'remote', '--help')
    check_returncode(result)
    check_assert(result, 'add' in result.stdout)
    check_assert(result, 'remove' in result.stdout)


# ---------------------------------------------------------------------------
# Argument routing for nested subcommands
# ---------------------------------------------------------------------------

def test_remote_add_default_args():
    result = check_command(sys.executable, 'nested_example', '--no-color', '--config-file', os.devnull, 'remote', 'add')
    check_returncode(result)
    check_assert(result, 'add: url= fetch=False' in result.stdout)


def test_remote_add_with_url():
    result = check_command(sys.executable, 'nested_example', '--no-color', '--config-file', os.devnull, 'remote', 'add', '--url', 'https://example.com')
    check_returncode(result)
    check_assert(result, 'url=https://example.com' in result.stdout)
    check_assert(result, 'fetch=False' in result.stdout)


def test_remote_add_with_fetch():
    result = check_command(sys.executable, 'nested_example', '--no-color', '--config-file', os.devnull, 'remote', 'add', '--fetch')
    check_returncode(result)
    check_assert(result, 'fetch=True' in result.stdout)


def test_remote_remove():
    result = check_command(sys.executable, 'nested_example', '--no-color', '--config-file', os.devnull, 'remote', 'remove', '--name', 'origin')
    check_returncode(result)
    check_assert(result, 'remove: name=origin' in result.stdout)


# ---------------------------------------------------------------------------
# Same function name under different parents (id-based dispatch)
# ---------------------------------------------------------------------------

def test_sub1_add_dispatches_correctly():
    result = check_command(sys.executable, 'nested_example', '--no-color', '--config-file', os.devnull, 'sub1', 'add')
    check_returncode(result)
    check_assert(result, 'sub1 add' in result.stdout)
    check_assert(result, 'sub2 add' not in result.stdout)


def test_sub2_add_dispatches_correctly():
    result = check_command(sys.executable, 'nested_example', '--no-color', '--config-file', os.devnull, 'sub2', 'add')
    check_returncode(result)
    check_assert(result, 'sub2 add' in result.stdout)
    check_assert(result, 'sub1 add' not in result.stdout)


# ---------------------------------------------------------------------------
# subcommand_name and subcommand_path
# ---------------------------------------------------------------------------

def test_info_subcommand_name_and_path():
    result = check_command(sys.executable, 'nested_example', '--no-color', '--config-file', os.devnull, 'info')
    check_returncode(result)
    check_assert(result, 'name=info' in result.stdout)
    check_assert(result, 'path=info' in result.stdout)


def test_info_nested_subcommand_name_and_path():
    result = check_command(sys.executable, 'nested_example', '--no-color', '--config-file', os.devnull, 'info', 'nested')
    check_returncode(result)
    check_assert(result, 'name=nested' in result.stdout)
    check_assert(result, 'path=info.nested' in result.stdout)


# ---------------------------------------------------------------------------
# Config subcommand with dotted paths
# ---------------------------------------------------------------------------

def test_config_set_and_read_nested_key():
    fd, tempfile = mkstemp()

    try:
        os.close(fd)

        # Set a nested config value
        result = check_command(sys.executable, 'nested_example', '--no-color', '--config-file', tempfile, 'config', 'remote.add.url=https://stored.example.com')
        check_returncode(result)
        check_assert(result, 'remote.add.url' in result.stdout)
        check_assert(result, 'https://stored.example.com' in result.stdout)

        # Read it back
        result = check_command(sys.executable, 'nested_example', '--no-color', '--config-file', tempfile, 'config', 'remote.add.url')
        check_returncode(result)
        check_assert(result, 'https://stored.example.com' in result.stdout)

    finally:
        os.remove(tempfile)


def test_config_show_nested_section():
    fd, tempfile = mkstemp()

    try:
        os.close(fd)

        # Write two values under remote.add
        result = check_command(sys.executable, 'nested_example', '--no-color', '--config-file', tempfile, 'config', 'remote.add.url=https://example.com', 'remote.add.fetch=true')
        check_returncode(result)

        # Show the remote.add section
        result = check_command(sys.executable, 'nested_example', '--no-color', '--config-file', tempfile, 'config', 'remote.add')
        check_returncode(result)
        check_assert(result, 'remote.add.url' in result.stdout)
        check_assert(result, 'remote.add.fetch' in result.stdout)

    finally:
        os.remove(tempfile)


# ---------------------------------------------------------------------------
# Config file round-trip: write [remote.add] section, read back via config
# ---------------------------------------------------------------------------

def test_config_file_roundtrip_nested_subcommand():
    fd, tempfile = mkstemp()

    try:
        os.close(fd)

        # Set value via config subcommand (writes INI file)
        result = check_command(sys.executable, 'nested_example', '--no-color', '--config-file', tempfile, 'config', 'remote.add.url=https://roundtrip.example.com')
        check_returncode(result)

        # Read value back by running the actual subcommand (reads INI file into config)
        result = check_command(sys.executable, 'nested_example', '--no-color', '--config-file', tempfile, 'remote', 'add')
        check_returncode(result)
        check_assert(result, 'url=https://roundtrip.example.com' in result.stdout)

    finally:
        os.remove(tempfile)
