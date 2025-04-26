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

    def __iter__(self):
        """Allows iterating over all elements"""
        return self.__elements__.__iter__()

    def __str__(self):
        elements = list(self.__elements__)
        if len(elements) > MAX_STR_ELEMENTS:
            elements = elements[:ceil(MAX_STR_ELEMENTS / 2)] + ["..."] + elements[-MAX_STR_ELEMENTS // 2:]
        return f"<{type(self).__name__}: {elements}>"


class StructureElement:
    """
    Element of a certain algebraic structure.
    """
    __structure__: AbstractStructure

    def __init__(self, *, value: Any, group: AbstractStructure):
        self.__structure__ = group
        self.value = value

    def __add__(self, other):
        return self.structure.elements_add(self, other)

    def __mul__(self, other):
        return self.structure.elements_mul(self, other)

    def __str__(self):
        return str(self.value)

    @property
    def structure(self):
        return self.__structure__

    @property
    def group(self):
        """Alias for self.structure"""
        return self.structure


class Group(AbstractStructure, metaclass=ABCMeta):
    """
    Algebraic group - https://en.wikipedia.org/wiki/Algebraic_group
    """

    @property
    @abstractmethod
    def neutral(self):
        """Returns neutral element of the algebraic group"""

    @property
    def e(self):
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
        return StructureElement(value=num % self.n, group=self)

    @override
    def elements_add(self, a, b):
        return self((a.value + b.value) % self.n)

    def neutral(self):
        return 0
