from hashlib import sha256
import random
from rsa import PrimeHelper


class DomainParams(object):
    def __init__(self, p, q, g):
        self.p = p
        self.q = q
        self.g = g


class Signature(object):
    def __init__(self, r, s):
        self.r = r
        self.s = s


def generate_domain_params(N=256, L=2048):
    while True:
        q = random.randint(2**(N-2), 2**(N-1) - 1) * 2 + 1
        if PrimeHelper.check_prime(q, 40):
            break
    left = 2**(L-1) / q + 1
    right = 2**L / q
    while True:
        p = random.randint(left, right) * q + 1
        if p % 2 == 0:
            continue
        if PrimeHelper.check_prime(p, 40):
            break
    st = (p - 1) / q
    h = 2
    while True:
        g = pow(h, st, p)
        if g != 1:
            break
        h += 1
    return DomainParams(p, q, g)


def generate_keys(domain_params):
    secret = random.randint(1, domain_params.q - 1)
    public = pow(domain_params.g, secret, domain_params.p)
    return secret, public


def sign(message, domain_params, secret):
    while True:
        k = random.randint(1, domain_params.q - 1)
        r = pow(domain_params.g, k, domain_params.p) % domain_params.q
        if r == 0:
            continue
        s = pow(k, domain_params.q-2, domain_params.q) * (int(sha256(message).hexdigest(), 16) + secret * r) % domain_params.q
        if s == 0:
            continue
        return Signature(r, s)


def check_signature(message, signature, domain_params, public):
    w = pow(signature.s, domain_params.q - 2, domain_params.q)
    u1 = int(sha256(message).hexdigest(), 16) * w % domain_params.q
    u2 = signature.r * w % domain_params.q
    v = (pow(domain_params.g, u1, domain_params.p) * pow(public, u2, domain_params.p) % domain_params.p) % domain_params.q
    return signature.r == v


def main():
    domain_params = generate_domain_params()
    secret, public = generate_keys(domain_params)
    message = "DSA algorithm"
    signature = sign(message, domain_params, secret)
    print check_signature(message, signature, domain_params, public)
    print check_signature(message, Signature(signature.r, signature.s + 1), domain_params, public)


if __name__ == "__main__":
    main()