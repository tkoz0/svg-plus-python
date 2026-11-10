# SVGPP2

This is a library for creating 2D drawings for math diagrams, geometry problems,
visualizations, etc. It is designed to balance ease of use with high flexibility
and ensure a high standard of numerical stability and robustness.

Goals/priorities:
- Mathematical correctness
- Numerical stability and robustness
- Customizable and correct SVG output
- Ease of use without losing features

Things that are not goals/priorities:
- Not planning to support every SVG feature yet
- Not a general purpose vector graphics library

## Software

- Target compatibility with Python 3.14.
  - Latest stable features are fine to use
  - If a feature depends on recent Python or standard library changes,
    mention it and include appropriate comments in the code

## Architecture

The project is a single module with the following files.

`helpers.py`
- General tools for reuse. Includes number formatting and sincos.

`vec.py`
- Contains a `Vec2` class used for coordinates and directions.
- `Vec2` is immutable to prevent surprise changes since coordinates can be
  reused across many diagram components.

`affine.py`
- Contains `Affine2` which represents a 2D affine transformation with a linear
  basis (`xAxis` and `yAxis`) and a translation offset (`origin`).
- Immutable for the same reason as `Vec2`.

`transform.py`
- Contains a `TransformBase` base class and 6 derived classes for the 6 types of
  SVG transforms.
  - `TransformTranslate`
  - `TransformRotate`
  - `TransformScale`
  - `TransformSkewX`
  - `TransformSkewY`
  - `TransformMatrix`
- Handles specific cases of affine transformations and serialization for SVG.
- Supports other functionality like conversion to `Affine2`, inversion, and
  construction from `Affine2` if it matches a transformation type within a
  tolerance.
- Composition operations maintain the specific transformation type if possible,
  and fall back to `TransformMatrix` otherwise.
- Immutable for the same reason as `Vec2`.

## Conventions

### Design

For low level types (like `Vec2` and `Affine2`)
- Enforce immutability with `__slots__` and by raising `AttributeError` in
  `__setattr__` and `__delattr__`. Constructors bypass it with
  `object.__setattr__(self,'attrName',value)`. Ensure base classes have a
  `__slots__` to maintain memory efficiency benefits.
- For immutable types, `__copy__` and `__deepcopy__` return `self`.
- To support `pickle` for immutable objects, `__reduce__` returns
  `(type(self),tupleOfSlotValues)`. For many classes, the slots order matches
  the constructor order, but if that differs, make sure `__reduce__` works.
- Do not allow silent errors. Prefer exceptions instead of error values.
- Disallow `bool` for arguments where a number (`int` or `float`) is expected.

For higher level types (the SVG and geometry layers)
- Allow mutability

Priorities:
- Correctness, numerical stability, robustness to scaling
- Clear and predictable API behavior
- Simplicity and readability
- Performance

### Naming

- Use `PascalCase` for classes.
- Use `camelCase` for public functions, attributes, module names, and local
  variables. This is deliberate personal preference and differs from PEP 8.
- Use `CAPS_SNAKE_CASE` for public constants and prefix with `_` if private.
- Prefix private module helpers or member functions with `_`, for example
  `_checkValue`.

### Code Style

- Use single quotes for strings.
- Prefer f-strings for formatting.
- Use `!r` in f-strings for `__repr__`.
- Include type hints for function arguments and return types.
- Comment non trivial things including math derivations.
- Keep brief related notes in comments, including justifications for choices or
  alternatives that were not used.

### Exception Usage

This table should provide some guidelines to choose proper exception types.
Exception messages should include invalid value for small types.

| Condition | Exception |
|---|---|
| Non finite scalar argument | `ValueError` |
| Calculations produce a non finite result | `OverflowError` |
| Normalizing zero vector or zero division | `ZeroDivisionError` |
| Incorrect type for an argument | `TypeError` |
| Passing `bool` where `int` or `float` is expected | `TypeError` |
| Correct type but value is invalid | `ValueError` |
| Conversion to bool when not allowed | `TypeError` |

### Type Hints

- Document acceptable types for function arguments and return types.
- Include type hints for arguments and return types except for functions that
  do not return a value.

### Documentation

- Include a docstring for every public function, even if short.
- Make documentation concise, but describe gotchas or other information callers
  should know about.
- Document exceptions raised.
- Document tolerances, scale-free coordinate handling, etc, if relevant.

## SVG Notes

