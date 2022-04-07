# Data Export

PyRoll includes a class capable of converting the simulation results to
a [pandas](https://pandas.pydata.org/) `DataFrame` and save this to different file formats. The feature can be accessed
by use of the CLI through the [`export`](cli.md#export) command.

The data included in the frame can be modified by hooks. The available file formats can be extended by the use of hooks.

> To read about the basics of hooks and plugins, see [here](plugins.md).

## Specifying data to include

There is a hook `columns(unit : Unit)` that can be used to specify the columns included in the data frame. One can use
the `pyroll.utils.hookutils.applies_to_unit_types(types)` decorator to specify the unit types the hook implementation
should apply to (currently only `Unit`, `RollPass`, `Transport`).

Each implementation must return a mapping of column names (string) to values (any type that can be data in
a `DataFrame`). The list of hook results will be combined to the final set of columns. Later registered implementations
will override earlier ones.

Define new implementations of this hook to include more data in the export. Commonly you would return a `dict` mapping
from `str` to a numeric type or string.

## Adding new file formats

For exporting to a file a hook is defined to handle the formatting:

    export(data: pandas.DataFrame, export_format: str)

It takes the generated `DataFrame` and a string specifying the format as arguments. Depending on the value
of `export_format` an implementation can decide whether it is able to handle the format or not. If it can, it should
return the binary data that will be saved to file. If it can not, it should return `None`. The first implementation not
returning `None` will be used for the file
content ([`firstresult`](https://pluggy.readthedocs.io/en/stable/#first-result-only)).

Current basic implementations support CSV and XML formats by use of the methods provided by `DataFrame`.

## Class Documentation

```{eval-rst}
.. autoclass:: pyroll.ui.exporter.Exporter
    :members:
```

## Hooks

```{eval-rst}
.. automodule:: pyroll.ui.exporter.hookspecs
    :members:
```