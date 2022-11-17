import logging
from importlib import reload
from pathlib import Path

from pyroll.core import solve
from pyroll.ui import report


def test_solve_min(tmp_path: Path, caplog):
    caplog.set_level(logging.DEBUG, logger="pyroll")

    import pyroll.ui.cli.res.input_min as input_py
    reload(input_py)

    sequence = input_py.sequence

    solve(sequence, input_py.in_profile)

    rendered = report(sequence)
    print()

    report_file = tmp_path / "report.html"
    report_file.write_text(rendered)
    print(report_file)

    print("\nLog:")
    print(caplog.text)


def test_solve_three_high_rolling_plant(tmp_path: Path, caplog):
    caplog.set_level(logging.DEBUG, logger="pyroll")

    import pyroll.ui.cli.res.input_trio as input_py

    sequence = input_py.sequence

    solve(sequence, input_py.in_profile)

    rendered = report(sequence)
    print()

    report_file = tmp_path / "report.html"
    report_file.write_text(rendered)
    print(report_file)

    print("\nLog:")
    print(caplog.text)
