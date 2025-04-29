import unittest
from hypothesis import given, assume, example, strategies as st

from abstractAlgebra.structures import Fp
from abstractAlgebra.elliptic_curves import *

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

class TestElliptic(unittest.TestCase):

    @given(
        a=st.integers(-5, 100),
        b=st.integers(-5, 100),
        p=prime_numbers
    )
    def test_initialization(self, a, b, p):
        """
        Test that EllipticCurve constructor doesn't fail
        """

        # initializing with integers
        if 4*a**3 + 27*b ** 2 == 0 or p <= 1:
            # must return an assertion error because for such a and b, an elliptic curve cannot be constructed
            self.assertRaises(AssertionError, EllipticCurve, *(a, b, p))
        else:
            # must not fail otherwise
            EllipticCurve(a, b, p)

    @given(
        delta=st.integers(1, 100),
        p=prime_numbers
    )
    def test_contains(self, delta, p):
        """
        Tests that __contains__ method works properly
        """

        curve = random_elliptic_curve(p)
        curve_point = curve.get_random_point()
        shifted_point = (curve_point.x, curve.field(curve_point.y + delta))

        self.assertTrue(curve_point in curve, "__contain__ method returns False though the point must belong to it "
                                              "(except for the case if random_elliptic_curve function returns bad point)")

    @given(p=prime_numbers)
    def test_additive_inverse(self, p):
        """Test how additive negation/inverse works"""
        curve = random_elliptic_curve(p)
        point = curve.get_random_point()
        self.assertTrue(point.is_inverse_of(-point), f"{point} isn't inverse of {-point} though must be")


if __name__ == '__main__':
    unittest.main()


