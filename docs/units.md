# Units

> **This part of the documentation is currently work in progress.**

Think of a rolling process as of a sequence of roll passes and intermediate times, called transports. Both are subsumed
under the term *unit*. The `Unit` class is the base class representing this concept.

It defines three attributes:

| Attribute     | Description                                                               |
|---------------|---------------------------------------------------------------------------|
| `label`       | A label string for human identification, used in log messages and output. |
| `in_profile`  | The profile that represents the incoming workpiece state into the unit.   |
| `out_profile` | The profile that represents the outgoing workpiece state out of the unit. |

Currently, two derived classes exist in the core library: [`RollPass`](units.md#roll-passes)
and [`Transport`](units.md#transports).

The unit class defines an abstract method `solve(in_profile: Profile)`, which triggers the solution procedure an accepts
a profile object that has to be treated as the incoming profile. This object in copied and modified and made available
in the `in_profile` attribute by the implementations of this method.

Also, it maintains hooks that should be applicable to all types of units.

> To read about the basics of hooks and plugins, see [here](plugins.md).

## Roll Passes

The roll pass is the most important unit, since deformation is happening here. It is represented by the `RollPass`
class.

The constructor takes the basic attributes of the roll pass and additional keyword arguments.

| Argument      | Description                                                                      |
|---------------|----------------------------------------------------------------------------------|
| `groove`      | The groove object defining the shape of the roll gap, see [here](../grooves.md). |
| `roll_radius` | The mean roll radius of both rolls, measured at their flat surface.              |
| `velocity`    | Workpiece velocity in the roll pass.                                             |
| `gap`         | The gap between the flat surfaces of the rolls.                                  |
| `label`       | A label string for human identification, used in log messages and output.        |

The class provides several basics geometric attributes calculated from this information:

| Attribute              | Description                                            |
|------------------------|--------------------------------------------------------|
| `height`               | Maximum heigth of the roll gap.                        |
| `tip_width`            | $b_\mathrm{ks}$                                        |
| `usable_cross_section` | Cross-section of the roll gap bounded by usable width. |
| `tip_cross_section`    | Cross-section of the roll gap bounded by tip width.    |
| `minimal_roll_radius`  | Roll radius minus groove depth.                        |

### Hooks

> To read about the basics of hooks and plugins, see [here](../plugins.md).


## Transports
