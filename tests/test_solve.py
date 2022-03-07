from pathlib import Path
from click.testing import CliRunner

import pytest

THIS_DIR = Path(__file__).parent
INPUT = (THIS_DIR.parent / "pyroll" / "ui" / "cli" / "res" / "input_trio.py").read_text()
CONFIG = (THIS_DIR / "config.yaml").read_text()


def test_solve(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    from pyroll.ui.cli.program import main

    (tmp_path / "input.py").write_text(INPUT)
    (tmp_path / "config.yaml").write_text(CONFIG)

    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "input-py",
            "solve",
            "report",
        ],

    )

    print("\n")
    print(result.stdout)
    print(result.exception)

    assert result.exit_code == 0
