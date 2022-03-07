import importlib.util
import logging.config
import logging
import re
import sys
from dataclasses import dataclass, field
from typing import List

import click
import yaml

import pyroll.core
from ...core import Profile
from ...core.unit import Unit

from pathlib import Path

RES_DIR = Path(__file__).parent / "res"
DEFAULT_INPUT_PY_FILE = "input.py"
DEFAULT_CONFIG_FILE = "config.yaml"
DEFAULT_REPORT_FILE = "report.html"
DEFAULT_EXPORT_FILE = "export.csv"


@dataclass
class State:
    sequence: List[Unit] = field(default_factory=list)
    in_profile: Profile = field(default_factory=lambda: None)
    config: dict = field(default_factory=dict)


@click.group(chain=True)
@click.pass_context
@click.option("--config-file", "-c", default=DEFAULT_CONFIG_FILE, help="The configuration YAML file.",
              type=click.Path())
@click.option("--plugin", "-p", multiple=True, default=[])
def main(ctx, config_file, plugin):
    state = State()
    ctx.obj = state

    config = yaml.safe_load((Path(__file__).parent / "res" / "config.yaml").read_text())

    if Path(config_file).exists():
        config.update(yaml.safe_load(Path(config_file).read_text()))

    state.config = config

    if "logging" in config:
        logging.config.dictConfig(config["logging"])
    else:
        logging.basicConfig(format='[%(levelname)s] %(name)s: %(message)s', stream=sys.stdout)

    log = logging.getLogger(__name__)

    plugins = list(plugin)
    if "plugins" in config:
        plugins += list(config["plugins"])

    for p in plugins:
        try:
            importlib.import_module(p)
        except:
            log.exception(f"Failed to import the plugin '{p}'.")
            raise

    if plugins:
        log.info(f"Loaded plugins: {plugins}.")


@main.command()
@click.option(
    "-f", "--file",
    help="File to load from.",
    type=click.Path(exists=True, dir_okay=False, writable=False, path_type=Path),
    default=DEFAULT_INPUT_PY_FILE, show_default=True
)
@click.pass_obj
@click.pass_context
def input_py(ctx, state: State, file: Path):
    """
    Reads input data from the Python script FILE.
    The script must define two attributes:

    in_profile:\t\tProfile object defining the entry shape in the first pass
    sequence:\titerable of Unit objects (RollPass or Transport) defining the pass sequence
    """

    log = logging.getLogger(__name__)
    log.info(f"Reading input from: {file.absolute()}")

    try:
        spec = importlib.util.spec_from_file_location("__pyroll_input__", file)
        module = importlib.util.module_from_spec(spec)
        sys.modules["__pyroll_input__"] = module
        spec.loader.exec_module(module)
        state.sequence = list(getattr(module, "sequence"))
        state.in_profile = getattr(module, "in_profile")
    except:
        log.exception("Error during reading of input file.")
        raise

    log.info(f"Finished reading input.")


@main.command()
@click.pass_obj
def solve(state):
    """Runs the solution procedure on all loaded roll passes."""
    log = logging.getLogger(__name__)

    log.info("Starting solution process...")
    pyroll.core.solve(state.sequence, state.in_profile)
    log.info("Finished solution process.")


@main.command()
@click.option(
    "-f", "--file",
    help="File to write to.",
    type=click.Path(dir_okay=False, path_type=Path),
    default=DEFAULT_REPORT_FILE, show_default=True
)
@click.pass_obj
def report(state: State, file: Path):
    """Generates a HTML report from the simulation results and writes it to FILE."""
    from ..report import Report
    log = logging.getLogger(__name__)

    rendered = Report().render(state.sequence)

    file.write_text(rendered, encoding='utf-8')
    log.info(f"Wrote report to: {file.absolute()}")


@main.command()
@click.option(
    "-f", "--file",
    help="File to write to.",
    type=click.Path(dir_okay=False, path_type=Path),
    default=DEFAULT_EXPORT_FILE, show_default=True
)
@click.option(
    "-F", "--format",
    help="Data format to export to.",
    default="csv", show_default=True
)
@click.pass_obj
def export(state: State, file: Path, format: str):
    """Generates a HTML report from the simulation results and writes it to FILE."""
    from ..exporter import Exporter
    log = logging.getLogger(__name__)

    exported = Exporter().export(state.sequence, format)

    file.write_bytes(exported)
    log.info(f"Wrote exported data to: {file.absolute()}")


@main.command()
@click.option(
    "-f", "--file",
    help="File to write to.",
    type=click.Path(dir_okay=False, path_type=Path),
    default=DEFAULT_CONFIG_FILE, show_default=True
)
@click.option(
    "-p", "--include-plugins",
    help="Whether to include a list of all installed plugins. A package is considered as plugin for PyRoll, if its name matches the regular expression 'pyroll.+'",
    type=click.BOOL,
    default=True, show_default=True
)
def create_config(file: Path, include_plugins: bool):
    """Creates a standard config in FILE that can be used with the -c option."""
    log = logging.getLogger(__name__)

    if file.exists():
        click.confirm(f"File {file} already exists, overwrite?", abort=True)

    content = (RES_DIR / "config.yaml").read_text()

    if include_plugins:
        import pkg_resources
        re_plugin = re.compile(r"pyroll.+")
        plugins = [
            dist.project_name.replace("-", "_")
            for dist in pkg_resources.working_set
            if re_plugin.match(dist.project_name)
        ]

        plugins_itemized = "\n".join([f"  - {p}" for p in plugins])
        content = re.sub(r"plugins:(.*)\n\s*\[\]", rf"plugins:\g<1>\n{plugins_itemized}", content)

    file.write_text(content, encoding='utf-8')
    log.info(f"Created config file in: {file.absolute()}")


@main.command()
@click.option(
    "-f", "--file",
    help="File to write to.",
    type=click.Path(dir_okay=False, path_type=Path),
    default=DEFAULT_INPUT_PY_FILE, show_default=True
)
def create_input_py(file: Path):
    """Creates a sample input script in FILE that can be loaded using input-py command."""
    log = logging.getLogger(__name__)

    if file.exists():
        click.confirm(f"File {file} already exists, overwrite?", abort=True)

    content = (RES_DIR / "input_trio.py").read_text()
    file.write_text(content, encoding='utf-8')
    log.info(f"Created input file in: {file.absolute()}")
