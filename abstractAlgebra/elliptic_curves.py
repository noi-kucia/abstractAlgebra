from __future__ import annotations

from typing import Tuple

from abstractAlgebra.structures import *
from decimal import Decimal

INFTY = Decimal('Infinity')

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
        assert 4*a**3 + 27*b ** 2, "4a^3 + 27b^2 must not be zero"
        self.a = a
        self.b = b
        self.p = p

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
        return f"<{self.__class__.__name__}: x^3 + {self.a}x + {self.b} (mod {self.p})>"

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

