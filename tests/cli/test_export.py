from pathlib import Path
from click.testing import CliRunner

import pytest

PARENT_DIR = Path(__file__).parent.parent
INPUT = (PARENT_DIR.parent / "pyroll" / "ui" / "cli" / "res" / "input_trio.py").read_text()
CONFIG = (PARENT_DIR / "config.yaml").read_text()


def test_export_csv(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
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
            "export"
        ],

    )

    print("\n")
    print(result.stdout)
    print(result.exception)

    assert result.exit_code == 0

    print((tmp_path / "export.csv").read_text())


def test_export_xml(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
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
            "export",
            "-F", "xml",
            "-f", "export.xml",
        ],

    )

    print("\n")
    print(result.stdout)
    print(result.exception)

    assert result.exit_code == 0

    print((tmp_path / "export.xml").read_text())
