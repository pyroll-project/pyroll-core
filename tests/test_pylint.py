import pathlib
import subprocess


def test_pylint_check():
    test_dir = pathlib.Path.cwd()
    repo_dir = test_dir.parent
    pyroll_dir = repo_dir / "pyroll"

    pylint_cmd = f"pylint {pyroll_dir}"
    result = subprocess.run(pylint_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    assert result.returncode == 0, f"Pylint check failed:\n{result.stderr}"
