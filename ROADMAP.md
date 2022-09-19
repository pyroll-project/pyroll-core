For discussion regarding the roadmap see [#13](../../issues/13).

# PyRolL Core

## Version 1.1 "Spacial Resolution"

- implement concept of strip element/disk element to enable spacial resolution in rolling direction
- enable possibilities for:
  - one-dimensional Karman-type tension and force calculation
  - local spreading and roll contact
  - one-dimensional thermal modelling

## Version 2.0 "Asymmetric Rolling"

- implement data structures for asymmetric rolling
  - distinct working rolls
  - drop symmetry assumptions in current code

# Plugin Packages

## Rounded Sides

- approximate consideration of free forming on sides of the profile
- circular arc geometry
- mainly by implementation of `Profile.cross_section`

## Microstructure

- microstructure evolution by JMAK-approaches
- mean microstructure composition
- recrystallization, relaxation, phase transformation

## Interstand Tension

- approximate consideration of interstand tensions on filling and roll force

## `pyroll-integral-thermal`

- introduce surface temperature estimation to existing plugin