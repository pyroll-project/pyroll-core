# Units

Think of a rolling process as of a sequence of roll passes and intermediate times, called transports. Both are subsumed
under the term *unit*. The `Unit` class is the base class representing this concept.

It defines three attributes:

| Attribute     | Description                                                               |
|---------------|---------------------------------------------------------------------------|
| `label`       | A label string for human identification, used in log messages and output. |
| `in_profile`  | The profile that represents the incoming workpiece state into the unit.   |
| `out_profile` | The profile that represents the outgoing workpiece state out of the unit. |

Currently, two derived classes exist in the core library: [`RollPass`](roll_pass.md) and [`Transport`](transport.md).

The unit class defines an abstract method `solve(in_profile: Profile)`, which triggers the solution procedure an accepts
a profile object that has to be treated as the incoming profile. This object in copied and modified and made available
in the `in_profile` attribute by the implementations of this method.

Also, it maintains hooks that should be applicable to all types of units.

> To read about the basics of hooks and plugins, see [here](../plugins.md).
