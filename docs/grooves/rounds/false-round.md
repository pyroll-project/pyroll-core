# The `FalseRoundGroove` class

The `FalseRoundGroove` class represents a groove with a roughly circular cross-section, which shows a small straight flank, as shown in the figure.

![false round groove geometry](false_round.svg)

It is defined by two radii $`r_1`$ and $`r_2`$, the depth $`d`$ and the flank angle $`\alpha_1`$ , so the constructor has the following signature:

    FalseRoundGroove(r1, r2, depth, flank_angle)

The geometric constraints are $`r_1 << r_2`$, $`d < r_2`$ and $`\alpha_1 < 90°`$ .

$`r_3`$ and $`r_4`$ are considered to be zero, as well as $`b_d`$ and $`b_d'`$.

The usable width can be calculated as:

```math
    b_\mathrm{kn} = 2 \frac{d + \frac{r_2}{\cos \alpha_1} - r_2}{\tan \alpha_1}
```

