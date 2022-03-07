# The `Oval3RadiiGroove` class

The `Oval3RadiiGroove` class represents an oval shaped groove consisting of three radii as shown in the figure.

![3 radii oval groove geometry](oval_3radii.svg)

Mandatory measures of this groove are the three radii $`r_1`$, $`r_2`$ and $`r_3`$, as well as the depth $`d`$ and the
usable width $`b_\mathrm{kn}`$.

So the constructor has the following signature:

    Oval3RadiiGroove(r1, r2, r3, depth, usable_width)

The depth is $`d`$ typically $`\le \frac{b_\mathrm{kn}}{2}`$.

$`r_4`$ and $`b_d'`$ are considered to be zero.