from pathlib import Path
from click.testing import CliRunner

import pytest

THIS_DIR = Path(__file__).parent


def test_load_dummy_plugin(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    from pyroll.ui.cli.program import main

    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "create-config",
            "-p", "true"
        ],
    )

    print("\n")
    print(result.output)

    config_file = tmp_path / "config.yaml"

    assert config_file.exists()
    assert "pyroll.dummy_plugin" in config_file.read_text()


def test_plugin_load_throws(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    from pyroll.ui.cli.program import main

    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "-p",
            "not_present",
            "input-py",
        ],
    )

    print("\n")
    print(result.output)

    assert result.exit_code != 0
    assert isinstance(result.exception, ModuleNotFoundError)
