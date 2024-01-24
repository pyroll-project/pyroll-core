# PyRolL Rolling Simulation Framework

[![PyPI](https://img.shields.io/pypi/v/pyroll-core)](https://pypi.org/project/pyroll-core/)
![Python Versions](https://img.shields.io/pypi/pyversions/pyroll-core)
[![License](https://img.shields.io/pypi/l/pyroll-core)](LICENSE)
[![DOI](https://joss.theoj.org/papers/10.21105/joss.06200/status.svg)](https://doi.org/10.21105/joss.06200)
![Downloads](https://img.shields.io/pypi/dm/pyroll-core)
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/7971/badge)](https://www.bestpractices.dev/projects/7971)


Welcome to The PyRolL Project!

PyRolL is an OpenSource rolling framework, aimed to provide a fast and extensible base for rolling simulation.
The current focus lies on groove rolling in elongation grooves.
The core package includes the basic data structures and algorithms.
Further functionality is provided via [extension packages](https://pyroll.readthedocs.io/en/latest/extensions/index.html) and model approaches are provided via [plugin packages](https://pyroll.readthedocs.io/en/latest/plugins/index.html).

## Aim and Scope

Publications in the field of groove rolling simulation are, to the authors knowledge, characterized by lack of reproducibility, mainly because often details are missing regarding implementation or numerical solution procedure or the provided equations are erroneous.
Very few authors provide their source code alongside their publications.
PyRolL aims to change this by providing an open basis for model and methodology development.
The PyRolL Core package hosted in this repository is the common base dependency to refer to.
Plugins to the core provide model approaches for the partial problems to be described in a rolling simulation, which include mechanical, thermal, material behavior and more.
The library of available models is constantly growing and can be extended by everyone.
Extensions provide application logic and numerical procedures helping to analyse the subject rolling process regarding its technical feasibility, optimization potential, identity error sources, or, to design a new process.
PyRolL is therefore a tool for model developers, either with broad focus or specialists, wishing to try out for example a new physical material model within a real process simulation, as well as for technologists wishing to investigate a concrete process.
Currently, there is no click'n'run graphical user interface (GUI) provided, at least basic knowledge of programming in general and Python in particular is needed to use the software.
Nevertheless, this is also recommended to leverage the full power of PyRolL.

## Documentation

See the [documentation](https://pyroll.readthedocs.io/en/latest) to learn about basic concepts and
usage.
The documentation of version 1.0 can be found [here](https://pyroll.readthedocs.io/en/stable).

## Versions

The main branch of this repository contains the code of the version 2.0 of PyRolL.
See the [backport branch](https://github.com/pyroll-project/pyroll-core/tree/v1.0_backport) for the code of version 1.0.
Version 1.0 is now out of support, as version 2.0 has been released.
It is recommended to develop new plugins and extensions only for 2.0.

### Principal Changes of Version 2.0 Respective to 1.0

- Split of old `pyroll` package into `pyroll-core`, `pyroll-report`, `pyroll-export` and `pyroll-cli`.
- Complete reworking of the hook system.
    - Implementation of own hooking framework and removal of pluggy.
    - Simpler user interface for hook definition and implementation.
    - More orthodox default hook implementations, removal of "basic models".
- Rework of the object model.
    - Stricter hierarchy of unit classes.
    - Extended possibilities of groove definition.
    - Roll passes with three working rolls.
    - New unit classes: `Rotator`, `PassSequence`, `ThreeRollPass`.
    - Introduction of disk elements for incremental modelling in rolling direction.
    - Nestable units (esp. pass sequences and disk elements).

## License

The project is licensed under the [BSD 3-Clause license](LICENSE).

## Contributing

Feel free to open issues, or, fork and open pull requests, if you want to contribute to the core.
If you want to implement model approaches for use with PyRolL, create your own plugin package using our [plugin template](https://github.com/pyroll-project/pyroll-plugin-template).
To learn how to write plugins and extensions, please read the [documentation](https://pyroll.readthedocs.io/en/latest) and refer to the numerous existing plugins and extensions available at the [organization's GitHub page](https://github.com/pyroll-project).

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
