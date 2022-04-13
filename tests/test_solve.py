import logging
from pathlib import Path

from pyroll import solve
from pyroll.ui.reporter import Reporter


def test_solve_min(tmp_path: Path, caplog):
    caplog.set_level(logging.DEBUG, logger="pyroll")

    import pyroll.ui.cli.res.input_min as input_py

    sequence = input_py.sequence

    solve(sequence, input_py.in_profile)

    report = Reporter()

    rendered = report.render(sequence)
    print()

    report_file = tmp_path / "report.html"
    report_file.write_text(rendered)
    print(report_file)

    print("\nLog:")
    print(caplog.text)


def test_solve_trio(tmp_path: Path, caplog):
    caplog.set_level(logging.DEBUG, logger="pyroll")

    import pyroll.ui.cli.res.input_trio as input_py

    sequence = input_py.sequence

    solve(sequence, input_py.in_profile)

    report = Reporter()

    rendered = report.render(sequence)
    print()

    report_file = tmp_path / "report.html"
    report_file.write_text(rendered)
    print(report_file)

    print("\nLog:")
    print(caplog.text)
