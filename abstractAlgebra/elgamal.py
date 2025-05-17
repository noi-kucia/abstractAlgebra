from abstractAlgebra.structures import *
from abstractAlgebra.elliptic_curves import *

ELGAMAL_MAX_I_ITERATIONS = 128

def elgamal_genkey(p: int) -> tuple[EllipticCurvePoint, EllipticCurvePoint, int]:
    """
    Returns 2 points which represent a public key and a number that is a part of private key.
    """
    # TODO: test whether p is prime or not

    curve = random_elliptic_curve(p)
    pk = (curve.field.get_random_element() % (curve.field.p - 1)).value + 1  # 1<k<p-1
    alpha = curve.get_random_point()
    beta = alpha * pk

    return alpha, beta, pk

def elgamal_encrypt(message: FieldElement,
                    alpha: EllipticCurvePoint,
                    beta: EllipticCurvePoint,
                    parameter: int) -> tuple[EllipticCurvePoint, EllipticCurvePoint]:
    """
    Encrypts a message using ElGamal encryption by 2 given points that must belong to the same elliptic curve and given parameter.
    Message could be either an integer or an element curve is built on (essentially anything that can be converted to a field element).

    Returns 2 points (c1, c2).
    """
    curve = alpha.curve
    field = curve.field

    assert message in field, "message must be an element of the curve's field"
    assert curve == beta.curve, "points must belong to the same curve"

    # generating i
    for c in range(ELGAMAL_MAX_I_ITERATIONS):
        i = field(c)
        message_x = parameter * message + i
        if curve.polynom(message_x).is_quadratic_residue():
            break
    else:
        raise RuntimeError("Cannot generate i. If you are sure it exists, try increasing the ELGAMAL_MAX_I_ITERATIONS parameter.")

    # cure point to be encrypted
    message_point = curve(message_x, curve.polynom(message_x).sqrt)

    # encrypting with random x
    x = field.get_random_element()
    с1 = alpha * x
    с2 = message_point + beta * x

    return с1, с2

def elgamal_decrypt(c1: EllipticCurvePoint,
                    c2: EllipticCurvePoint,
                    parameter: int,
                    pk: int):
    curve = c1.curve

    assert curve == c2.curve, "points must belong to the same curve"

    # decrypting
    beta_x = c1 * pk  # a * x*k = a * k*x = b * x
    message_point = c2 - beta_x
    message_x = message_point.x
    message = message_x // parameter

    return message

