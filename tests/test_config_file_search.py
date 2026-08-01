"""Tests for layered configuration file handling."""
import os
import subprocess
import sys
from configparser import RawConfigParser

import milc


def _create_config_file(path, contents):
    path.write_text(contents)


def _create_milc(monkeypatch, tmp_path, system_config_file=None, argv=None):
    platform_config_dir = tmp_path / 'platformdirs'
    monkeypatch.setattr(sys, 'argv', argv or ['application'])
    monkeypatch.setattr(milc.milc, 'user_config_dir', lambda **kwargs: str(platform_config_dir))
    return milc.milc.MILC(name='application', config_file=system_config_file), platform_config_dir / 'application.ini'


def test_platformdirs_config_overrides_and_merges_system_config(monkeypatch, tmp_path):
    system_config_file = tmp_path / 'system.ini'
    _create_config_file(system_config_file, '[general]\nshared = system\nsystem_only = yes\n')
    platform_config_dir = tmp_path / 'platformdirs'
    platform_config_dir.mkdir()
    _create_config_file(platform_config_dir / 'application.ini', '[general]\nshared = user\nuser_only = 42\n')
    monkeypatch.setattr(sys, 'argv', ['application'])
    monkeypatch.setattr(milc.milc, 'user_config_dir', lambda **kwargs: str(platform_config_dir))

    cli = milc.milc_interface.MILCInterface()
    cli.milc_options(name='application', config_file=system_config_file)

    assert cli.milc.config_file == (platform_config_dir / 'application.ini').resolve()
    assert cli.config.general.shared == 'user'
    assert cli.config.general.system_only is True
    assert cli.config.general.user_only == 42


def test_missing_system_config_still_loads_platformdirs_config(monkeypatch, tmp_path):
    platform_config_dir = tmp_path / 'platformdirs'
    platform_config_dir.mkdir()
    platform_config_file = platform_config_dir / 'application.ini'
    _create_config_file(platform_config_file, '[general]\nsource = user\n')

    milc, _ = _create_milc(monkeypatch, tmp_path, tmp_path / 'missing-system.ini')

    assert milc.config_file == platform_config_file.resolve()
    assert milc.config.general.source == 'user'


def test_normal_save_writes_merged_config_to_platformdirs(monkeypatch, tmp_path):
    system_config_file = tmp_path / 'system.ini'
    _create_config_file(system_config_file, '[general]\nsystem_only = system\n')
    platform_config_dir = tmp_path / 'platformdirs'
    platform_config_dir.mkdir()
    platform_config_file = platform_config_dir / 'application.ini'
    _create_config_file(platform_config_file, '[general]\nuser_only = user\n')

    milc, _ = _create_milc(monkeypatch, tmp_path, system_config_file)
    milc.save_config()

    saved_config = RawConfigParser()
    saved_config.read(platform_config_file)
    assert saved_config.get('general', 'system_only') == 'system'
    assert saved_config.get('general', 'user_only') == 'user'


def test_command_line_config_file_bypasses_system_and_platformdirs_configs(monkeypatch, tmp_path):
    system_config_file = tmp_path / 'system.ini'
    _create_config_file(system_config_file, '[general]\nsource = system\n')
    platform_config_dir = tmp_path / 'platformdirs'
    platform_config_dir.mkdir()
    _create_config_file(platform_config_dir / 'application.ini', '[general]\nsource = user\n')
    command_line_config_file = tmp_path / 'command-line.ini'
    _create_config_file(command_line_config_file, '[general]\nsource = command-line\n')

    milc, _ = _create_milc(monkeypatch, tmp_path, system_config_file, ['application', '--config-file', str(command_line_config_file)])

    assert milc.config_file == command_line_config_file.resolve()
    assert milc.config.general.source == 'command-line'


def test_config_output_exports_without_writing_platformdirs_config(tmp_path):
    system_config_file = tmp_path / 'system.ini'
    _create_config_file(system_config_file, '[general]\nsource = system\n')
    output_config_file = tmp_path / 'output.ini'
    script = tmp_path / 'application.py'
    script.write_text(
        """
import os

from milc import cli

cli.milc_options(name='application', config_file=os.environ['SYSTEM_CONFIG'])

import milc.subcommand.config


@cli.entrypoint('Test application.')
def main(cli):
    pass


if __name__ == '__main__':
    cli()
""".strip()
        + '\n'
    )
    environment = {**os.environ, 'SYSTEM_CONFIG': str(system_config_file), 'XDG_CONFIG_HOME': str(tmp_path / 'platformdirs')}

    result = subprocess.run([sys.executable, str(script), 'config', '--output', str(output_config_file)], capture_output=True, text=True, env=environment)

    assert result.returncode == 0, result.stdout + result.stderr
    exported_config = RawConfigParser()
    exported_config.read(output_config_file)
    assert exported_config.get('general', 'source') == 'system'
    assert not (tmp_path / 'platformdirs' / 'application' / 'application.ini').exists()
