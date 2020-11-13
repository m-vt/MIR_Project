from __future__ import division
from struct import pack, unpack
import sys

def encode_number(number):
    bytes_list = []
    while True:
        bytes_list.insert(0, number % 128)
        if number < 128:
            break
        number = number // 128
    bytes_list[-1] += 128
    return pack('%dB' % len(bytes_list), *bytes_list)

# def encode(numbers):
# 
#     bytes_list = []
#     for number in numbers:
#         bytes_list.append(encode_number(number))
#     return b"".join(bytes_list)

def decode(bytestream):

    n = 0

    bytestream = unpack('%dB' % len(bytestream), bytestream)
    for byte in bytestream:
        if byte < 128:
            n = 128 * n + byte
        else:
            n = 128 * n + (byte - 128)
            number=n
            n = 0
    return number




q=encode_number(5113443)
print(q)
print(decode(q))
print("size before", sys.getsizeof(511))
print("size after", sys.getsizeof(q))

