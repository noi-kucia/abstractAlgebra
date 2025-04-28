from __future__ import annotations

from typing import Tuple

from abstractAlgebra.structures import *
from decimal import Decimal

import random

INFTY = Decimal('Infinity')
MAX_RANDOM_CURVE_ITERS = 16

def define_appropriate_curve(a: FieldElement, b: FieldElement) -> bool:
    """
    Returns true if x^3 + ax + b is non-singular (4a^3 + 27b^2 != 0)
    """
    return bool(4*a**3 + 27*b ** 2)

def random_elliptic_curve(p: int) -> EllipticCurve:
    """
    Returns random elliptic curve over finite Fp field.
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
                 x: int | INFTY,
                 y: int | INFTY,
                 *,
                 value: Iterable[int | INFTY] = None,
                 structure: AbstractStructure):
        value = value or (x, y)
        super().__init__(value=value, structure=structure)
        self.value: Tuple[int | INFTY, int | INFTY]

    @property
    def x(self) -> int:
        return self.value[0]

    @x.setter
    def x(self, value: int):
        self.value[0] = value

    @property
    def y(self) -> int:
        return self.value[1]

    @y.setter
    def y(self, value: int):
        self.value[1] = value

    @property
    def curve(self) -> EllipticCurve:
        """Alias for self.structure"""
        return self.structure

class EllipticCurve(Field):
    """
    Elliptic curve over finite field Fp
    """

    def __init__(self, a: int | FieldElement, b: int | FieldElement, p: int = None):
        """
        Can be initialized either with 3 integers: a,b and p
        or with 2 Field elements of the same field.
        In the second case, the elements' field will be used.
        """

        if all((isinstance(arg, int) for arg in (a, b, p))):
            self.field: Fp = Fp(p)
            self.a: FieldElement = self.field(a)
            self.b: FieldElement = self.field(b)
        elif isinstance(a, FieldElement) and isinstance(b, FieldElement) and a.field is b.field:
            self.field = a.field
            self.a: FieldElement = a
            self.b: FieldElement = b
        else:
            raise AttributeError(f"Expected 3 ints or 2 FieldElements, got: {a, b, p}")

        assert define_appropriate_curve(a, b), "4a^3 + 27b^2 must not be zero"
        self.field: Fp = Fp(p)
        self.a: FieldElement = self.field(a)
        self.b: FieldElement = self.field(b)

    def __call__(self, *args, **kwargs) -> EllipticCurvePoint:
        """
        Returns an element of this structure based on the given value.
        It can be either single iterable of 2 integers or 2 integers itself as 2 arguments.
        """

        if len(args) == 2:
            x, y = args
            assert isinstance(x, int) or x == INFTY, f"x expected to be an integer or INFTY, got {type(x)} instead"
            assert isinstance(y, int) or y == INFTY, f"y expected to be an integer or INFTY, got {type(y)} instead"

    def __str__(self):
        return f"<{self.__class__.__name__}: x^3 + {self.a.value}x + {self.b.value} (mod {self.p})>"

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

