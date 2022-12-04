from random import getrandbits, seed

class HashFinder:
    def __init__(self, t=5):
        self.m = bytearray(32)
        self.t = t
        self.int_lookup = b'\x00\x01\x02\x03\x04\x05\x06'

    def find(self, sd=17, pt=True):
        seed(sd)
        # make original one
        self.makeinput()
        if pt:
            print("Message : ", end='')
            self.hexprint(self.m)
        o = self.hash()
        if pt:
            print("Hash : ", end='')
            self.hexprint(o)

        # make intermediate output
        self.tweak()
        o_i = self.hash()

        # change B and make collision pair
        self.change_B(o, o_i)
        if pt:
            print("Message : ", end='')
            self.hexprint(self.m)
        o2 = self.hash()
        if pt:
            print("Hash : ", end='')
            self.hexprint(o2)
        if not pt:
            return o, o2

    def makeinput(self):
        m = bytearray(16)
        for i in range(4):
            m[i] = getrandbits(8)
        m.extend(m)
        self.m = m

    def tweak(self):
        # just change the last bit of the first byte of A and B
        self.m[0] = self.m[0] ^ 0x01
        self.m[16] = self.m[16] ^ 0x01

    def change_B(self, o, o_i):
        newb = self.xor(o, self.xor(o_i, self.m[16:]))
        self.m[20:] = newb[4:]

    def hexprint(self, bytearr):
        print(" ".join(list(map(hex, bytearr))))

    def xor(self, A, B):
        return bytearray(a ^ b for (a, b) in zip(A, B))

    def hash(self):
        # initialization
        a0 = self.m[:16]
        b0 = self.m[16:]
        a_now = a0[:]
        b_now = b0[:]

        # round loop
        for i in range(self.t):
            rb = b_now[:4]
            if i != self.t - 1:
                a_next = self.h_round(rb, a_now)
                b_next = self.h_round(self.int_lookup[i:i+4], a_now)
                a_now = a_next[:]
                b_now = b_next[:]
            else:
                a_t = self.h_round_prime(rb, a_now)

        return self.xor(a_t, self.xor(a0, b0))
    def hash_print(self):
        # initialization
        a0 = self.m[:16]
        b0 = self.m[16:]
        a_now = a0[:]
        b_now = b0[:]

        # round loop
        for i in range(self.t):
            rb = b_now[:4]
            if i != self.t - 1:
                print(f"round {i}")
                self.hexprint(rb)
                self.hexprint(a_now)
                self.hexprint(b_now)
                a_next = self.h_round(rb, a_now)
                b_next = self.h_round(self.int_lookup[i:i+4], a_now)
                a_now = a_next[:]
                b_now = b_next[:]
            else:
                print(f"round {i}")
                self.hexprint(rb)
                self.hexprint(a_now)
                self.hexprint(b_now)
                a_t = self.h_round_prime(rb, a_now)
                self.hexprint(a_t)
                print("result")
                result = self.xor(a_t, self.xor(a0, b0))
                self.hexprint(result)

        return result

    def h_round(self, rb, X):
        Y = bytearray(16)
        Y[:4] = self.xor(self.F(rb, X[:4]), X[4:8])
        Y[4:8] = X[8:12]
        Y[8:12] = X[12:16]
        Y[12:16] = X[:4]
        return Y

    def h_round_prime(self, rb, X):
        Y = bytearray(16)
        Y[:4] = X[4:8]
        Y[4:8] = self.xor(self.F(rb, X[:4]), X[8:12])
        Y[8:12] = X[12:16]
        Y[12:16] = X[:4]
        return Y

    def F(self, rb, X):
        p = self.xor(rb, X)
        q = self.s_box(p)
        y = self.mixcol(q)
        return y

    def s_box(self, p):
        sbox = [
            0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
            0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
            0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
            0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
            0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
            0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
            0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
            0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
            0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
            0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
            0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
            0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
            0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
            0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
            0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
            0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
        ]
        q = bytearray(4)
        for i in range(4):
            q[i] = sbox[p[i]]
        return q

    def mixcol(self, q):
        y = bytearray(4)
        y[0] = self.mult(q[0], 2) ^ self.mult(q[1], 3) ^ self.mult(q[2], 1) ^ self.mult(q[3], 1)
        y[1] = self.mult(q[0], 1) ^ self.mult(q[1], 2) ^ self.mult(q[2], 3) ^ self.mult(q[3], 1)
        y[2] = self.mult(q[0], 1) ^ self.mult(q[1], 1) ^ self.mult(q[2], 2) ^ self.mult(q[3], 3)
        y[3] = self.mult(q[0], 3) ^ self.mult(q[1], 1) ^ self.mult(q[2], 1) ^ self.mult(q[3], 2)
        return y

    def mult(self, byte, num):
        if num == 1:
            return byte
        elif num == 2:
            return self.times(byte)
        else:
            return self.times(byte) ^ byte

    def times(self, byte):
        poly = 0x1b # 0001 1011
        if byte & 0x80: # if 1st digit is 1
            return ((byte << 1) ^ poly) & 0xff
        else:
            return byte << 1
