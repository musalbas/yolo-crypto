import random

"""Generate dh params

Returns (prime, generator)
"""
def generate_dh_params(bits):
    while True:
        q = _generate_random_prime(bits)
        p = 2*q+1 # generate "safe" prime
        if _mr_prime_test(p, 50):
            break

    return (p, 2)

"""Generate a public and private key

Returns (public, private)
"""
def generate_keypair(bits, dh_params):
    rand = random.SystemRandom()
    private = rand.randrange(2**(bits-1), 2**bits)
    if private > dh_params[0]:
        raise ValueError("private key cannot be larger than dh modulus")
    public = _power(dh_params[1], private, dh_params[0])
    return (public, private)

"""Test a key exchange"""
def test_key_exchange(dh_modulus_bits, key_bits):
    dh_params = generate_dh_params(dh_modulus_bits)
    alice = generate_keypair(key_bits, dh_params)
    bob = generate_keypair(key_bits, dh_params)

    if _power(alice[0], bob[1], dh_params[0]) == _power(bob[0], alice[1], dh_params[0]):
        return True
    else:
        return False

"""Generate random prime number"""
def _generate_random_prime(bits):
    rand = random.SystemRandom()
    n = 0
    while (n == 0 or not _mr_prime_test(n, 50)):
        n = rand.randrange(2**(bits-1), 2**bits)
    return n

"""Miller-Rabin primality test"""
def _mr_prime_test(n, witnesses):
    rand = random.SystemRandom()
    for i in range(witnesses):
        a = rand.randrange(2, n-1)
        (r, prime) = _power2(a, n-1, n)
        if r != 1 or not prime:
            return False
    return True

"""Compute a^p%n"""
def _power(a, p, n):
    if p == 0:
        r = 1
    else:
        x = _power(a, int(p/2), n)
        r = (x*x)%n
    if p%2 == 1:
        r = r*a
        r = r%n
    return r

"""Fermat's little theorem and non-trivial square root test"""
def _power2(a, p, n):
    prime = True
    if p == 0:
        r = 1
    else:
        x = _power(a, int(p/2), n)
        r = (x*x)%n
        if r == 1 and x != 1 and x != n-1:
            prime = False
    if p%2 == 1:
        r = r*a
    return (r, prime)
