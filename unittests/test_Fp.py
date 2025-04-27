import random
import unittest
from abstractAlgebra.structures import Fp
from hypothesis import given, assume, example, strategies as st

small_primes = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
    53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107,
    109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
    179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239,
    241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311,
    313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383,
    389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457,
    461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541,
    547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613,
    617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683,
    691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769,
    773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857,
    859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941,
    947, 953, 967, 971, 977, 983, 991, 997
]
prime_numbers = st.sampled_from(small_primes)


class FpTest(unittest.TestCase):

    @given(
        a=st.integers(min_value=0, max_value=2000),
        b=st.integers(min_value=0, max_value=2000),
        p=prime_numbers
    )
    def test_equality(self, a, b, p):
        """
        Fp(a) == Fp(b) or Fp(a) == b must be true iff a==b
        :param a:
        :param b:
        :param p:
        :return:
        """
        assume(a % p != b % p)

        field = Fp(p)
        self.assertEqual(field(a), field(a))
        self.assertEqual(field(a), a, "Failed to compare equality of fp(n) and n")
        self.assertNotEqual(field(a), field(b), "False positive equality of field and integer")
        self.assertNotEqual(field(a), b, "False positive equality of field and integer")

    @given(
        a=st.integers(min_value=0, max_value=2000),
        p=prime_numbers
    )
    def test_additive_inverse(self, a, p):
        """
        Fp(a) + (-Fp(a)) == Fp.aneutral (0) must be true (additive inverse)
        :param a:
        :param p:
        :return:
        """
        field = Fp(p)
        el = field(a)
        self.assertEqual(el + el.ainverse, field.aneutral, f"{el.ainverse} is not a negation of {el}")

    @given(
        a=st.integers(min_value=0, max_value=2000),
        p=prime_numbers
    )
    def test_multiplicative_inverse(self, a, p):
        """
        Test that Fp(a) * Fp(a).inverse == 1 for a ≠ 0,
        and Fp(0).inverse == None.
        """
        field = Fp(p)
        el = field(a)

        if a % p == 0:
            self.assertIsNone(el.minverse, f"Expected no inverse for {el}, got {el.minverse} instead")
        else:
            self.assertIsNotNone(el.minverse, f"Expected inverse for {el}, got None")
            self.assertEqual(el * el.minverse, field.mneutral, f"{el.minverse} is not an inverse of {el}")

    @given(
        a=st.integers(min_value=0, max_value=32),
        b=st.integers(min_value=0, max_value=64),
        p=prime_numbers
    )
    def test_power(self, a, b, p):
        """
        Test that a**b if Fp(p) equals to a**b mod p
        """
        field = Fp(p)
        self.assertEqual(field(a)**field(b), pow(a % p, b % p) % p, f"Wrong power for {a}**{b} (mod {p})")


if __name__ == '__main__':
    unittest.main()
