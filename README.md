# PyRoll Rolling Simulation Framework

Welcome to The PyRoll Project!

PyRoll is an OpenSource rolling framework, aimed to provide a fast and extensible base for rolling simulation.
The current focus lies on groove rolling in elongation grooves.
The core package comes with a basic set of models to allow a first estimation of forces and torques occurring in a pass
sequence.
There is a flexible plugin system, able to modify and extend the model set available to describe the process.

## Installation

The PyRoll Core package is installable via [PyPI](https://pypi.org)

```shell
pip install pyroll
```

A collection of plugin packages can be installed the same way, the packages names usually start with `pyroll-`.
Use the [PyPI search](https://pypi.org/search/?q=pyroll) or look at the
projects [GitHub page](https://github.com/pyroll-project) for discovering plugins.

## Basic Usage

The package provides a simple CLI tool that can be used to load input data, run the solution procedure and export the
solution data.
The CLI provides several commands that can and must be chained in one call.
No state is preserved between different program runs.

The simplest use case is to read from a python script, solve and render the results to an HTML report page.
The default input file is `input.py`, the default report file `report.html`.

```shell
pyroll input-py solve report
```

One may specify the files explicitly with the `-f`/`--file` option:

```shell
pyroll input-py -f other_input.py solve report -f other_report.html
```

A most basic input file may look like:

```python
from pyroll.core import Profile, RollPass, Transport, Roll, DiamondGroove, SquareGroove

in_profile = Profile.square(
    side=45e-3, corner_radius=3e-3,
    temperature=1200 + 273.15, flow_stress=100e6, strain=0,
)

sequence = [
    RollPass(
        label="Diamond I", velocity=1, gap=3e-3,
        roll=Roll(
            groove=DiamondGroove(
                usable_width=76.5e-3, tip_depth=22e-3, r1=12e-3, r2=8e-3
            ),
            nominal_radius=160e-3
        )
    ),
    Transport(duration=2),
    RollPass(
        label="Square II", velocity=1, gap=3e-3,
        roll=Roll(
            groove=SquareGroove(
                usable_width=52.7e-3, tip_depth=26e-3, r1=8e-3, r2=6e-3
            ),
            nominal_radius=160e-3
        )
    ),
]
```

The file must define the variables `in_profile` and `sequence` defining the state of the initial workpiece and the
sequence of roll passes and transport ranges.
For a more advanced example, representing a pass sequence at the 3-high mill at the Institute of Metals Forming, run:

```shell
pyroll create-input-py -k trio -f input.py
```

The PyRoll command line interface resides additionally on a YAML configuration file `config.yaml`.
The default file can be created using the following command:

```shell
pyroll create-config
```

The core section of this file is the `plugins` section.
Here one can specify a list of plugins that will be loaded in each simulation run.
Another way of loading plugins is to directly import them in the input Python script.

It is recommended to create a fresh directory for each simulation project to avoid the need to specify the filenames explicitly.
A basic input and config file can be created in the current directory using

```shell
pyroll new
```

One may also use the appropriate classes and functions directly from Python code, see
the [documentation](https://pyroll.readthedocs.io/en/latest) for more examples.

## Documentation

See the [documentation](https://pyroll.readthedocs.io/en/latest) to learn about basic concepts and
usage.

## License

The project is licensed under the [BSD 3-Clause license](LICENSE).

## Contributing

Since the project is currently in initial state, we would ask you to contact us first if you would like to contribute.
This helps to avoid unnecessary effort by you and us. Use the issue system
or [mail us](mailto:kalibrierzentrum@imf.tu-freiberg.de). If you want to create your own plugin package, please use
the [plugin template](https://github.com/pyroll-project/pyroll-plugin-template) and follow the instructions there.

### Policy for Inclusion of Hooks in the Core

Since version 2.0 we try to include as many hooks as possible into the core, to tie down the nomenclature.
This seems necessary, since for the same concepts, often different terms exist in literature.
To avoid collisions and redundancies, it is better to include these hooks in the core, although some of them may come without implementation.
This improves the exchangeability of plugins.
If you like a hook to be included in the core, open an issue, or preferably, a pull request with the respective changes.
Supply your pull request with fallback implementations of the hook, if any meaningful exist.

From this policy we explicitly exclude hooks, that are solely of use for one model approach, namely "coefficients".
They are large in number across the whole plugin landscape, but usually named after the model and of no further use to other plugins.
So the benefit from including them in the core is small, while the pollution of the core would be exzessive.
If another plugin has to make use of them, just add a dependency for the respective source plugin.

A few examples for clarification:

- The hooks `Profile.surface_temperature` and `Profile.core_temperature` may be of interests to many plugins.
  The core provides fallbacks which just return `self.temperature`, which is a good first estimate of those.
  So plugins modelling surface and thermal effects can easily refer to the respective temperatures, without worrying, if there is a model describing the temperature gradient or not.
- The hook `Profile.freiberg_flow_stress_coefficients` from the `pyroll-freiberg-flow-stress` plugin makes no sense without the Freiberg flow stress model, so it is not included in the core.
- The hook `Profile.thermal_conductivity` is a material property useful to many plugins, but no meaningful fallback exists, since there is no default material.
  So the provision of values or implementations is deferred to the user or developers of material databases.

So the core includes several hooks, that are not used by other core functionality, but provide a save ground for plugins.

## Roadmap

See the [roadmap](ROADMAP.md) for information about ongoing development and future plans.