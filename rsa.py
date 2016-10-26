import random
import time

class PrimeHelper:

    @staticmethod
    def check_prime_iteration(n, n_, t, a):
        x = pow(a, n_, n)
        if x == 1:
            return True
        for _ in xrange(t):
            if x == n-1:
                return True
            x = pow(x, 2, n)
        return False


    @staticmethod
    def check_prime(n, iterations=60):
        if n % 2 == 0:
            return False
        n_ = n - 1
        t = 0
        while n_ % 2 == 0:
            n_ >>= 1
            t += 1
        for iteration in xrange(iterations):
            a = random.randint(2, n - 1)
            if not PrimeHelper.check_prime_iteration(n, n_, t, a):
                return False
        return True

    @staticmethod
    def get_prime(bit_size=2048):
        while True:
            prime_to_check = random.randint(1<<(bit_size-2), (1<<(bit_size-1))-1) * 2 + 1
            if PrimeHelper.check_prime(prime_to_check):
                return prime_to_check


class Euclid:

    @staticmethod
    def gcd(x, y):
        if x == 0:
            return 0, 1
        nx, ny = Euclid.gcd(y % x, x)
        return ny - (y / x) * nx, nx

    @staticmethod
    def get_inv(e, n):
        x = Euclid.gcd(e, n)[0]
        if x < 0:
            x += n
        return x


class RSAKey:
    def __init__(self, n, e, d):
        self.n = n
        self.e = e
        self.d = d

    def public(self):
        return self.e, self.n

    def private(self):
        return self.d, self.n


class RSA:
    def encode(self, data, public_key):
        return pow(data, *public_key)

    def decode(self, data, private_key):
        return pow(data, *private_key)

    def get_key(self, bit_size=2048):
        e = 17
        while True:
            p, q = (PrimeHelper.get_prime(bit_size) for _ in xrange(2))
            phi = (p-1)*(q-1)
            if p == q or phi % 17 == 0:
                continue
            d = Euclid.get_inv(e, phi)
            return RSAKey(p * q, e, d)


def main():
    rsa = RSA()
    key = rsa.get_key(bit_size=512)
    data = random.randint(0, 1 << 500)
    print data
    encode_data = rsa.encode(data, key.public())
    print encode_data
    decode_data = rsa.decode(encode_data, key.private())
    print decode_data
    print data == decode_data

if __name__ == "__main__":
    main()
