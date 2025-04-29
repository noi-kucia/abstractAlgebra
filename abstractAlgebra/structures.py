"""
This file contains all classes to handle different algebraic structures and operations performed in them.
Abstract algebra shit it 2 words
"""
from __future__ import annotations

import random
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
        """
        raise NotImplementedError(f"{self.__class__.__name__} does not implement addition")

    def elements_mul(self, a: StructureElement, b: Any) -> StructureElement:
        """
        Every structure with multiplicative notation available must implement this method.
        When some structure element got __mul__ call it should pass this call to this method with itself as the first argument.
        Thus, we're guaranteed first argument to be an instance of a current class.
        """
        raise NotImplementedError(f"{self.__class__.__name__} does not implement multiplication")

    def elements_div(self, element: StructureElement, b: Any) -> StructureElement:
        """
        Every structure with multiplicative notation available must implement this method.
        When some structure element got __truediv__ call it should pass this call to this method with itself as the first argument.
        Thus, we're guaranteed first argument to be an instance of a current class.
        """
        raise NotImplementedError(f"{self.__class__.__name__} does not implement division")

    def elements_floordiv(self, element: StructureElement, other: Any) -> StructureElement:
        """
        When some structure element got __floordiv_ call it should pass this call to this method with itself as the first argument.
        Thus, we're guaranteed first argument to be an instance of a current class.
        """
        raise NotImplementedError(f"{self.__class__.__name__} does not implement floor division")

    def elements_mod(self, element: StructureElement, other: Any) -> StructureElement:
        """
        When some structure element got __mod_ call it should pass this call to this method with itself as the first argument.
        Thus, we're guaranteed first argument to be an instance of a current class.
        """
        raise NotImplementedError(f"{self.__class__.__name__} does not implement modulation")

    def elements_sub(self, element: StructureElement, b: Any) -> StructureElement:
        """
        Subtraction by default works like an addition of inverse.
        Should be overridden by subclasses because of possible poor performance.
        """
        if isinstance(b, StructureElement):
            return self.elements_add(a, b.inverse)
        raise NotImplementedError(f"{self.__class__.__name__} does not implement subtraction")

    def element_pow(self, element: StructureElement, power, modulo) -> StructureElement | None:
        """
        Every structure that supports powering must override this method.
        """
        raise NotImplementedError(f"{self.__class__.__name__} does not implement power operation")

    def element_additive_inverse(self, element: StructureElement) -> StructureElement | None:
        """
        Every structure that supports additive inverting must override this method.
        It returns inverse or None if it doesn't exist.
        """
        raise NotImplementedError(f"{self.__class__.__name__} does not implement additive inverse")

    def element_multiplicative_inverse(self, element: StructureElement) -> StructureElement | None:
        """
        Every structure that supports multiplicative inverting must override this method.
        It returns inverse or None if it doesn't exist.
        """
        raise NotImplementedError(f"{self.__class__.__name__} does not implement multiplicative inverse")

    def elements_eq(self, element: StructureElement, other: Any) -> bool:
        if isinstance(other, StructureElement) and other.structure == element.structure:
            return element.value == other.value
        return element.value == other

    def elements_ge(self, element: StructureElement, other: Any) -> bool:
        if isinstance(other, StructureElement) and other.structure == element.structure:
            return element.value >= other.value
        return element.value >= other

    def elements_gt(self, element: StructureElement, other: Any) -> bool:
        if isinstance(other, StructureElement) and other.structure == element.structure:
            return element.value > other.value
        return element.value > other

    def elements_le(self, element: StructureElement, other: Any) -> bool:
        if isinstance(other, StructureElement) and other.structure == element.structure:
            return element.value <= other.value
        return element.value <= other

    def elements_lt(self, element: StructureElement, other: Any) -> bool:
        if isinstance(other, StructureElement) and other.structure == element.structure:
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

    def __repr__(self):
        return self.__str__()

    @abstractmethod
    def __eq__(self, other):
        """
        Each structure must implement its equality with other structures
        """
        return self is other

    @property
    def name(self) -> str:
        """Returns the display name of the structure"""
        return type(self).__class__.__name__


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

    def __mod__(self, other):
        return self.structure.elements_mod(self, other)

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

    def __bool__(self):
        return bool(self.value)

    def __str__(self):
        return f"<{self.structure.name}: {self.value}>"

    def __repr__(self):
        return self.__str__()

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

    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        """other - self = -self + other"""
        return self.ainverse + other

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

    def __eq__(self, other):
        """
        Every other Zn with the same n value is considered equal
        """
        return isinstance(other, Zn) and other.n == self.n

    @override
    def __str__(self):
        if self.n > MAX_STR_ELEMENTS:
            elements = list(range(ceil(MAX_STR_ELEMENTS / 2))) + ["..."] + list(range(self.n-MAX_STR_ELEMENTS // 2, self.n))
        return f"<{self.name}: {elements}>"

    @override
    def __iter__(self) -> Iterable[GroupElement]:
        return super().__iter__()

    @override
    def elements_eq(self, element: GroupElement, other: Any) -> bool:
        if isinstance(other, StructureElement) and other.structure == element.structure:
            return element.value == other.value
        if isinstance(other, int):
            return element.value == other % self.n
        return element.value == other

    @override
    def elements_ge(self, element: GroupElement, other: Any) -> bool:
        if isinstance(other, StructureElement) and other.structure == element.structure:
            return element.value >= other.value
        if isinstance(other, int):
            return element.value >= other % self.n
        return element.value >= other

    @override
    def elements_gt(self, element: GroupElement, other: Any) -> bool:
        if isinstance(other, StructureElement) and other.structure == element.structure:
            return element.value > other.value
        if isinstance(other, int):
            return element.value > other % self.n
        return element.value > other

    @override
    def elements_le(self, element: GroupElement, other: Any) -> bool:
        if isinstance(other, StructureElement) and other.structure == element.structure:
            return element.value <= other.value
        if isinstance(other, int):
            return element.value <= other % self.n
        return element.value <= other

    @override
    def elements_lt(self, element: GroupElement, other: Any) -> bool:
        if isinstance(other, StructureElement) and other.structure == element.structure:
            return element.value < other.value
        if isinstance(other, int):
            return element.value < other % self.n
        return element.value < other

    @override
    def elements_add(self, a, b):

        # adding an element of certain structure
        if isinstance(b, StructureElement):
            if b.structure == self:  # cannot add elements from different structures
                return self((a.value + b.value) % self.n)
            raise AttributeError(f"cannot add elements from different groups: {a.structure} and {b.structure}")

        # adding an integer
        if isinstance(b, int):
            return self((a.value + b) % self.n)

        raise NotImplementedError(f"Addition is undefined for types: {type(a)}, {type(b)}")

    @override
    def elements_sub(self, a: GroupElement, b: Any) -> GroupElement:

        # subtracting an element of certain structure
        if isinstance(b, StructureElement):
            if b.structure == self:
                return self((a.value - b.value) % self.n)
            raise AttributeError(f"cannot subtract elements from different groups: {a.structure} and {b.structure}")

        # subtracting an integer
        if isinstance(b, int):
            return self((a.value - b) % self.n)

        raise NotImplementedError(f"Subtraction is undefined for types: {type(a)}, {type(b)}")

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
    __structure__: Field

    def is_quadratic_residue(self) -> bool:
        return self.field.is_quadratic_residue(self)

    def __rmul__(self, other):
        return self * other

    def __rpow__(self, other):
        return self.structure(other) ** self

    @property
    def sqrt(self):
        return self.structure.sqrt(self)

    @property
    def inverse(self) -> FieldElement:
        """Alias for multiplicative inverse since"""
        return self.minverse

    @property
    def field(self) -> Field:
        """Alias for self.structure"""
        return self.structure


class Field(AbstractStructure, metaclass=ABCMeta):
    """
    Algebraic field - https://en.wikipedia.org/wiki/Field_(mathematics)
    Supports additive and multiplicative notations.
    """

    def is_quadratic_residue(self, element: FieldElement) -> bool:
        raise NotImplementedError

    @abstractmethod
    def sqrt(self, element: FieldElement) -> FieldElement | None:
        """Returns sqrt of the given field element or None if it doesn't exist"""

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
        self.__nonresidue__ = None

    def __call__(self, value: int | FieldElement) -> FieldElement:

        # the member of equal field is given
        if isinstance(value, FieldElement) and value.field == self:
            value.__structure__ = self
            return value

        # integer is given
        assert isinstance(value, int), "num must be integer or the member of the equal field"
        return FieldElement(value=value % self.p, structure=self)

    def get_random_element(self) -> FieldElement:
        """Returns random element of this field"""
        return self(random.randint(0, self.p-1))

    @override
    def is_quadratic_residue(self, element: FieldElement) -> bool:
        # Euler’s criterion
        return not element.value or element ** ((self.p-1)//2) == 1

    def get_nonresidue(self):
        """
        :return: first found quadratic non-residue or None if it doesn't exist (in Z/2Z only)
        """
        if self.__nonresidue__ is None:
            for candidate in self:
                if not self.is_quadratic_residue(candidate):
                    self.__nonresidue__ = candidate
                    break
        return self.__nonresidue__

    def sqrt(self, element: FieldElement) -> FieldElement | None:
        # Tonelli–Shanks algorithm - https://en.wikipedia.org/wiki/Tonelli–Shanks_algorithm
        MAX_ITTERATIONS = 512

        # trivial for Z/2Z (Tonelli-shanks cannot be applied here)
        if self.p == 2:
            return element

        if not self.is_quadratic_residue(element):
            return None

        # By factoring out powers of 2, find q and s such that p-1 = q*2^s with q odd
        p = self.p
        t = self(p - 1)
        s = self(0)
        while not t % 2:
            s += 1
            t.value //= 2
        q = t

        z = self.get_nonresidue()
        m = s
        c = z ** q
        t = element ** q
        r = element ** ((q + 1) / 2)

        for _ in range(MAX_ITTERATIONS):
            if t == 0:
                return self(0)
            if t == 1:
                return r
            i = self(1)
            while t ** (2 ** i.value) != 1:
                i += 1
            b = c ** (2 ** (m - i - 1))
            m = i
            c = b ** 2
            t *= b ** 2
            r *= b
        else:
            raise RuntimeError(f"Exceeded maximum number of iterations when finding sqrt of  {element}")

    @override
    def elements_mul(self, a: StructureElement, b: Any) -> FieldElement:

        # multiplication with the element of certain structure
        if isinstance(b, StructureElement):
            if b.structure == self:
                return self((a.value * b.value) % self.p)
            raise AttributeError(f"cannot multiply elements from different groups: {a.structure} and {b.structure}")

        # with integer
        if isinstance(b, int):
            return self((a.value * b) % self.p)

    @override
    def element_pow(self, base: FieldElement, power, modulo) -> FieldElement:

        # extracting the power as integer into b variable
        if isinstance(power, StructureElement):
            if power.structure != self:
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
    def elements_div(self, element: FieldElement, b: Any) -> FieldElement:

        # dividing by a structure element
        if isinstance(b, StructureElement):
            if b.structure == self:
                return self(element.value * b.minverse.value)
            raise AttributeError(f"cannot divide element of {element.structure} by element of {b.structure}")

        # dividing by integer
        if isinstance(b, int):
            return self(element.value * self(b).minverse.value)

        raise NotImplementedError(f"Division is undefined for types: {type(element)}, {type(b)}")

    @override
    def elements_mod(self, element: FieldElement, modulus: Any) -> FieldElement:

        # modulus is a structure element
        if isinstance(modulus, GroupElement):
            return self(element.value % modulus.value)

        if isinstance(modulus, int):
            return self(element.value % modulus)

        raise NotImplementedError(f"Modulo division is undefined for types: {type(a)}, {type(b)}")

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
