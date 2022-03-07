# The `ConstrictedBoxGroove` class

The `ConstrictedBoxGroove` class represents a [`BoxGroove`](box.md) but with an indent in the ground as shown in the
figure.

![constricted box groove geometry](constricted_box.svg)

Mandatory measures of the box groove are the two radii $`r_1`$ and $`r_2`$, as well as the depth $`d`$ and the indent
$`i`$. To constrain geometry fully, any two of the following must be given:

- usable width $`b_\mathrm{kn}`$
- ground width $`b_d`$
- flank angle $`\alpha_1`$

So the constructor has the following signature:

    ConstrictedBoxGroove(r1, r2, depth, indent, usable_width, ground_width, flank_angle)

The radii are typically small, the depth is $`d`$ typically $`\le \frac{b_\mathrm{kn}}{2}`$.

$`r_3`$ and $`r_4`$ are considered to be zero.