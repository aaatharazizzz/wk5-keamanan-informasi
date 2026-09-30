import socket, numpy
from collections.abc import Buffer
from bitarray import bitarray
from bitarray.util import ba2int, int2ba
from enum import Enum

class DESPermutationType(Enum):
    IP = 1
    PC1 = 2,
    PC2 = 3,
    P = 4,
    IP_INVERSE = 5,
    EXPAND = 6

DES_IP_TABLE = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9 , 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

DES_IP_INVERSE_TABLE = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9 , 49, 17, 57, 25
]

DES_EXPANSION_TABLE = [
    32, 1 , 2 , 3 , 4 , 5,
    4 , 5 , 6 , 7 , 8 , 9,
    8 , 9 , 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]

DES_PERMUTATION_TABLE = [
    16, 7 , 20, 21,
    29, 12, 28, 17,
    1 , 15, 23, 26,
    5 , 18, 31, 10,
    2 , 8 , 24, 14,
    32, 27, 3 , 9 ,
    19, 13, 30, 6 ,
    22, 11, 4 , 25
]

DES_PC1_TABLE = [
    57, 49, 41, 33, 25, 17, 9 ,
    1 , 58, 50, 42, 34, 26, 18,
    10, 2 , 59, 51, 43, 35, 27,
    19, 11, 3 , 60, 52, 44, 36,

    63, 55, 47, 39, 31, 23, 15,
    7 , 62, 54, 46, 38, 30, 22,
    14, 6 , 61, 53, 45, 37, 29,
    21, 13, 5 , 28, 20, 12, 4 ,
]

DES_PC2_TABLE = [
    14, 17, 11, 24, 1 , 5 ,
    3 , 28, 15, 6 , 21, 10,
    23, 19, 12, 4 , 26, 8 ,
    16, 7 , 27, 20, 13, 2 ,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32,
]

DES_SUBSTITUTION_TABLE = [
    [
        14, 4 , 13, 1 , 2 , 15, 11, 8 , 3 , 10, 6 , 12, 5 , 9 , 0 , 7 ,
        0 , 15, 7 , 4 , 14, 2 , 13, 1 , 10, 6 , 12, 11, 9 , 5 , 3 , 8 ,
        4 , 1 , 14, 8 , 13, 6 , 2 , 11, 15, 12, 9 , 7 , 3 , 10, 5 , 0 ,
        15, 12, 8 , 2 , 4 , 9 , 1 , 7 , 5 , 11, 3 , 14, 10, 0 , 6 , 13,
    ],
    [
        15, 1 , 8 , 14, 6 , 11, 3 , 4 , 9 , 7 , 2 , 13, 12, 0 , 5 , 10,
        3 , 13, 4 , 7 , 15, 2 , 8 , 14, 12, 0 , 1 , 10, 6 , 9 , 11, 5 ,
        0 , 14, 7 , 11, 10, 4 , 13, 1 , 5 , 8 , 12, 6 , 9 , 3 , 2 , 15,
        13, 8 , 10, 1 , 3 , 15, 4 , 2 , 11, 6 , 7 , 12, 0 , 5 , 14, 9 ,
    ],
    [
        10, 0 , 9 , 14, 6 , 3 , 15, 5 , 1 , 13, 12, 7 , 11, 4 , 2 , 8 ,
        13, 7 , 0 , 9 , 3 , 4 , 6 , 10, 2 , 8 , 5 , 14, 12, 11, 15, 1 ,
        13, 6 , 4 , 9 , 8 , 15, 3 , 0 , 11, 1 , 2 , 12, 5 , 10, 14, 7 ,
        1 , 10, 13, 0 , 6 , 9 , 8 , 7 , 4 , 15, 14, 3 , 11, 5 , 2 , 12,
    ],
    [
        7 , 13, 14, 3 , 0 , 6 , 9 , 10, 1 , 2 , 8 , 5 , 11, 12, 4 , 15,
        13, 8 , 11, 5 , 6 , 15, 0 , 3 , 4 , 7 , 2 , 12, 1 , 10, 14, 9 ,
        10, 6 , 9 , 0 , 12, 11, 7 , 13, 15, 1 , 3 , 14, 5 , 2 , 8 , 4 ,
        3 , 15, 0 , 6 , 10, 1 , 13, 8 , 9 , 4 , 5 , 11, 12, 7 , 2 , 14,
    ],
    [
        2 , 12, 4 , 1 , 7 , 10, 11, 6 , 8 , 5 , 3 , 15, 13, 0 , 14, 9 ,
        14, 11, 2 , 12, 4 , 7 , 13, 1 , 5 , 0 , 15, 10, 3 , 9 , 8 , 6 ,
        4 , 2 , 1 , 11, 10, 13, 7 , 8 , 15, 9 , 12, 5 , 6 , 3 , 0 , 14,
        11, 8 , 12, 7 , 1 , 14, 2 , 13, 6 , 15, 0 , 9 , 10, 4 , 5 , 3 ,
    ],
    [
        12, 1 , 10, 15, 9 , 2 , 6 , 8 , 0 , 13, 3 , 4 , 14, 7 , 5 , 11,
        10, 15, 4 , 2 , 7 , 12, 9 , 5 , 6 , 1 , 13, 14, 0 , 11, 3 , 8 ,
        9 , 14, 15, 5 , 2 , 8 , 12, 3 , 7 , 0 , 4 , 10, 1 , 13, 11, 6 ,
        4 , 3 , 2 , 12, 9 , 5 , 15, 10, 11, 14, 1 , 7 , 6 , 0 , 8 , 13,
    ],
    [
        4 , 11, 2 , 14, 15, 0 , 8 , 13, 3 , 12, 9 , 7 , 5 , 10, 6 , 1 ,
        13, 0 , 11, 7 , 4 , 9 , 1 , 10, 14, 3 , 5 , 12, 2 , 15, 8 , 6 ,
        1 , 4 , 11, 13, 12, 3 , 7 , 14, 10, 15, 6 , 8 , 0 , 5 , 9 , 2 ,
        6 , 11, 13, 8 , 1 , 4 , 10, 7 , 9 , 5 , 0 , 15, 14, 2 , 3 , 12,
    ],
    [
        13, 2 , 8 , 4 , 6 , 15, 11, 1 , 10, 9 , 3 , 14, 5 , 0 , 12, 7,
        1 , 15, 13, 8 , 10, 3 , 7 , 4 , 12, 5 , 6 , 11, 0 , 14, 9 , 2,
        7 , 11, 4 , 1 , 9 , 12, 14, 2 , 0 , 6 , 10, 13, 15, 3 , 5 , 8,
        2 , 1 , 14, 7 , 4 , 10, 8 , 13, 15, 12, 9 , 0 , 3 , 5 , 6 , 11,
    ]
]

