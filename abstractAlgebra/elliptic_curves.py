from __future__ import annotations

from typing import Tuple

from abstractAlgebra.structures import *
from decimal import Decimal

import random

INFTY = Decimal('Infinity')
MAX_RANDOM_CURVE_ITERS = 64


def define_appropriate_curve(a: FieldElement, b: FieldElement) -> bool:
    """
    Returns true if x^3 + ax + b is non-singular (4a^3 + 27b^2 != 0)
    """
    return bool(4 * a ** 3 + 27 * b ** 2)


def random_elliptic_curve(p: int) -> EllipticCurve:
    """
    Returns a random elliptic curve over finite Fp field.
    :param p:
    :return:
    """
    assert p > 1, "p must be greater than 1"
    for _ in range(MAX_RANDOM_CURVE_ITERS):
        field = Fp(p)
        a = field.get_random_element()
        b = field.get_random_element()
        if define_appropriate_curve(a, b):
            return EllipticCurve(a, b, p)
    else:
        raise RuntimeError("Cannot generate random elliptic curve over finite Fp field. If you sure it exists,"
                           " try increasing the MAX_RANDOM_CURVE_ITERS parameter.")


class EllipticCurvePoint(FieldElement):
    """
    Represents a point in an Elliptic Curve.
    Its value is a tuple of 2 decimals that can be reached via x and y properties.
    """

    def __init__(self,
                 x: int = None,
                 y: int = None,
                 *,
                 value: Iterable[FieldElement | INFTY] = None,
                 structure: EllipticCurve):

        curve = structure
        field = curve.field
        if x is None or y is None:
            assert len(list(value)) == 2, "value must contain exactly 2 elements"
            x, y = value
        if isinstance(x, int):
            x = field(x)
        if isinstance(y, int):
            y = field(y)

        assert isinstance(x, FieldElement), "x expected to be a FieldElement instance"
        assert isinstance(y, FieldElement), "y expected to be a FieldElement instance"
        assert y.field == x.field, "both x and y must be from the same field"

        value = (x, y)
        structure = structure or x.field
        super().__init__(value=value, structure=structure)
        self.value: Tuple[FieldElement | INFTY, FieldElement | INFTY]

    def __str__(self):
        return f"<{self.__class__.__name__}: {self.value}>"

    @property
    def x(self) -> int:
        return self.value[0]

    @x.setter
    def x(self, value: int):
        self.value = (value, self.value[1])

    @property
    def y(self) -> int:
        return self.value[1]

    @y.setter
    def y(self, value: int):
        self.value = (self.value[0], value)

    @property
    def field(self) -> Fp:
        return self.curve.field

    @property
    def curve(self) -> EllipticCurve:
        """Alias for self.structure"""
        return self.structure


class EllipticCurve(Field):
    """
    Elliptic curve over finite field Fp
    """

    def __init__(self, a: int, b: int, p: int):
        assert define_appropriate_curve(a, b), "4a^3 + 27b^2 must not be zero"
        self.a = a
        self.b = b
        self.field = Fp(p)

    def __call__(self, *args, **kwargs) -> EllipticCurvePoint:
        """
        Returns an element of this structure based on the given value.
        It can be either single iterable of 2 objects or 2 objects itself as 2 arguments.
        Those objects must be either elements of equal to underlying field or something that can construct an Fp element
        """

        # unpacking x, y values
        if len(args) == 1:
            x, y = args[0]
        elif len(args) == 2:
            x, y = args
        else:
            raise AttributeError(f"Expected 1 or 2 arguments, got {len(args)}")

        # constructing new field elements when x or y isn't from the equal field
        if not isinstance(x, FieldElement) or x.structure != self.field:
            x = self.field(x)
        if not isinstance(y, FieldElement) or y.structure != self.field:
            y = self.field(y)

        # point must belong to the curve
        if not (x, y) in self:
            raise AttributeError(f"{(x, y)} does not define a point in {self}")

        return EllipticCurvePoint(x, y, structure=self)

    def __str__(self):
        return f"<{self.__class__.__name__}: x^3 + {self.a.value}x + {self.b.value} (mod {self.p})>"

    def __eq__(self, other):
        """
        Every other elliptic curve with the same a and v values and defined over equal field
        is considered to be equal
        """
        fields_equal = other.field == self.field
        params_equal = other.a == self.a and other.b == self.b
        return isinstance(other, EllipticCurve) and params_equal and fields_equal

    def polynom(self, x: FieldElement) -> FieldElement:
        x = self.field(x)
        return x ** 3 + self.a * x + self.b

    def get_random_point(self) -> EllipticCurvePoint:
        for _ in range(MAX_RANDOM_CURVE_ITERS):
            x = self.field.get_random_element()
            y_squared = self.polynom(x)
            if y_squared.is_quadratic_residue():
                return EllipticCurvePoint(x, y_squared.sqrt, structure=self)
        else:
            raise RuntimeError(f"Cannot generate random point of the {self}. If you sure it exists,"
                               " try increasing the MAX_RANDOM_CURVE_ITERS parameter.")

    def __contains__(self, item):

        if isinstance(item, EllipticCurvePoint) and item.structure == self:
            return True

        if isinstance(item, Iterable):
            if len(item) == 2:
                x, y = tuple(item)
                return self.polynom(x) == y
            else:
                raise AttributeError(f"Expected 2 values to be unpacked, got {len(item)}")

    @override
    def element_additive_inverse(self, element: EllipticCurvePoint) -> EllipticCurvePoint:
        element.y = element.y.ainverse
        return element

    @override
    def sqrt(self, element: EllipticCurvePoint) -> EllipticCurvePoint | None:
        raise NotImplementedError

    @property
    def aneutral(self) -> EllipticCurvePoint:
        """neutral element of addition"""
        self(INFTY, INFTY)

    @property
    def mneutral(self) -> EllipticCurvePoint:
        """neutral element of multiplication"""

    @property
    def p(self):
        return self.field.p

