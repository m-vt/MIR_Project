# Python3 implementation
import sys
from math import log

log2 = lambda x: log(x, 2)


def Unary(x):
    return (x - 1) * '1' + '0'


def Binary(x, l=1):
    s = '{0:0%db}' % l
    return s.format(x)


def Elias_Gamma(x):
    if (x == 0):
        return '0'

    n = 1 + int(log2(x))
    b = x - 2 ** (int(log2(x)))

    l = int(log2(x))

    return Unary(n) + Binary(b, l)

def GammaCode(numbers):
    bytes_list = []
    for number in numbers:
        bytes_list.append(Elias_Gamma(number).encode())
    return b"".join(bytes_list)


input=[824,5,214577,824,5,214577824,5,214577824,5,214577824,5,214577824,5,214577824,5,214577824,5,214577824,5,214577824,5,214577824,5,214577]
out=GammaCode(input)
print(out)
#out2=out.encode()
print("size before", sys.getsizeof(input))
print("size after", sys.getsizeof(out))
#print(type(out2))
#print(out2)
#print("size after", sys.getsizeof(out2))
