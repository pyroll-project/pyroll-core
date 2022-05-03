# The Concept of Profiles

Think of a `Profile` object as of a state of the workpiece anywhere in the pass sequence. Every sequence unit has an
incoming and an outgoing profile. Also, you must provide a profile as definition for the initial workpiece being
processed in the pass sequence.

## Main Attributes and Properties

| Attribute | Description                                                                                  |
|-----------|----------------------------------------------------------------------------------------------|
| `groove`  | Groove object defining the shape of the profile, see [here](grooves.md).                     |
| `height`  | Dimension of the profile in height direction ($y$ direction of the groove coordinate system) |
| `width`   | Dimension of the profile in width direction ($z$ direction of the groove coordinate system)  |
| `strain`  | Equivalent strain of the profile material, mainly used for flow stress calculation.          |

Each profile has a certain shape, defined by the `groove` contour from which the profile was formed and its main
dimensions `height` and `width`. Note, that `height` and `width` are meant relative to the groove. They are not changed,
if a profile is rotated before passing it into another roll pass. These three must be provided as minimum to
the `Profile` constructor. More values can be given as keyword arguments and are saved automatically as attributes in
the instance. Which you may or must provide depends on the loaded plugins.

| Property        | Description                                                         |
|-----------------|---------------------------------------------------------------------|
| `cross_section` | Get the cross-section area of the profile.                          |
| `perimenter`    | Get the perimeter length of the profile.                            |
| `filling_ratio` | Get the ratio of profile width to the usable width of its `groove`. |

## Hooks

> To read about the basics of hooks and plugins, see [here](plugins.md).

The following hooks are defined on plain profiles per default:

```{eval-rst} 
.. automodule:: pyroll.core.profile.hookspecs
    :members:
```

## Derived classes

For the units types [`RollPass`](units.md#roll-passes) and [`Transport`](units.md#transports), specialized versions of
the `Profile` class are defined. They all maintain their own hooks, so it is possible to specify hooks on profiles only
for those places, were they are applicable.

| Class                 | Base class         | Description                                              |
|-----------------------|--------------------|----------------------------------------------------------|
| `RollPassProfile`     | `Profile`          | Common base class for in and out profile in roll passes. |
| `RollPassInProfile`   | `RollPassProfile`  | Class for incoming profiles in roll passes.              |
| `RollPassOutProfile`  | `RollPassProfile`  | Class for outgoing profiles in roll passes.              |
| `TransportProfile`    | `Profile`          | Common base class for in and out profile in transports.  |
| `TransportInProfile`  | `TransportProfile` | Class for incoming profiles in transports.               |
| `TransportOutProfile` | `TransportProfile` | Class for outgoing profiles in transports.               |

All hooks on those classes receive additionally to the profile instance also the instance of the roll pass or transport
they are belonging to.

So the signatures are:

    hook_name(profile: Profile, roll_pass: RollPass)
    hook_name(profile: Profile, transport: Transport)