# The Concept of Profiles

```{py:currentmodule} pyroll.core.profile
```

Think of a {py:class}`Profile` object as of a state of the workpiece anywhere in the pass sequence. Every sequence unit
has an incoming and an outgoing profile. Also, you must provide a profile as definition for the initial workpiece being
processed in the pass sequence.

Profiles Each profile has a certain shape, defined by the `upper_contour_line` and `lower_contour_line` and its main
dimensions `height` and `width`.

For creating an initial profile, several class methods exist in the {py:class}`Profile` class. One can either derive the
profile shape from an existing groove object by use of the {py:meth}`Profile.from_groove` method, or created some
standard shapes use of the other class methods of {py:class}`Profile`, like {py:meth}`Profile.round`. More values can be
given as keyword arguments and are saved automatically as attributes in the instance. Which you may or must provide
depends on the loaded plugins.

```{eval-rst}
.. autoclass:: Profile
    :members:
```

## Hooks

> To read about the basics of hooks and plugins, see [here](plugins.md).

The following hooks are defined on plain profiles per default:

```{eval-rst} 
.. automodule:: pyroll.core.profile.hookspecs
    :members:
```

## Derived classes

For the units types [`RollPass`](units.md#roll-passes) and [`Transport`](units.md#transports), specialized versions of
the `Profile` class are defined as nested classes within the respective unit class. They all maintain their own hooks,
so it is possible to specify hooks on profiles only for those places, were they are applicable.

All hooks on those classes receive additionally to the profile instance also the instance of the roll pass or transport
they are belonging to.