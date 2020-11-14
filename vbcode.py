from __future__ import division
from struct import pack, unpack
from bitarray import bitarray
import sys
import struct

def encode_number(number):
    bytes_list = []
    while True:
        bytes_list.insert(0, number % 128)
        if number < 128:
            break
        number = number // 128
    bytes_list[-1] += 128
    t=""
    for i in bytes_list:
        t+=format(i, '#010b')[2:]
    return t

def encode(numbers):

    bytes_list=""
    for number in numbers:
        bytes_list+=encode_number(number)
    return  bitarray(bytes_list, endian='little')

def decode(bytestream):
    
    numbers=[]
    temp=""
    for k in range(len(bytestream)//8):
        i=8*k
        if  not bytestream[i]:
            temp+=str(bytestream[i:i+8])[11:18]
        else:
            temp += str(bytestream[i:i + 8])[11:18]
            numbers.append(int('0b'+temp, 2))
            temp=""

    return numbers




q=encode([824,5,214577,824,5,214577])
print(q)
print("size before", sys.getsizeof([824,5,214577,824,5,214577]))
print("size after", sys.getsizeof( bitarray(q, endian='little')))
print(decode(q))

