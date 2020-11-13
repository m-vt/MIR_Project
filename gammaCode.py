# Python3 implementation
import sys
from math import log
from struct import pack, unpack
from bitstring import BitArray


log2 = lambda x: log(x, 2)

def bitstring_to_bytes(s):
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])


def Unary(x):
    return (x - 1) * '1' + '0'


def Binary(x, l=1):
    s = '{0:0%db}' % l
    return s.format(x)


def encode_Gamma(x):
    if (x == 0):
        return '0'

    n = 1 + int(log2(x))
    b = x - 2 ** (int(log2(x)))

    l = int(log2(x))

    return bitstring_to_bytes(Unary(n) + Binary(b, l))

def decode_Gamma(bytes):
    a = ''.join(format(byte, '08b') for byte in bytes)

    counter=0
    pointer=0
    flag=False
    for i in a:
        if flag:
            counter += 1
            if i=='0':
                break
        else:
            if i =='1':
                flag=True
            else:
                pointer += 1

    number="1"+a[pointer+counter+1:]

    return int(number, 2)







out=encode_Gamma(1025)
print(out)
print(decode_Gamma(out))

print("size before", sys.getsizeof(1025))
print("size after", sys.getsizeof(out))


