---
title: Pass Sequence Units in PyRolL  
author: Max Weiner  
date: 2022-03-16
---

> **This part of the documentation is currently work in progress.**

Think of a rolling process as of a sequence of roll passes and intermediate times, called transports. Both are subsumed
under the term *unit*. The `Unit` class is the base class representing this concept.
A unit can most abstractly be considered as a black box transforming the state of a profile,
thus taking an incoming profile instance, simulation its evolution within the unit and yielding an outgoing profile instance.

It defines three attributes:

| Attribute     | Description                                                               |
|---------------|---------------------------------------------------------------------------|
| `label`       | A label string for human identification, used in log messages and output. |
| `in_profile`  | The profile that represents the incoming workpiece state of the unit.     |
| `out_profile` | The profile that represents the outgoing workpiece state of the unit.     |

Currently, two derived classes exist in the core library: [`RollPass`](units.md#roll-passes)
and [`Transport`](units.md#transports).

The unit class defines an abstract method `solve(in_profile: Profile)`, which triggers the solution procedure and accepts
a profile object that has to be treated as the incoming profile. This object is copied and modified and made available
in the `in_profile` attribute by the implementations of this method.

Also, the `Unit` class maintains hooks that should be applicable to all types of units.

> To read about the basics of hooks and plugins, see [here](plugins.md).

## Roll Passes

The roll pass is the most important unit, since forming of the workpiece is happening here.
It is represented by the `RollPass` class.
The `RollPass` constructor takes a `Roll` object, which is defining the properties of the working rolls including the groove.

### Rolls

Roll objects represent a working roll implemented in a rolling stand.
The main properties are about the geometry and rotational movement of the roll.
Rolls define the basic hooks specified below.
With appropriate plugins, elastic deformation of the rolls during the process can be modelled.

### Hooks

> To read about the basics of hooks and plugins, see [here](plugins.md).

On roll passes, several basic hooks are specified and implemented. You can provide your own implementations of them and
also specify new ones. The following are defined by default.

#### `RollPass`

```{eval-rst} 
.. automodule:: pyroll.core.roll_pass.hookspecs.roll_pass
    :members:
```

#### `Roll`

```{eval-rst} 
.. automodule:: pyroll.core.roll.hookspecs
    :members:
```

#### `RollPass.Roll`

```{eval-rst} 
.. automodule:: pyroll.core.roll_pass.hookspecs.roll
    :members:
```

#### `RollPass.Profile`

```{eval-rst} 
.. automodule:: pyroll.core.roll_pass.hookspecs.profile
    :members:
```

#### `RollPass.OutProfile`

```{eval-rst} 
.. automodule:: pyroll.core.roll_pass.hookspecs.out_profile
    :members:
```

Below you will find detailed descriptions of selected hooks as example of using them.

#### `in_profile_rotation`

The angle in degree by which the incoming profile is rotated at feeding into the roll pass. Currently only integers are
valid values. Per default common rotations are implemented for the available groove types. Typically you will use
the `applies_to_in_grooves` and `applies_to_in_grooves` decorators from `pyroll.utils` to provide new implementations.
The code block below shows an example implementation of this hook, the explicit `specname` is used to avoid naming
conflicts when providing more than one implementation in one file.

```python
@RollPass.hookimpl(specname="in_profile_rotation")
@applies_to_in_grooves("diamond")
@applies_to_out_grooves("diamond")
def diamonds(roll_pass):
    return 90
```

## Transports

### Hooks

> To read about the basics of hooks and plugins, see [here](plugins.md).

On transports, several basic hooks are specified and implemented. You can provide your own implementations of them and
also specify new ones. The following are defined by default.

#### `Transport`

```{eval-rst} 
.. automodule:: pyroll.core.transport.hookspecs.transport
    :members:
```

#### `Transport.OutProfile`

```{eval-rst} 
.. automodule:: pyroll.core.transport.hookspecs.out_profile
    :members:
```