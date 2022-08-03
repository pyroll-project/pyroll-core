# The Plugin System

PyRolL is mainly built on the plugin system [pluggy](https://pluggy.readthedocs.io), which is also used in well known
projects like [pytest](https://docs.pytest.org) and [pytask](https://pytask-dev.readthedocs.io). Many core
functionalities are also implemented as plugins. The PyRolL Core project only implements a minimal set of model
approaches, look into the various official and unofficial plugins available for more.

Unlike the other mentioned projects, PyRolL has not only one plugin system, but several. Many main classes of PyRolL
hold class attributes used to maintain plugins on that class, these are in detail:

| Attribute        | Description                                                                                                                                           |
|------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| `plugin_manager` | A {py:class}`pluggy.PluginManager` instance used to maintain the plugins on this class.                                                               |
| `hookspec`       | A wrapper around a {py:class}`pluggy.HookspecMarker` instance for defining new hook specifications. Supports only a subset of the original arguments. |
| `hookimpl`       | A wrapper around a {py:class}`pluggy.HookimplMarker` instance for defining new hook implementations.                                                  |

This is implemented using the {py:class}`pyroll.plugin_host.PluginHost` class and the {py:class}`pyroll.plugin_host.PluginHostMeta` metaclass.

```{eval-rst}
.. autoclass:: pyroll.core.plugin_host.PluginHostMeta
    :members:
```

```{eval-rst}
.. autoclass:: pyroll.core.plugin_host.PluginHost
    :members:
    :special-members: __getattr__
```

The `hookspec` markers of all classes derived from [`Unit`](units.md) ([`RollPass`](units.md#roll-passes)
and [`Transport`](units.md#transports)) and [`Profile`](profile.md) are preconfigured
as [`firstresult`](https://pluggy.readthedocs.io/en/stable/#first-result-only). That means, that the first hook
implementation, that returns not `None` is used as only result of the hook call. This offers the possibility of
implementing many specialized versions of a hook and fall back to general ones if no special one applies.

Almost every attribute on the mentioned classes can be represented by a hook. This is achieved by
overriding `__getattr__`, so that if no attribute with a desired name is present on an object, the framework searches
for a hook of equal name. If there is no such hook, or the hook call results in `None`, an error is raised. Therefore,
it is easy to specify new hooks, just use the `hookspec` marker on a dummy function and add it to the `plugin_manager`
by use of `plugin_manager.add_hookspecs()`. It is common in writing plugins for PyRolL to specify hooks for all
intermediate and result values on profiles and units you want to calculate, and then to provide at least one general
implementation of them. Afterwards you can proceed providing more specialized implementations in the same plugin
package, or maybe also in another one if you need more flexibility in loading different implementations.

The classes [`Reporter`](report.md) and [`Exporter`](export.md) are also maintaining a plugin system, to allow plugins to
contribute their own results to the output. But those hooks are
not [`firstresult`](https://pluggy.readthedocs.io/en/stable/#first-result-only) per default and specifying new hooks is
not as easy as with units and profiles.

Details affecting only the distinct classes are described in their documentation.

For examples on specifying and implementing hooks, please read the [pluggy documentation](https://pluggy.readthedocs.io)
and look into the source code of PyRolL.