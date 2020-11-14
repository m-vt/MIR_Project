import sys
from math import log
from struct import pack, unpack
from bitarray import bitarray



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


def encode_Gamma(list):
    str=""
    for x in list:
        if (x == 0):
            return '0'
        n = 1 + int(log2(x))
        b = x - 2 ** (int(log2(x)))

        l = int(log2(x))

        str+=(Unary(n) + Binary(b, l))
    return bitarray(str, endian='little')

def decode_Gamma(bytes):

    numbers=[]
    a=str(bytes)[10:len(str(bytes))-2]
    counter=0
    pointer=0
    flag=False
    k=0
    while(k<len(a)):
        if flag:
            counter += 1
            if a[k]=='0':
                flag=False
                numbers.append(int("1"+a[pointer+counter+1:pointer+2*counter+1], 2))
                pointer+=2*counter+1
                counter=1
                k=pointer
        else:
            if a[k] =='1':
                flag=True
            else:
                pointer += 1
        k+=1

    return numbers







out=encode_Gamma([24,511,1025])
print("out")
print(out)
print(decode_Gamma(out))

print("size before", sys.getsizeof([24,511,1025]))
print("size after", sys.getsizeof(out))


