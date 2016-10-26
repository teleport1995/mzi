# x^256+x^16+x^3+x+1
import random


class Scrambler:
    def __init__(self, size, scrambler, initial):
        self.size = size
        self.scrambler = scrambler
        self.cur = initial
        self.all_without_largest = (1 << (size - 1)) - 1

    def next(self):
        next_bit = bin(self.cur & self.scrambler).count("1") & 1
        ans = self.cur >> (self.size - 1) # 1 if (self.cur & (1 << (self.size - 1))) else 0
        self.cur &= self.all_without_largest
        self.cur <<= 1
        self.cur |= next_bit
        return ans


def encode(data, scrambler):
    return [scrambler.next() ^ x for x in data]


def decode(data, scrambler):
    return encode(data, scrambler)


def main():
    size = 256
    mask = (1 << 16) + (1 << 3) + (1 << 1) + (1 << 0)
    initial = random.randint(1, (1 << size) - 1)
    print initial
    scrambler = Scrambler(size, mask, initial)
    initial_data = [random.randint(0, 1) for _ in range(10000)]
    print initial_data
    encode_data = encode(initial_data, scrambler)
    print encode_data
    scrambler = Scrambler(size, mask, initial)
    decode_data = decode(encode_data, scrambler)
    print decode_data
    print initial_data == decode_data

if __name__ == "__main__":
    main()
