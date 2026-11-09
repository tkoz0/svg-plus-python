# SVGPP2

This is a library for creating 2D drawings for math diagrams, geometry problems,
visualizations, etc. It is designed to balance ease of use with high flexibility
and ensure a high standard of numerical stability and robustness.

## Software

Feel free to use most recent Python 3.14 features. If using something very
recent, inform about the possibility that things may not work on older Python
versions. This project will likely accept anything for latest stable Python.

## Architecture

`helpers.py`
- General tools for reuse. Includes number formatting and sincos.

`vec.py`
- Contains a `Vec2` class used for coordinates and math calculations.
- `Vec2` is immutable to prevent surprise changes since coordinates can be
  reused across many diagram components.

`affine.py`
- Contains `Affine2` which represents a 2D affine transformation with a linear
  basis (`xAxis` and `yAxis`) and a translation offset (`origin`).
- Immutable for the same reason as `Vec2`.

`transform.py`
- Contains a `TransformBase` base class and 6 derived classes for the 6 types of
  SVG transforms.
- Handles specific cases of affine transformations and serialization for SVG.
- Supports other functionality like conversion to `Affine2`, inversion, and
  construction from `Affine2` if it matches a transformation type within a
  tolerance.
- Composition operations maintain the specific transformation type if possible,
  and fall back to `TransformMatrix` otherwise.
- Immutable for the same reason as `Vec2`.

## Conventions

- Enforce immutability with `__slots__` and by raising `AttributeError` in
  `__setattr__` and `__delattr__`. Constructors bypass it with
  `object.__setattr__(self,'attrName',value)`.
- For immutable types, `__copy__` and `__deepcopy__` return `self`.
- To support `pickle` for immutable objects, `__reduce__` returns
  `(type(self),tupleOfSlotValues)`. For many classes, the slots order matches
  the constructor order, but if that differs, make sure `__reduce__` works.
- Do not allow silent errors. Prefer exceptions instead of error values.
- Disallow `bool` for arguments where a number (`int` or `float`) is expected.

### Naming

- Use `PascalCase` for classes.
- Use `camelCase` for functions. This is deliberate personal preference and
  differs from PEP 8.
- Use `CAPS_SNAKE_CASE` for constants.
- Prefix private module helpers with `_`, for example `_checkValue`.

### Code Style

- Use single quotes for strings.
- Prefer f-strings for formatting.
- Use `!r` in f-strings for `__repr__`.
- Comment non trivial things including math derivations.
- Keep brief related notes in comments, including justifications for choices or
  alternatives that were not used.

### Exception Usage

This table should provide some guidelines to choose exception types that make
sense.

| Condition | Exception |
|---|---|
| Non finite scalar argument | `ValueError` |
| Calculations produce a non finite result | `OverflowError` |
| Normalizing zero vector or zero division | `ZeroDivisionError` |
| Incorrect type for an argument | `TypeError` |
| Correct type but value is invalid | `ValueError` |
| Conversion to bool when not allowed | `TypeError` |

### Documentation

- Include a docstring for every public function, even if short.
- Make documentation concise, but describe gotchas or other information callers
  should know about.
- Document exceptions raised.
- Document tolerances, scale-free coordinate handling, etc, if relevant.

## SVG Notes

- The transform `matrix(a b c d e f)` describes the following mapping on a point
  `(x,y)`
  - `x' = a*x + c*y + e`
  - `y' = b*x + d*y + f`
- Multiple transforms are applied in right to left order, which is the same as
  the math order and matrix multiplication.
  - For example, in `scale(5) rotate(10)`, the rotation is before translation.
  - This matches the composition order used in the library. For example,
    `TransformScale(5).compose(TransformRotate(10))` would compose those two
    into a single equivalent transformation.
- SVG uses y-down coordinates. The geometry layer uses y-up by default.
- The helper function `formatNumber` is used for converting numbers to be
  written in SVG output.

## Numerical Stability and Robustness

- Try to ensure coordinate scales from `10^-100` to `10^100` should
  work well. Due to the multiplication in dot products and similar, we should
  even be able to have `10^-150` to `10^150` work, but consider these to be
  borderline pathological. Try to keep the code working in some extreme cases
  if possible. Don't bother increasing complexity in order to support something
  like normalizing vectors or computing dot products at `1e308` coordinates.
  - Don't worry about documenting every pathological case. For example,
    `Vec2.dot` can overflow with very large coordinates, but we put that in the
    category of unsupported pathological cases.
- Use exceptions to prevent constructing objects with inf/nan as well as when
  they show up from calculations. SVG does not allow inf/nan and appearance of
  these values indicates problems.
- Use `math.hypot` for magnitude calculations.
- Direction comparison normalizes before comparing to be scale-free.
- When a formula can involve destructive cancellation, use an alternative form.
  - For example, $$1-\cos(\theta)={\sin^2(\theta)\over(1+\cos(\theta))}$$ when
    $$\theta\approx0$$.
- Scale-free design means callers are responsible for knowing the coordinate
  scale they are working with. This is important to determine if a calculation
  results in a zero vector, since "close enough" to zero varies with scaling.
- The default tolerance of `1e-9` matches the default of `math.isclose`. This
  was chosen to be significantly above the floating point noise and far below
  anything that would be visually noticeable in practice.
- For functions that take a tolerance and scale (`tol` and `scale`), use `tol`
  for dimensionless quantities like comparing normalized vectors, and use
  `tol*scale` for coordinate space quantities like the origin.

## Pitfalls

- `Vec2` construction from numbers requires both coordinates. For example,
  `Vec2(1.0,0.0)` or `Vec2(0.0,1.0)`. `Vec2()` is the zero vector.
- `Affine2` construction can take 3 vectors, each having defaults, or a 6-tuple.
  `Affine2((1,2),(3,4),(5,6))` and `Affine2((1,2,3,4,5,6))` are equivalent. The
  3 defaults for the vectors default to the identity.
- The transformation classes use angles in degrees to follow the SVG standard.

## Testing

- Verify immutability. `__setattr__` and `__delattr__` should raise for
  immutable types. Copy and pickle operations should work.
- Arithmetic code should handle inf and nan with exceptions.
- Test scale invariance. Common number scales like `10` or `100` should work,
  but test coordinates at scales like `10^-100` and `10^100` as well.
- Round trip conversions should work, like composing transformations with their
  inverse, or converting to another type and back.
- Edge cases, such as zero vectors, zero angles, multiples of 90 degrees,
  negative zero, inf/nan, etc.
