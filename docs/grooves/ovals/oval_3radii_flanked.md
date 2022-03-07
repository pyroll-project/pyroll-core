# The `Oval3RadiiFlankedGroove` class

The `Oval3RadiiFlankedGroove` class represents an oval shaped groove consisting of three radii and a small straight
flank as shown in the figure.

![3 radii flanked oval groove geometry](oval_3radii_flanked.svg)

Mandatory measures of this groove are the three radii $`r_1`$, $`r_2`$ and $`r_3`$, as well as the depth $`d`$, the
usable width $`b_\mathrm{kn}`$ and the flank angle $`\alpha_1`$.

So the constructor has the following signature:

    Oval3RadiiFlankedGroove(r1, r2, r3, depth, usable_width, flank_angle)

The depth is $`d`$ typically $`\le \frac{b_\mathrm{kn}}{2}`$.

$`r_4`$ and $`b_d'`$ are considered to be zero.