DES_BITS_ROTATE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

def _des_permutation(data_bits : bitarray, type : DESPermutationType):
    match type:
        case DESPermutationType.IP:
            used_table = DES_IP_TABLE
        case DESPermutationType.PC1:
            used_table = DES_PC1_TABLE
        case DESPermutationType.PC2:
            used_table = DES_PC2_TABLE
        case DESPermutationType.P:
            used_table = DES_PERMUTATION_TABLE
        case DESPermutationType.IP_INVERSE:
            used_table = DES_IP_INVERSE_TABLE
        case DESPermutationType.EXPAND:
            used_table = DES_EXPANSION_TABLE
    output_bit_len = len(used_table)
    output_bits = bitarray(output_bit_len)
    for i in range(output_bit_len):
        bit_idx = used_table[i] - 1
        output_bits[i] = data_bits[bit_idx]

    return output_bits

def _des_substitution(data_bits : bitarray):
    output = bitarray(32)
    for i in range(8):
        start_bit = i * 6
        sub_outer_idx = (data_bits[start_bit] << 1) | data_bits[start_bit+5]
        sub_inner_idx = ba2int(data_bits[(start_bit+1):(start_bit+5)])
        output[(i*4):(i*4+4)] = int2ba(DES_SUBSTITUTION_TABLE[i][sub_outer_idx * 16 + sub_inner_idx], length=4)
    return output


def _des_encrypt_decrypt(data : Buffer, key : Buffer, decrypt : bool):
    encrypted_data = bytearray(len(data))
    encrypted_data[:] = data
    
    subkeys : list[bitarray] = []

    permuted_key = _des_permutation(bitarray(buffer=key), DESPermutationType.PC1)
    # print(permuted_key)
    permuted_key_l = permuted_key[:28]
    permuted_key_r = permuted_key[28:]
    for i in range(16):
        permuted_key_l.rotate(-DES_BITS_ROTATE[i])
        permuted_key_r.rotate(-DES_BITS_ROTATE[i])
        combined_key = bitarray(permuted_key_l)
        combined_key.extend(permuted_key_r)
        # print("pkey", combined_key)
        subkeys.append(_des_permutation(combined_key, DESPermutationType.PC2))
    # for i in range(16):
    #        print("i (", i, ") ", subkeys[i]) 
    if decrypt:
        subkeys.reverse()
    for data_start in range (0, len(encrypted_data), 8):
        chunk_bits = bitarray(encrypted_data[data_start:data_start + 8])
        initial_permutation = _des_permutation(chunk_bits, DESPermutationType.IP)
        data_permutation_l = bitarray(initial_permutation[:32])
        data_permutation_r = bitarray(initial_permutation[32:])
        for i in range(16):

            f_1 = subkeys[i] ^ _des_permutation(data_permutation_r, DESPermutationType.EXPAND)
            f_2 = _des_substitution(f_1)
            f_final = _des_permutation(f_2, DESPermutationType.P)
            new_l = bitarray(data_permutation_r)
            new_r = data_permutation_l ^ f_final
            data_permutation_l = new_l
            data_permutation_r = new_r
        final_combine = bitarray(data_permutation_r)
        final_combine.extend(data_permutation_l)
        final_permutation = _des_permutation(final_combine, DESPermutationType.IP_INVERSE)
        encrypted_data[data_start:data_start + 8] = bytearray(final_permutation)
    return encrypted_data

def des_encrypt(data : Buffer, key : Buffer):
    return _des_encrypt_decrypt(data, key, False)

def des_decrypt(data : Buffer, key : Buffer):
    return _des_encrypt_decrypt(data, key, True)


def pad_pkcs5(data : bytearray):
    pad_value = 8 - (len(data) % 8)
    return data + bytes([pad_value] * pad_value)

def unpad_pkcs5(data : bytearray):
    pad_value = data[-1]
    return data[:-pad_value]
