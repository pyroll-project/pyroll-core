# The `CircularOvalGroove` class

The `CircularOvalGroove` class represents an oval shaped groove consisting of two radii as shown in the figure.

![circular oval groove geometry](circular_oval.svg)

It is defined by two radii $`r_1`$ and $`r_2`$ and the depth $`d`$, so the constructor has the following signature:

    CircularOvalGroove(r1, r2, depth)

The geometric constraints are $`r_1 << r_2`$ and $`d << r_2`$.

$`r_3`$ and $`r_4`$ are considered to be zero, as well as $`b_d`$ and $`b_d'`$.

The topology of this groove is similar to the [`RoundGroove`](../rounds/round.md), with the main difference, that the
center of $`r_2`$ is not placed in the center of the groove.
For this reason $`d`$ is typically much smaller than $`r_2`$.

