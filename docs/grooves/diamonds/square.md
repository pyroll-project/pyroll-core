# The `SquareGroove` class

The `SquareGroove` class represents a square shaped groove as shown in the figure.

![square groove geometry](square.svg)

Mandatory measures of this groove are the two radii $`r_1`$ and $`r_2`$. To constrain geometry fully, any two of the
following must be given:

- usable width $`b_\mathrm{kn}`$
- tip depth $`d_\mathrm{t}`$
- tip angle $`\delta`$

So the constructor has the following signature:

    SquareGroove(r1, r2, usable_width, tip_depth, tip_angle)

The radii are typically small, the depth is $`d_\mathrm{t}`$ typically $`\approx \frac{b_\mathrm{kn}}{2}`$. The tip
angle $`\delta`$ is typically a one or two degree larger than 90° for wear reasons.

$`r_3`$ and $`r_4`$ are considered to be zero, as well as $`b_d`$ and $`b_d'`$.

The tip depth $`d_\mathrm{t}`$ was chosen in favor of the real depth $`d`$, because it does not change, when the radii are modified.
So the overall geometry remains the same if one modifies only the radii.
The tip depth can be considered as the diagonal of the square with sharp corners.

The constructor will raise a warning, if the tip angle significantly deviates from 90°, consider to use
a [`DiamondGroove`](diamond.md) instead.