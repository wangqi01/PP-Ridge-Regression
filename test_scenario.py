from scenario import *

m = Element.random(pairing, Zr) # 随机生成一条消息m
M = Element(pairing, GT, value=pow(bi, m))  # e(g,g)^m


"""
基于线性对的原始加密方案测试
"""
cipher_m = CS.raw_enc(CS_pk, M)
plain_m = CS.raw_dec(cipher_m, CS_sk)
print(plain_m == M)

# 加法运算, Enc(m1)*Enc(m2)=Enc(m1+m2)
m1 = Element.random(pairing, Zr)
M1 = Element(pairing, GT, value=pow(bi, m1))
cipher_m1 = CS.raw_enc(CS_pk, M1)
m2 = Element.random(pairing, Zr)
M2 = Element(pairing, GT, value=pow(bi, m2))
cipher_m2 = CS.raw_enc(CS_pk, M2)
C = BiHE._add(cipher_m1, cipher_m2)
plain_add = CS.raw_dec(C, CS_sk)
print("----------------------------------- Enc(m1)*Enc(m2)=Enc(m1+m2): -----------------------------------")
print(plain_add == pow(bi, m1+m2))

# 乘以常数, Enc(m1)**k = Enc(k*m1)
k = Element.random(pairing, Zr)
c1 = BiHE._cMul(cipher_m1, k)
plain_km = CS.raw_dec(c1, CS_sk)
print("----------------------------------- Enc(m1)**k = Enc(k*m1): -----------------------------------")
print(plain_km == M1**k)


"""
代理重加密方案测试
"""
c = CS.bi_enc(CS_pk, M)  # 密文为[pk1^r, M*e(g,g)^r]
re_key = Element(pairing, G2, value=pow(ACS_pk, ~CS_sk))  # 重加密密钥pk2^(sk1^-1)
re_c = CS.re_enc(c, re_key)  # 重加密密文为[e(g,g)^(sk2*r), M*e(g,g)^r]
dec_M = CS.raw_dec(re_c, ACS_sk)
print("----------------------------------- 代理重加密结果: -----------------------------------")
print(dec_M == M)

raw_m1 = 100
# M1 = Element(pairing, GT, value=pow(bi, m1))
enc_m1 = encrypt(raw_m1)
raw_m2 = 200
# M2 = Element(pairing, GT, value=pow(bi, m2))
enc_m2 = encrypt(raw_m2)

tran_c1 = transfer(enc_m1, reKey)
tran_c2 = transfer(enc_m2, reKey)

# 测试加法
result_add = add(tran_c1, tran_c2)
m = decrypt(result_add)
print("----------------------------------- 代理重加密加法: -----------------------------------")
print(m == pow(bi, 300))

# 测试乘法
result_mul = mul(tran_c1, tran_c2)
M = decrypt(result_mul)
print("----------------------------------- 代理重加密乘法: -----------------------------------")
print(M == pow(bi, 20000))

# 计算向量点积
x1 = [1, 2, 3]
x2 = [2, 3, 4]
x1 = [encrypt(x1[i]) for i in range(len(x1))]  # [m-b, [DP_pk ^r, e(g,g)^b*e(g,g)^r]]
x2 = [encrypt(x2[i]) for i in range(len(x2))]
tran_x1 = [transfer(x1[i], reKey) for i in range(len(x1))]  # [m-b, [e(g,g)^(ACS_sk*r), e(g,g)^b*e(g,g)^r)]]
tran_x2 = [transfer(x2[i], reKey) for i in range(len(x2))]
result = vec_dot(tran_x1, tran_x2)
print("----------------------------------- 加密向量的点积运算: -----------------------------------")
print(decrypt(result) == pow(bi, 20))

# enc_x1 = [CS.raw_enc(ACS_pk, pow(bi, Element(pairing, Zr, value=x1[i]))) for i in range(len(x1))]
# print(enc_x1)
# result = vec_cdot(enc_x1, x2)
# print(decrypt(result) == pow(bi, 20))
