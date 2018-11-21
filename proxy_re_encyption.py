from pypbc import *

"""
基于双线性对的代理重加密方案实现
现有的双线性对的构造是基于椭圆曲线的，椭圆曲线上的点由坐标(x,y)表示。
因此Ｇ1、Ｇ2的输出是一个坐标，而GT是一个普通的群，其元素的表示是一个数。
"""


# 初始化线性对及公共参数
def params_init(qbits, rbits) -> "pairing, g, e(g,g)":
    # 指定椭圆曲线的种类为Type A, 需要两个参数来生成：ｒbits是Zr中阶数r的比特长度，qbits是Ｇ中阶数的比特长度。
    params = Parameters(qbits=qbits, rbits=rbits)
    pairing = Pairing(params)  # 构造一个线性映射
    g = Element.random(pairing, G2)  # 产生一个G2群中的元素
    bi = pairing.apply(g, g)  # 产生线性对e(g,g)
    return pairing, g, bi


def key_gen(pairing, g) ->"sk, pk":
    sk = Element.random(pairing, Zr)  # 从Zn中随机选取一个元素作为私钥
    pk = Element(pairing, G2, value=pow(g, sk))
    return sk, pk


class BiHE(object):
    def __init__(self, pairing, g, bi):
        self.pairing = pairing
        self.g = g
        self.bi = bi

    # 密钥生成算法，输入安全参数qbits和rbits，返回[sk, pk]
    def key_pairing(self) -> "sk, pk":
        sk, pk = key_gen(self.pairing, self.g)
        return [sk, pk]

    def raw_enc(self, pk, m) ->"[e(g,g)^(r*sk1), m*e(g,g)^r]":
        r = Element.random(self.pairing, Zr)
        c0 = self.pairing.apply(Element(self.pairing, G2, value=pow(self.g, r)), pk)  # e(g,g)^(r*sk1)
        c1 = Element(self.pairing, GT, value=m*pow(self.bi, r))  # m*e(g,g)^r
        return [c0, c1]

    def raw_dec(self, c, sk) -> "Dec(Enc(m))":
        m = c[1] * pow(pow(c[0], ~sk), Element(self.pairing, Zr, value=-1))
        return m

    def bi_enc(self, pk, m) -> "[pk^r, m*e(g,g)^r]":
        # 这里传入的m必须为GT中的元素
        r = Element.random(self.pairing, Zr)
        A = Element(self.pairing, G2, value=pow(pk, r))
        B = Element(self.pairing, GT, value=m*pow(self.bi, r))
        return [A, B]

    # 代理重加密阶段，利用2005年论文中的A second attempt
    def re_enc(self, c, re_key) -> "[e(g,g)^(r*sk), m*e(g,g)^r]":
        c[0] = self.pairing.apply(c[0], re_key)
        return [c[0], c[1]]

    @staticmethod
    def _add(c1, c2) -> "Enc(m1+m2)":
        c = [i*j for (i, j) in zip(c1, c2)]
        return c

    @staticmethod
    def _cMul(c, k) -> "Enc(k*m)":
        result = [c[i]**k for i in range(len(c))]
        return result
