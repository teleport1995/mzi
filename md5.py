import math


class MD5:

    T =[int(2**32 * abs(math.sin(i + 1))) for i in xrange(64)]
    MASK = 2**32-1

    def neg(self, x, l=32):
        return (2**l-1) ^ x

    def fun_f(self, x, y, z):
        return z ^ (x & (y ^ z))

    def fun_g(self, x, y, z):
        return y ^ (z & (x ^ y))

    def fun_h(self, x, y, z):
        return x ^ y ^ z

    def fun_i(self, x, y, z):
        return y ^ (self.neg(z) | x)

    def left_shift(self, x, s):
        return ((x << s) | (x >> (32-s))) & self.MASK

    def round(self, a, b, c, d, xk, s, i, func):
        return (b + self.left_shift((a + func(b, c, d) + xk + self.T[i]) & self.MASK, s)) & self.MASK

    def get_bits(self, l, k):
        ans = []
        for i in xrange(k / 8):
            x = l & 255
            cur = []
            for _ in xrange(8):
                cur.append(x & 1)
                x >>= 1
            cur.reverse()
            ans.extend(cur)
            l >>= 8
        return ans

    def get_num(self, bits):
        ans = 0
        for i in xrange(24, -1, -8):
            for j in xrange(8):
                ans = ans * 2 + bits[i+j]
        return ans

    def extend_data(self, data):
        l = len(data)
        data.extend([1, 0])
        while len(data) % 512 != 448:
            data.append(0)
        bits = self.get_bits(l, 64)
        data.extend(bits)
        return data

    def main_cycle(self, data):
        data = [self.get_num(data[i:i+32]) for i in xrange(0, len(data), 32)]
        regs = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476]
        arr1, arr2, arr3, arr4 = [7, 12, 17, 22], [5, 9, 14, 20], [4, 11, 16, 23], [6, 10, 15, 21]
        for i in range(0, len(data), 16):
            chunk = data[i:i+16]
            cur = regs[::]

            for i in xrange(16):
                num = (4 - i % 4) % 4
                arr = cur[num:] + cur[:num]
                cur[num] = self.round(*arr, xk=chunk[i], s=arr1[i%4], i=i, func=self.fun_f)
            for i in xrange(16):
                num = (4 - i % 4) % 4
                arr = cur[num:] + cur[:num]
                cur[num] = self.round(*arr, xk=chunk[(1+5*i)%16], s=arr2[i%4], i=16+i, func=self.fun_g)
            for i in xrange(16):
                num = (4 - i % 4) % 4
                arr = cur[num:] + cur[:num]
                cur[num] = self.round(*arr, xk=chunk[(5+3*i)%16], s=arr3[i%4], i=32+i, func=self.fun_h)
            for i in xrange(16):
                num = (4 - i % 4) % 4
                arr = cur[num:] + cur[:num]
                cur[num] = self.round(*arr, xk=chunk[(7*i)%16], s=arr4[i%4], i=48+i, func=self.fun_i)

            for i in xrange(4):
                regs[i] = (regs[i] + cur[i]) & self.MASK
        ans = []
        for x in regs:
            for j in xrange(4):
                ans.append(x & 255)
                x >>= 8
        return ans

    def encode_bits(self, data):
        extended_data = self.extend_data(data[::])
        return self.main_cycle(extended_data)

    def encode_str(self, s):
        data = []
        for x in s:
            data.extend(self.get_bits(ord(x), 8))
        return bytes_to_hex(self.encode_bits(data))


def bytes_to_hex(data):
    return ("".join((hex(x)[2:]).rjust(2, '0') for x in data)).upper()


def main():
    md5 = MD5()
    print md5.encode_str("")
    print md5.encode_str("md4")
    print md5.encode_str("md5")

if __name__ == "__main__":
    main()