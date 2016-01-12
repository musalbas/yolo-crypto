import random

"""
Generate a public and private key

Returns dict {'p': (n, e), 's': (n, d)}
"""
def generate_keypair(bits):
    # choose e = 3
    e = 3

    # generate p, q and s
    p = 0
    q = 0
    while True:
        p = _generate_random_prime(bits/2)
        q = _generate_random_prime(bits/2)
        if p == q: # p and q must be unique
            continue

        # compute s
        s = (p-1)*(q-1)
        if gcd(e, s) != 1: # gcd(e, s) must be 1
            continue

        break

    # compute n
    n = p*q

    # compute d
    (g, x, y) = e_gcd(e, s)
    d = x % s

    return {'p': (n, e), 's': (n, d)}

"""Encrypt m with key k"""
def encrypt(m, k):
    return _power(m, k['p'][1], k['s'][0])

"""Decrypt c with key k"""
def decrypt(c, k):
    return _power(c, k['s'][1], k['s'][0])

"""Euclid's algorithm"""
def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a%b)

"""Euclid's extended algorithm"""
def e_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = e_gcd(b%a, a)
        return (g, x-(b/a)*y, y)

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
