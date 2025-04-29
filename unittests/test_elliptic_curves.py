import unittest
from hypothesis import given, assume, example, strategies as st

from abstractAlgebra.structures import Fp
from abstractAlgebra.elliptic_curves import *

class TestElliptic(unittest.TestCase):

    @given(
        a=st.integers(-5, 100),
        b=st.integers(-5, 100),
        p=st.integers(-5, 50)
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

if __name__ == '__main__':
    unittest.main()
