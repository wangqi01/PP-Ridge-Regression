import random

"""
labHE加密方案实现,
这里我们利用phe库中的Paillier加密方案实现
"""


class LabHE(object):
    def __init__(self, pk, sk):
        self.pk = pk
        self.sk = sk

    def raw_enc(self, m) -> "Enc(m) = [m-b, Enc(b)]":
        b = random.SystemRandom().randrange(2**499, 2**500)     # 生成一个500位的随机数
        e_b = self.pk.encrypt(b)
        enc_m = [m-b, e_b]
        return enc_m

    def raw_dec(self, c) -> "m = Dec(Enc(m))":
        b = self.sk.decrypt(c[1])
        m = (c[0] + b) % self.pk.n
        return m

    def raw_add(self, c1, c2) -> "Enc(m1+m2) = [m1+m2-b1-b2, Enc(b1+b2)]":
        c = [i+j for (i, j) in zip(c1, c2)]
        return c

    def raw_mul(self, c1, c2) -> "[Enc(m1*m2 - b1*b2), Enc(b1*b2)]":
        c0 = self.pk.encrypt(c1[0]*c2[0]) + c2[1]*c1[0] + c1[1]*c2[0]  # Enc(m1*m2 - b1*b2)
        c1 = self.pk.encrypt(self.sk.decrypt(c1[1])*self.sk.decrypt(c2[1]) % self.pk.n)
        return [c0, c1]

    def dec_mul(self, c):
        m = self.sk.decrypt(c[0]+c[1])
        return m
