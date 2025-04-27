"""
This file contains all classes to handle different algebraic structures and operations performed in them.
Abstract algebra shit it 2 words
"""
from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Iterable, override, Any
from math import ceil, floor

MAX_STR_ELEMENTS = 7  # defines how many elements can be shown via Structure.__str__


class AbstractStructure(metaclass=ABCMeta):
    """
    Generic representation of algebraic structures.

    """
    __elements__: Iterable  # set of all structure elements

    def elements_add(self, a: StructureElement, b: Any) -> StructureElement:
        """
        Every group with addictive notation available must implement this method.
        When some structure element got __add__ call it should pass this call to this method with itself as the first argument.
        Thus, we're guaranteed first argument to be an instance of a current class.

        :param a:
        :param b:
        :return:
        """
        raise NotImplementedError(f"{self.__class__.__name__} does not implement addition")

    def elements_mul(self, a: StructureElement, b: Any) -> StructureElement:
        """
        Every structure with multiplicative notation available must implement this method.
        When some structure element got __mul__ call it should pass this call to this method with itself as the first argument.
        Thus, we're guaranteed first argument to be an instance of a current class.

        :param a:
        :param b:
        :return:
        """
        raise NotImplementedError(f"{self.__class__.__name__} does not implement multiplication")

    def elements_div(self, a: StructureElement, b: Any) -> StructureElement:
        """
        Every structure with multiplicative notation available must implement this method.
        When some structure element got __truediv__ call it should pass this call to this method with itself as the first argument.
        Thus, we're guaranteed first argument to be an instance of a current class.

        :param a:
        :param b:
        :return:
        """
        raise NotImplementedError(f"{self.__class__.__name__} does not implement division")

    def elements_floordiv(self, other: Any) -> StructureElement:
        """
        When some structure element got __floordiv_ call it should pass this call to this method with itself as the first argument.
        Thus, we're guaranteed first argument to be an instance of a current class.

        :param a:
        :param b:
        :return:
        """
        raise NotImplementedError(f"{self.__class__.__name__} does not implement floor division")

    def elements_sub(self, a: StructureElement, b: Any) -> StructureElement:
        """
        Subtraction by default works like an addition of inverse.
        Should be overridden by subclasses because of possible poor performance.

        :param a:
        :param b:
        :return:
        """
        if isinstance(b, StructureElement):
            return self.elements_add(a, b.inverse)
        raise NotImplementedError(f"{self.__class__.__name__} does not implement subtraction")

    def element_pow(self, base: StructureElement, power, modulo) -> StructureElement | None:
        """
        Every structure that supports powering must override this method.

        :param base: the element of the structure to be powered
        :param power:
        :param modulo:
        :return:
        """
        raise NotImplementedError(f"{self.__class__.__name__} does not implement power operation")

    def element_additive_inverse(self, element: StructureElement) -> StructureElement | None:
        """
        Every structure that supports additive inverting must override this method.
        It returns inverse or None if it doesn't exist.

        :param element:
        :return:
        """
        raise NotImplementedError(f"{self.__class__.__name__} does not implement additive inverse")

    def element_multiplicative_inverse(self, element: StructureElement) -> StructureElement | None:
        """
        Every structure that supports multiplicative inverting must override this method.
        It returns inverse or None if it doesn't exist.

        :param element:
        :return:
        """
        raise NotImplementedError(f"{self.__class__.__name__} does not implement multiplicative inverse")

    def elements_eq(self, element: StructureElement, other: Any) -> bool:
        if isinstance(other, StructureElement) and other.structure is element.structure:
            return element.value == other.value
        return element.value == other

    def elements_ge(self, element: StructureElement, other: Any) -> bool:
        if isinstance(other, StructureElement) and other.structure is element.structure:
            return element.value >= other.value
        return element.value >= other

    def elements_gt(self, element: StructureElement, other: Any) -> bool:
        if isinstance(other, StructureElement) and other.structure is element.structure:
            return element.value > other.value
        return element.value > other

    def elements_le(self, element: StructureElement, other: Any) -> bool:
        if isinstance(other, StructureElement) and other.structure is element.structure:
            return element.value <= other.value
        return element.value <= other

    def elements_lt(self, element: StructureElement, other: Any) -> bool:
        if isinstance(other, StructureElement) and other.structure is element.structure:
            return element.value < other.value
        return element.value < other

    @abstractmethod
    def __call__(self, value: Any) -> StructureElement:
        """
        Returns an element of this structure based on the given value.
        Must be implemented by subclasses.

        :param value:
        :return:
        """
        raise NotImplementedError

    def __iter__(self) -> Iterable[StructureElement]:
        """Allows iterating over all elements"""
        for element in self.__elements__:
            yield self(value=element)

    def __str__(self):
        elements = list(self.__elements__)
        if len(elements) > MAX_STR_ELEMENTS:
            elements = elements[:ceil(MAX_STR_ELEMENTS / 2)] + ["..."] + elements[-MAX_STR_ELEMENTS // 2:]
        return f"<{self.name}: {elements}>"

    @property
    def name(self) -> str:
        """Returns the display name of the structure"""
        return type(self).__name__


class StructureElement:
    """
    Element of a certain algebraic structure.
    """
    __structure__: AbstractStructure

    def __init__(self, *, value: Any, structure: AbstractStructure):
        self.__structure__: AbstractStructure = structure
        self.value = value

    def __add__(self, other):
        return self.structure.elements_add(self, other)

    def __sub__(self, other):
        return self.structure.elements_sub(self, other)

    def __mul__(self, other):
        return self.structure.elements_mul(self, other)

    def __truediv__(self, other):
        return self.structure.elements_div(self, other)

    def __floordiv__(self, other):
        return self.structure.elements_floordiv(self, other)

    def __pow__(self, power, modulo=None):
        return self.structure.element_pow(self, power, modulo)

    def __neg__(self):
        return self.ainverse

    def __eq__(self, other):
        return self.structure.elements_eq(self, other)

    def __ge__(self, other):
        return self.structure.elements_ge(self, other)

    def __gt__(self, other):
        return self.structure.elements_gt(self, other)

    def __le__(self, other):
        return self.structure.elements_le(self, other)

    def __lt__(self, other):
        return self.structure.elements_lt(self, other)

    def __str__(self):
        return f"<{self.structure.name}: {self.value}>"

    @property
    def structure(self):
        return self.__structure__

    @property
    def group(self):
        """Alias for self.structure"""
        return self.structure

    @property
    def ainverse(self) -> StructureElement | None:
        """Returns inverse of the element in additive notation"""
        return self.structure.element_additive_inverse(self)

    @property
    def minverse(self) -> StructureElement | None:
        """Returns inverse of the element in multiplicative notation"""
        return self.structure.element_multiplicative_inverse(self)


class GroupElement(StructureElement):

    @property
    def inverse(self) -> StructureElement:
        """Alias for additive inverse since on groups there's defined only addition"""
        return self.ainverse


class Group(AbstractStructure, metaclass=ABCMeta):
    """
    Algebraic group - https://en.wikipedia.org/wiki/Algebraic_group
    Assumed that groups are defined with addition.
    """

    @property
    @abstractmethod
    def neutral(self) -> StructureElement:
        """Returns neutral element of the algebraic group"""

    @property
    def e(self) -> StructureElement:
        """A shortcut for neutral element"""
        return self.neutral



class Zn(Group):
    """
    A cyclic group of integers modulo n with additive notation.
    """

    def __init__(self, n: int):
        assert isinstance(n, int) and n > 0, "n must be non-negative integer"

        self.__elements__ = range(n)
        self.n = n

    def __call__(self, value: int) -> GroupElement:
        assert isinstance(value, int), "num must be integer"
        return GroupElement(value=value % self.n, structure=self)

    @override
    def __iter__(self) -> Iterable[GroupElement]:
        return super().__iter__()

    @override
    def elements_add(self, a, b):

        # adding an element of certain structure
        if isinstance(b, StructureElement):
            if b.structure is self:  # cannot add elements from different structures
                return self((a.value + b.value) % self.n)
            raise AttributeError(f"cannot add elements from different groups: {a.structure} and {b.structure}")

        # adding an integer
        if isinstance(b, int):
            return self((a.value + b) % self.n)

    @override
    def elements_sub(self, a: GroupElement, b: Any) -> GroupElement:

        # subtracting an element of certain structure
        if isinstance(b, StructureElement):
            if b.structure is self:
                return self((a.value - b.value) % self.n)
            raise AttributeError(f"cannot subtract elements from different groups: {a.structure} and {b.structure}")

        # subtracting an integer
        if isinstance(b, int):
            return self((a.value - b) % self.n)

    @override
    def element_additive_inverse(self, element: GroupElement) -> GroupElement:
        return self(self.n - element.value)

    @override
    @property
    def neutral(self):
        return self(0)

    @override
    @property
    def name(self) -> str:
        return f"Z_{self.n}"


class FieldElement(GroupElement):

    @property
    def inverse(self) -> FieldElement:
        """Alias for multiplicative inverse since"""
        return self.minverse


class Field(AbstractStructure, metaclass=ABCMeta):
    """
    Algebraic field - https://en.wikipedia.org/wiki/Field_(mathematics)
    Supports additive and multiplicative notations.
    """

    @property
    @abstractmethod
    def aneutral(self) -> FieldElement:
        """neutral element of addition"""

    @property
    @abstractmethod
    def mneutral(self) -> FieldElement:
        """neutral element of multiplication"""


class Fp(Zn, Field):
    """
    Field with addition and multiplication available of Z/pZ type where p is a prime number.
    """

    def __init__(self, p: int):
        """
        :param p: assumed to be a prime number, otherwise will lead to unpredictable behavior
        """
        assert isinstance(p, int) and p > 1, "p must be a positive integer"
        super().__init__(p)

    def __call__(self, value: int) -> FieldElement:
        assert isinstance(value, int), "num must be integer"
        return FieldElement(value=value % self.p, structure=self)

    @override
    def elements_mul(self, a: StructureElement, b: Any) -> FieldElement:

        # multiplication with the element of certain structure
        if isinstance(b, StructureElement):
            if b.structure is self:
                return self((a.value * b.value) % self.p)
            raise AttributeError(f"cannot multiply elements from different groups: {a.structure} and {b.structure}")

        # with integer
        if isinstance(b, int):
            return self((a.value * b) % self.p)

    @override
    def element_pow(self, base: FieldElement, power, modulo) -> FieldElement:

        # extracting the power as integer into b variable
        if isinstance(power, StructureElement):
            if power.structure is not self:
                raise AttributeError(f"cannot use element of another group as power: {power.structure}")
            b = power.value
        elif isinstance(power, int):
            b = power
        else:
            raise NotImplementedError(f"Unknown type of power: {type(power)}")

        assert b >= 0, "power must be non-negative integer"

        # fast powering a^b modulo p
        a = base.value
        p = self.p
        ans = self.mneutral.value
        while b:
            if b % 2:
                ans = (ans * a) % p
            a = a ** 2 % p
            b //= 2

        return self(ans)

    @override
    def elements_div(self, a: FieldElement, b: Any) -> FieldElement:

        # dividing by a structure element
        if isinstance(b, StructureElement):
            if b.structure is self:
                return self(a.value * b.minverse.value)
            raise AttributeError(f"cannot divide element of {a.structure} by element of {b.structure}")

        # dividing by integer
        if isinstance(b, int):
            return self(a.value * self(b).minverse.value)

    @override
    def element_multiplicative_inverse(self, element: FieldElement) -> FieldElement | None:
        assert element >= 0, "element must be a positive integer"

        # zero doesn't have inverse
        if element == self.aneutral:
            return None

        a, b = element.value, self.p
        inv, inv_prev = 0, 1
        while b != 0:
            q = a // b
            a, b = b, a - q * b
            inv, inv_prev = inv_prev - q * inv, inv

        return self(inv_prev)

    @property
    def aneutral(self) -> FieldElement:
        return self(0)

    @property
    def mneutral(self) -> FieldElement:
        return self(1)

    @override
    def __iter__(self) -> Iterable[FieldElement]:
        return super().__iter__()

    @property
    def p(self) -> int:
        """alias for self.n"""
        return self.n

    @override
    @property
    def name(self) -> str:
        return f"F_{self.n}"

    @override
    @property
    def neutral(self) -> FieldElement:
        raise NotImplementedError("You must use either aneutral or mneutral method when dealing with fields")
