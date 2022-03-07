# The `RollPass` class

The roll pass is the most important unit, since deformation is happening here.

The constructor takes the basic attributes of the roll pass and additional keyword arguments.

| Argument      | Description                                                                              |
|---------------|------------------------------------------------------------------------------------------|
| `groove`      | The groove object defining the shape of the roll gap, see [here](../grooves/grooves.md). |
| `roll_radius` | The mean roll radius of both rolls, measured at their flat surface.                      |
| `velocity`    | Workpiece velocity in the roll pass.                                                     |
| `gap`         | The gap between the flat surfaces of the rolls.                                          |
| `label`       | A label string for human identification, used in log messages and output.                |

The class provides several basics geometric attributes calculated from this information:

| Attribute              | Description                                            |
|------------------------|--------------------------------------------------------|
| `height`               | Maximum heigth of the roll gap.                        |
| `tip_width`            | $`b_\mathrm{ks}`$                                      |
| `usable_cross_section` | Cross-section of the roll gap bounded by usable width. |
| `tip_cross_section`    | Cross-section of the roll gap bounded by tip width.    |
| `minimal_roll_radius`  | Roll radius minus groove depth.                        |

## Hooks

> To read about the basics of hooks and plugins, see [here](../plugins.md).


