from __future__ import annotations

from typing import Tuple

from abstractAlgebra.structures import *
from decimal import Decimal

import random

INFTY = Decimal('Infinity')
MAX_RANDOM_CURVE_ITERS = 16

def define_appropriate_curve(a: int, b: int) -> bool:
    """
    Returns true if x^3 + ax + b is non-singular (4a^3 + 27b^2 != 0)
    """
    return bool(4*a**3 + 27*b ** 2)

def random_elliptic_curve(p: int) -> EllipticCurve:
    """
    Returns a random elliptic curve over finite Fp field.
    :param p:
    :return:
    """
    assert p > 1, "p must be greater than 1"
    for _ in range(MAX_RANDOM_CURVE_ITERS):
        a = random.randint(0, p-1)
        b = random.randint(0, p-1)
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

class EllipticCurve(Field):
    """
    Elliptic curve over finite field Fp
    """

    def __init__(self, a: int, b: int, p: int):
        assert define_appropriate_curve(a, b), "4a^3 + 27b^2 must not be zero"
        self.a = a
        self.b = b
        self.p = p

    def __call__(self, *args, **kwargs) -> EllipticCurvePoint:
        """
        Returns an element of this structure based on the given value.
        It can be either single iterable of 2 integers or 2 integers itself as 2 arguments.
        """

        if len(args) == 1:
            x, y = args[0]
        elif len(args) == 2:
            x, y = args
        else:
            raise AttributeError(f"Expected 1 or 2 arguments, got {len(args)}")

        assert isinstance(x, int) or x == INFTY, f"x expected to be an integer or INFTY, got {type(x)} instead"
        assert isinstance(y, int) or y == INFTY, f"y expected to be an integer or INFTY, got {type(y)} instead"

        # TODO: check whether point lies on the curve

        return EllipticCurvePoint(x, y, structure=self)

    def __str__(self):
        return f"<{self.__class__.__name__}: x^3 + {self.a}x + {self.b} (mod {self.p})>"

    def __contains__(self, item):
        if isinstance(item, EllipticCurvePoint) and item.structure == self:
            return True
        if isinstance(item, Iterable):
            if len(item) == 2:
                x, y = tuple(item)
                if isinstance(x, int) and isinstance(y, int):
                    # TODO: finish
                    ...
        return False
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

