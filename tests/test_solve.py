import logging
import sys
from pathlib import Path

from pyroll import solve
from pyroll.ui.report import Report


def test_solve(tmp_path: Path, caplog):
    caplog.set_level(logging.DEBUG, logger="pyroll")

    import pyroll.ui.cli.res.input_trio as input_py

    sequence = input_py.sequence

    solve(sequence, input_py.in_profile)

    report = Report()

    rendered = report.render(sequence)
    print()

    report_file = tmp_path / "report.html"
    report_file.write_text(rendered)
    print(report_file)

    print("\nLog:")
    print(caplog.text)
