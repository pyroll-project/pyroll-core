# The `FlatOvalGroove` class

The `FlatOvalGroove` class represents an oval shaped groove consisting of two radii and an even ground as shown in the
figure.

![flat oval groove geometry](flat_oval.svg)

Mandatory measures of this groove are the two radii $`r_1`$ and $`r_2`$, as well as the depth $`d`$ and the usable width $`b_\mathrm{kn}`$.

So the constructor has the following signature:

    FlatOvalGroove(r1, r2, depth, usable_width)

The depth is $`d`$  typically $`\le \frac{b_\mathrm{kn}}{2}`$.

$`r_3`$ and $`r_4`$ are considered to be zero.