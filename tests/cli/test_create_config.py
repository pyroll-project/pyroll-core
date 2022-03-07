from pathlib import Path
from click.testing import CliRunner

import pytest


def test_create_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    from pyroll.ui.cli.program import main

    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "create-config",
        ],

    )

    print("\n")
    print(result.stdout)
    print(result.exception)

    assert result.exit_code == 0

    assert (tmp_path / "config.yaml").exists()
