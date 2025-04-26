"""
This file contains all classes to handle different algebraic structures and operations performed in them.
Abstract algebra shit it 2 words
"""

from abc import ABCMeta, abstractmethod
from typing import Iterable, override, Any
from math import ceil, floor

MAX_STR_ELEMENTS = 7  # defines how many elements can be shown via Structure.__str__


class AbstractStructure(metaclass=ABCMeta):
    """
    Generic representation of algebraic structures.

    """
    __elements__: Iterable  # set of all structure elements

    def elements_add(self, a, b):
        """
        Every group with addictive notation available must implement this method.
        When some structure element got __add__ call it should pass this call to this method with itself as the first argument.
        Thus, we're guaranteed first argument to be an instance of a current class.
        """
        NotImplemented

    def elements_mul(self, a, b):
        """
        Every group with multiplicative notation available must implement this method.
        When some structure element got __mul__ call it should pass this call to this method with itself as the first argument.
        Thus, we're guaranteed first argument to be an instance of a current class.
        """
        NotImplemented

    def element_inverse(self, a) -> StructureElement | None:
        """
        Every structure that supports inverting must override this method.
        It returns inverse or None if it doesn't exist.
        :param a:
        :return:
        """
        return None

    def __iter__(self):
        """Allows iterating over all elements"""
        return self.__elements__.__iter__()

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
        self.__structure__ = structure
        self.value = value

    def __add__(self, other):
        return self.structure.elements_add(self, other)

    def __mul__(self, other):
        return self.structure.elements_mul(self, other)

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
    @abstractmethod
    def inverse(self) -> StructureElement | None:
        """Returns inverse of the element in its structure or None"""
        return self.structure.element_inverse(self)


class Group(AbstractStructure, metaclass=ABCMeta):
    """
    Algebraic group - https://en.wikipedia.org/wiki/Algebraic_group
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

    def __init__(self, n):
        self.__elements__ = range(n)
        self.n = n

    def __call__(self, num: int) -> StructureElement:
        if not isinstance(num, int):
            raise TypeError
        return StructureElement(value=num % self.n, structure=self)

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
    @property
    def neutral(self):
        return StructureElement(value=0, structure=self)

    @override
    @property
    def name(self) -> str:
        return f"Z_{self.n}"

    @override
    def element_inverse(self, element: StructureElement) -> StructureElement:
        return self(self.n - element.value)

