alphabet = '''abcdefghijklmnopqrstvwxyz'''
right_frequencies = [8.1, 1.4, 2.7, 3.9, 13.1, 2.9, 2.0, 5.2, 6.5, 0.2, 0.4, 3.4, 2.5,
                     7.2, 7.9, 2.0, 0.1, 6.9, 6.1, 10.5, 2.4, 0.9, 1.5, 0.2, 1.9, 0.1]


def encode_char(c, k):
    if c.lower() not in alphabet:
        return c
    is_lower = True
    if c.isupper():
        c = c.lower()
        is_lower = False
    delta = alphabet.find(c)
    delta = (delta + k) % len(alphabet)
    if delta < 0:
        delta += len(alphabet)
    ans = alphabet[delta]
    if not is_lower:
        ans = ans.upper()
    return ans


def encode(s, k):
    return "".join([encode_char(c, k) for c in s])


def decode(s, k):
    return "".join([encode_char(c, -k) for c in s])


def get_frequencies(s):
    s = s.lower()
    a = [s.count(x) for x in alphabet]
    a_sum = sum(a)
    return [x * 100. / a_sum for x in a]


def get_predict(frequencies):
    return sum([abs(x - y) for x, y in zip(frequencies, right_frequencies)])


def smart_decode(s):
    predicts = []
    for k in xrange(len(alphabet)):
        cur = encode(s, k)
        cur_frequencies = get_frequencies(cur)
        predict = get_predict(cur_frequencies)
        predicts.append((predict, cur))
    return min(predicts)[1]

if __name__ == "__main__":
    sentence = """The Assyrian came down like the wolf on the fold,
    And his cohorts were gleaming in purple and gold;
    And the sheen of their spears was like stars on the sea,
    When the blue wave rolls nightly on deep Galilee."""

    print encode(sentence, 1)
    print decode(encode(sentence, 1), 1)
    print smart_decode(encode(sentence, 1))

    other_sentence = """Like the leaves of the forest when Summer is green,
    That host with their banners at sunset were seen:
    Like the leaves of the forest when Autumn hath blown,
    That host on the morrow lay withered and strown."""

    print smart_decode(encode(other_sentence, 10))
