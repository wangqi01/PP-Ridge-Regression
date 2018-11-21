from proxy_re_encyption import *

"""
测试基于代理重加密方案的正确性
"""

# 参数初始化
pairing, g, bi = params_init(1024, 180)

# 初始化DP/CS/DR,并生成公私钥
DP = BiHE(pairing, g, bi)
DP_sk, DP_pk = DP.key_pairing()
CS = BiHE(pairing, g, bi)
CS_sk, CS_pk = CS.key_pairing()
ACS = BiHE(pairing, g, bi)
ACS_sk, ACS_pk = ACS.key_pairing()
DR = BiHE(pairing, g, bi)
DR_sk, DR_pk = CS.key_pairing()

# DP生成代理密钥
reKey = Element(pairing, G2, value=pow(ACS_pk, ~DP_sk))

# 用一个字典来存储线性对及其指数的相关信息
dic_b = {}


# DP加密私有数据
def encrypt(m) -> "[m-b, [DP_pk ^r, e(g,g)^b*e(g,g)^r]]":
    m = Element(pairing, Zr, value=m)
    b = Element.random(pairing, Zr)
    B = Element(pairing, GT, value=pow(bi, b))  # e(g,g)^b
    dic_b[str(B)] = b  # 将该键值对存入字典
    e_b = DP.bi_enc(DP_pk, B)  # [DP_pk ^r, e(g,g)^b * e(g,g)^r]
    enc_m = [m-b, e_b]
    return enc_m


# CS进行密文转换, 传入DP加密的密文, 转化成ACS公钥加密的密文
def transfer(c, re_key) -> "[m-b, [e(g,g)^(ACS_sk*r), e(g,g)^b*e(g,g)^r)]]":
    c_1 = CS.re_enc(c[1], re_key)
    return [c[0], c_1]


# CS在转换后的密文上执行加法操作
def add(c1, c2) -> "Enc_ACS(e(g,g)^(m1+m2))":
    c0 = Element(pairing, GT, value=pow(bi, c1[0]+c2[0]))  # 将c0映射到相应的群上e(g,g)^(m1+m2-b1-b2)
    c0 = CS.raw_enc(ACS_pk, c0)  # 用线性对方案加密c0,[e(g,g)^(r*ACS_sk), e(g,g)^(m1+m2-b1-b2)*e(g,g)^r]
    c1 = BiHE._add(c1[1], c2[1])  # Enc(b1+b2)=[e(g,g)^(ACS_sk*(r1+r2)), e(g,g)^(b1+b2)*e(g,g)^(r1+r2)]
    c = BiHE._add(c0, c1)
    return c


# CS在转换后的密文上执行乘法操作,需与ACS交互一次
def mul(c1, c2) -> "Enc_ACS(e(g,g)^(m1*m2))":
    # 求前半部分密文为: [e(g,g)^(r*ACS_sk), e(g,g)^(m1*m2-b1*b2)*e(g,g)^r]
    c0 = CS._add(CS.raw_enc(ACS_pk, Element(pairing, GT, value=pow(bi, c1[0]*c2[0]))),
                 CS._add(CS._cMul(c2[1], c1[0]), CS._cMul(c1[1], c2[0])))
    # 若对c1[1],c2[1]进行解密,需求log得到b1和b2(这里采取在字典中进行查找),之后求 e(g,g)^(b1*b2)
    b1 = dic_b[str(ACS.raw_dec(c1[1], ACS_sk))]
    b2 = dic_b[str(ACS.raw_dec(c2[1], ACS_sk))]
    c1 = ACS.raw_enc(ACS_pk, Element(pairing, GT, value=pow(bi, b1*b2)))
    c = CS._add(c0, c1)  # [Enc_ACS(m1*m2 - b1*b2), Enc_ACS(b1*b2)]
    return c


# 计算两个密文向量的乘积
def vec_dot(c1, c2):
    # 对应元素相乘,再相加
    result = mul(c1[0], c2[0])
    for i in range(1, len(c1)):
        result = CS._add(result, mul(c1[i], c2[i]))
    return result


# 计算一个密文向量与一个明文向量的乘积
def vec_cdot(c_vec, p_vec):
    result = CS._cMul(c_vec[0], p_vec[0])
    for i in range(1, len(c_vec)):
        result = CS._add(result, CS._cMul(c_vec[i], p_vec[i]))
    return result


# DR执行解密,用发给ACS的临时密钥
def decrypt(c):
    m = ACS.raw_dec(c, ACS_sk)
    return m
