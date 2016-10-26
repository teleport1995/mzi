import random


class DES:
    chunk_size = 64

    direct_ip_table = [57,49,41,33,25,17,9,1,59,51,43,35,27,19,11,3,61,53,45,37,29,21,13,5,63,55,47,39,31,23,15,7,
                       56,48,40,32,24,16,8,0,58,50,42,34,26,18,10,2,60,52,44,36,28,20,12,4,62,54,46,38,30,22,14,6]

    inverse_ip_table = [39,7,47,15,55,23,63,31,38,6,46,14,54,22,62,30,37,5,45,13,53,21,61,29,36,4,44,12,52,20,60,
                        28,35,3,43,11,51,19,59,27,34,2,42,10,50,18,58,26,33,1,41,9,49,17,57,25,32,0,40,8,48,16,56,24]

    expand_table = [31,0,1,2,3,4,3,4,5,6,7,8,7,8,9,10,11,12,11,12,13,14,15,16,15,16,17,18,
                    19,20,19,20,21,22,23,24,23,24,25,26,27,28,27,28,29,30,31,0]

    s_table = [
        [
            [14, 4, 13, 1, 2, 15, 11, 8, 8, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
        ],
        [
            [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
        ],
        [
            [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
        ],
        [
            [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
        ],
        [
            [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
        ],
        [
            [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
        ],
        [
            [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
        ],
        [
            [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
        ],
    ]

    p_table = [15,6,19,20,28,11,27,16,0,14,22,25,4,17,30,9,1,7,23,13,31,26,2,8,18,12,29,5,21,10,3,24]

    key_table = [56, 48, 40, 32, 24, 16, 8, 0, 57, 49, 41, 33, 25, 17,
                 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35,
                 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21,
                 13, 5, 60, 52, 44, 36, 28, 20, 12, 4, 27, 19, 11, 3]

    left_shift_table = [1, 2, 4, 6, 8, 10, 12, 14, 15, 17, 19, 21, 23, 25, 27, 28]

    right_shift_table = [0, 1, 3, 5, 7, 9, 11, 13, 14, 16, 18, 20, 22, 24, 26, 27]

    after_shift_table = [13, 16, 10, 23, 0, 4, 2, 27, 14, 5, 20, 9, 22, 18, 11, 3, 25, 7, 15, 6, 26, 19, 12, 1, 40,
                         51, 30, 36, 46, 54, 29, 39, 50, 44, 32, 47, 43, 48, 38, 55, 33, 52, 45, 41, 49, 35, 28, 31]

    def direct_ip(self, data):
        return [data[x] for x in self.direct_ip_table]

    def inverse_ip(self, data):
        return [data[x] for x in self.inverse_ip_table]

    def xor(self, a, b):
        return [x ^ y for x, y in zip(a, b)]

    def shift(self, key, l):
        return key[l:] + key[:l]

    def get_k(self, key, iteration):
        cidi = (self.shift(key[:len(key) >> 1], self.left_shift_table[iteration - 1]) +
                self.shift(key[len(key) >> 1:], self.left_shift_table[iteration - 1]))
        return [cidi[x] for x in self.after_shift_table]

    def expand(self, r):
        return [r[x] for x in self.expand_table]

    def get_num(self, a):
        ans = 0
        for x in a:
            ans = ans * 2 + x
        return ans

    def get_arr(self, num, length):
        ans = []
        while num:
            ans.append(num % 2)
            num /= 2
        ans.reverse()
        return [0] * (length - len(ans)) + ans

    def add_parity(self, key):
        ans = []
        for i in range(8):
            chunk = key[i*7:(i+1)*7]
            ans.extend(chunk)
            ans.append(sum(chunk) & 1)
        return ans

    def f(self, r, key):
        r = self.expand(r)
        r = self.xor(r, key)
        answer = []
        for i in xrange(8):
            chunk = r[i*6:(i+1)*6]
            row = self.get_num([chunk[0], chunk[-1]])
            col = self.get_num(chunk[1:5])
            answer.extend(self.get_arr(self.s_table[i][row][col], 4))
        answer = [answer[x] for x in self.p_table]
        return answer

    def feistel(self, data, key):
        l = data[:self.chunk_size >> 1]
        r = data[self.chunk_size >> 1:]
        for i in range(1, 17):
            l, r = r, self.xor(l, self.f(r, self.get_k(key, i)))
        return l + r

    def encode_chunk(self, data, key):
        key = self.add_parity(key)
        key = [key[x] for x in self.key_table]
        ip_data = self.direct_ip(data)
        feistel_data = self.feistel(ip_data, key)
        data = self.inverse_ip(feistel_data)
        return data

    def get_inverse_k(self, key, iteration):
        cidi = (self.shift(key[:len(key) >> 1], (len(key) >> 1) - self.right_shift_table[iteration - 1]) +
                self.shift(key[len(key) >> 1:], (len(key) >> 1) - self.right_shift_table[iteration - 1]))
        return [cidi[x] for x in self.after_shift_table]

    def inverse_feistel(self, data, key):
        l = data[:self.chunk_size >> 1]
        r = data[self.chunk_size >> 1:]
        for i in range(1, 17):
            l, r = self.xor(r, self.f(l, self.get_inverse_k(key, i))), l
        return l + r

    def decode_chunk(self, data, key):
        key = self.add_parity(key)
        key = [key[x] for x in self.key_table]
        ip_data = self.direct_ip(data)
        feistel_data = self.inverse_feistel(ip_data, key)
        data = self.inverse_ip(feistel_data)
        return data


class TripleDES:
    def __init__(self):
        self.des = DES()

    def encode_chunk(self, data, k1, k2, k3):
        return self.des.encode_chunk(self.des.decode_chunk(self.des.encode_chunk(data, k3), k2), k1)

    def decode_chunk(self, data, k1, k2, k3):
        return self.des.decode_chunk(self.des.encode_chunk(self.des.decode_chunk(data, k1), k2), k3)


def generate_key():
    return [random.randint(0, 1) for _ in xrange(56)]


def main():
    des = DES()
    key = generate_key()
    data = [random.randint(0, 1) for _ in xrange(64)]
    print data
    encode_data = des.encode_chunk(data, key)
    print encode_data
    decode_data = des.decode_chunk(encode_data, key)
    print decode_data
    print data == decode_data

    triple_des = TripleDES()
    keys = [generate_key() for _ in xrange(3)]
    encode_data = triple_des.encode_chunk(data, *keys)
    print encode_data
    decode_data = triple_des.decode_chunk(encode_data, *keys)
    print decode_data
    print data == decode_data

if __name__ == "__main__":
    main()
