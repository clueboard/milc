"""Read and write configuration settings
"""
from typing import Any, Tuple

import milc
from milc.configuration import ConfigurationSection, _collect_config_sections, _config_navigate
from milc.milc import MILC


def print_config(section: str, key: str) -> None:
    """Print a single config setting to stdout.
    """
    config_section = _config_navigate(milc.cli.config, section)
    config_source_section = _config_navigate(milc.cli.config_source, section)
    source = config_source_section[key]
    if source == 'config_file':
        milc.cli.echo('%s.%s{fg_blue}={fg_reset}%s', section, key, config_section[key])
    elif source == 'env_var':
        milc.cli.echo('%s.%s{fg_yellow}={fg_reset}%s {fg_yellow}(env){fg_reset}', section, key, config_section[key])
    else:
        milc.cli.echo('{fg_cyan}%s.%s=%s', section, key, config_section[key])


def show_config() -> None:
    """Print the current configuration to stdout.
    """
    for section_name, key, value in sorted(_collect_config_sections(milc.cli.config)):
        config_source_section = _config_navigate(milc.cli.config_source, section_name)
        if config_source_section[key] in ('config_file', 'env_var') or milc.cli.config.config.all:
            print_config(section_name, key)


def parse_config_token(config_token: str) -> Tuple[str, str, Any]:
    """Split a user-supplied configuration-token into its components.
    """
    section = option = value = ''

    if '=' in config_token and '.' not in config_token:
        milc.cli.log.error('Invalid configuration token, the key must be of the form <section>.<option>: %s', config_token)
        return section, option, value

    # Separate the key (<section>.<option>) from the value
    if '=' in config_token:
        key, value = config_token.split('=', 1)
    else:
        key = config_token

    # Extract the section path and option from the key.
    # Split on the LAST dot so nested paths like 'remote.add.url' are handled:
    #   'remote.add.url' -> section='remote.add', option='url'
    #   'general.name'   -> section='general',    option='name'
    if '.' in key:
        section, option = key.rsplit('.', 1)
    else:
        section = key

    return section, option, value


def set_config(section: str, option: str, value: str) -> None:
    """Set a config key in the running config.
    """
    log_string = '%s.%s{fg_cyan}:{fg_reset} %s {fg_cyan}->{fg_reset} %s'

    if milc.cli.args.read_only:
        log_string += ' {fg_red}(change not written)'

    config_section = _config_navigate(milc.cli.config, section)
    milc.cli.echo(log_string, section, option, config_section[option], value)

    if not milc.cli.args.read_only:
        config_source_section = _config_navigate(milc.cli.config_source, section)
        if value == 'None':
            if option in config_section:
                del config_section[option]
            else:
                milc.cli.log.debug('No such configuration key: %s.%s', section, option)

        else:
            config_section[option] = value
            config_source_section[option] = 'config_file'


def _process_config_token(config_token: str) -> bool:
    """Process a single config token. Returns True if a write occurred.
    """
    section, option, value = parse_config_token(config_token)

    if section and option and value:
        set_config(section, option, value)
        return not milc.cli.args.read_only

    if section and option:
        config_section = _config_navigate(milc.cli.config, section)
        if isinstance(config_section[option], ConfigurationSection):
            full_section = f"{section}.{option}"
            nested = config_section[option]
            for section_name, key, value in _collect_config_sections(nested, full_section):
                src_section = _config_navigate(milc.cli.config_source, section_name)
                if src_section[key] in ('config_file', 'env_var'):
                    print_config(section_name, key)
        else:
            print_config(section, option)
        return False

    if section:
        config_section = _config_navigate(milc.cli.config, section)
        for section_name, key, value in _collect_config_sections(config_section, section):
            src_section = _config_navigate(milc.cli.config_source, section_name)
            if src_section[key] == 'config_file':
                print_config(section_name, key)

    return False


@milc.cli.argument('-a', '--all', action='store_true', help='Show all configuration options.')
@milc.cli.argument('-ro', '--read-only', arg_only=True, action='store_true', help='Operate in read-only mode.')
@milc.cli.argument('configs', nargs='*', arg_only=True, help='Configuration options to read or write.')
@milc.cli.subcommand("Read and write configuration settings.")
def config(cli: MILC) -> bool:
    """Read and write config settings.

    This script iterates over the config_tokens supplied as argument. Each config_token has the following form:

        section[.key][=value]

    For nested subcommands, section paths use dots: remote.add.url=https://...

    If only a section (EG 'compile') is supplied all keys for that section will be displayed.

    If section.key is supplied the value for that single key will be displayed.

    If section.key=value is supplied the value for that single key will be set.

    If section.key=None is supplied the key will be deleted.

    No validation is done to ensure that the supplied section.key is actually used by a subcommand.
    """
    if not milc.cli.args.configs:
        show_config()
        return False

    results = [_process_config_token(token) for token in milc.cli.args.configs]
    save_config = any(results)

    if save_config:
        milc.cli.save_config()

    return True