- There are 6 types of transformations
  - `translate(x y)` is a translation with offset `(x,y)`
  - `rotate(a)` is a rotation around the origin by `a` degrees
  - `rotate(a x y)` is a rotation around the point `(x,y)` by `a` degrees
  - `scale(s)` is a uniform scale by factor `s` on both axes
  - `scale(s t)` is a scale by factor `s` on the `x` axis and factor `t` on the
    `y` axis
  - `skewX(a)` is a skew along the x axis by `a` degrees
  - `skewY(a)` is a skew along the y axis by `a` degrees
  - `matrix(a b c d e f)` is the following mapping on a point `(x,y)`:
    - `x' = a*x + c*y + e`
    - `y' = b*x + d*y + f`
- Multiple transforms are applied in right to left order, which is the same as
  the math order and matrix multiplication.
  - For example, in `scale(5) rotate(10)`, the rotation is applied to a point
    before the scale.
  - This matches the composition order used in the library. For example,
    `TransformScale(5).compose(TransformRotate(10))` would compose two
    transformations into a single equivalent transformation, in this case the
    same as the SVG value `scale(5) rotate(5)`.
- SVG uses y-down coordinates, where positive angles rotate clockwise.
  The geometry layer uses y-up coordinates by default, where positive angles
  rotate counterclockwise.
- SVG transformations involving angles use degrees, which matches the design
  choice for derived classes of `TransformBase`.
- The helper function `formatNumber` is used for converting numbers to be
  written in SVG output.

## Numerical Stability and Robustness

- The library should work well for coordinate scales from `10^-100` to `10^100`.
  Due to the multiplication in dot products and similar, we should even be able
  to have `10^-150` to `10^150` work, but consider these to be borderline
  pathological. Try to keep the code working in some extreme cases if possible.
  Don't bother increasing complexity in order to support something like
  normalizing vectors or computing dot products at `1e308` coordinates.
  - Don't worry about documenting every pathological case. For example,
    `Vec2.dot` can overflow with very large coordinates, but we put that in the
    category of unsupported pathological cases.
- Use exceptions to prevent constructing objects with inf/nan as well as when
  they show up from calculations. SVG does not allow inf/nan and appearance of
  these values indicates problems.
- Use `math.hypot` for magnitude calculations.
- Use `math.fma` when it helps with numerical stability.
- Direction comparison normalizes before comparing to be scale-free.
- When a formula can involve destructive cancellation, use an alternative form
  if possible, such as for trigonometric quantities.
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
  - For example, `tol` is used when comparing normalized directions to check if
    they are the same.
  - `tol*scale` is used for checking if a calculation results in a point close
    enough to the origin to assume it should be the origin.

## Pitfalls

- `Vec2` construction from numbers requires both coordinates. For example,
  `Vec2(1.0,0.0)` or `Vec2(0.0,1.0)`. `Vec2()` is the zero vector.
- `Affine2` construction can take 3 vectors, each having defaults, or a 6-tuple.
  `Affine2((1,2),(3,4),(5,6))` and `Affine2((1,2,3,4,5,6))` are equivalent. The
  3 defaults for the vectors default to the identity.
- The transformation classes use angles in degrees to follow the SVG standard.
- SVG uses y-down coordinates with clockwise positive rotations. The geometry
  layer uses y-up by default with counterclockwise positive rotation. Ensure
  these are handled correctly with a transformation if necessary.
- `bool` is a subclass of int in Python and should be explicitly rejected where
  numbers are expected.
- Use the `formatNumber` helper or an accepted number formatter as a parameter,
  possibly from the `numberFormatter` helper. Do not use `str(number)`.

## Testing

- Verify immutability. `__setattr__` and `__delattr__` should raise for
  immutable types. Copy and pickle operations should work.
- Arithmetic code should handle inf and nan with exceptions.
- Test scale invariance. Common number scales like `10` or `100` should work,
  but also test coordinates at scales like `10^-100` and `10^100` as well.
- Round trip conversions should work, like composing transformations with their
  inverse, or converting to another type and back.
- Edge cases, such as zero vectors, zero angles, multiples of 90 degrees,
  negative zero, inf/nan, near parallel/orthogonal vectors, near singular
  matrices, near degenerate transformations, etc.
- Public functions should reject `bool` where `int` or `float` is expected.

## Policies

Before making changes:
- Keep immutable types immutable
- Check for helper functions to keep code simpler
- Do not weaken validation or type safety to make tests pass
- Ensure type hints and docstrings are included

Things to avoid:
- Do not modify `Vec2`, `Affine2`, or transforms. If there seems to be a good
  reason to, check for confirmation
- Do not allow inf/nan in SVG/geometry objects or SVG output
- Do not accept `bool` where numbers are expected
- Do not use `str(number)` for SVG output
- Do not use absolute tolerances for coordinate comparisons without a scale
