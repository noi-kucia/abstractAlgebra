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

    def element_pow(self, power, modulo) -> StructureElement | None:
        """
        Every structure that supports powering must override this method.

        :param power:
        :param modulo:
        :return:
        """
        raise NotImplementedError(f"{self.__class__.__name__} does not implement power operation")

    def element_additive_inverse(self, a: StructureElement) -> StructureElement | None:
        """
        Every structure that supports additive inverting must override this method.
        It returns inverse or None if it doesn't exist.

        :param a:
        :return:
        """
        raise NotImplementedError(f"{self.__class__.__name__} does not implement additive inverse")

    def element_multiplicative_inverse(self, s: StructureElement) -> StructureElement | None:
        """
        Every structure that supports multiplicative inverting must override this method.
        It returns inverse or None if it doesn't exist.

        :param s:
        :return:
        """
        raise NotImplementedError(f"{self.__class__.__name__} does not implement multiplicative inverse")

    @abstractmethod
    def __call__(self, value: Any) -> StructureElement:
        """
        Returns an element of this structure based on the given value.
        Must be implemented by subclasses.

        :param value:
        :return:
        """
        raise NotImplementedError

    def __iter__(self):
        """Allows iterating over all elements"""
        for element in self.__elements__:
            yield self(value=element)

    def __str__(self):
        elements = list(self.__elements__)
        if len(elements) > MAX_STR_ELEMENTS:
            elements = elements[:ceil(MAX_STR_ELEMENTS / 2)] + ["..."] + elements[-MAX_STR_ELEMENTS // 2:]
        return f"<{type(self).__name__}: {elements}>"

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

    def __pow__(self, power, modulo=None):
        return self.structure.element_pow(power, modulo)

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
        return GroupElement(value=0, structure=self)

    @override
    @property
    def name(self) -> str:
        return f"Z_{self.n}"

