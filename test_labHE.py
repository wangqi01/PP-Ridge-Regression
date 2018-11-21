from labHE import *
from phe import paillier

"""
labHE方案测试
"""

DEFAULT_KEYSIZE = 1024  # security parameter
public_key, private_key = paillier.generate_paillier_keypair(n_length=DEFAULT_KEYSIZE)
Alice = LabHE(public_key, private_key)
m0 = 100
m1 = 200
c1 = Alice.raw_enc(m0)
d1 = Alice.raw_dec(c1)
# print(d1 == m0)
c2 = Alice.raw_enc(m1)

# 测试加法
E_a = Alice.raw_add(c1, c2)
D_a = Alice.raw_dec(E_a)
print(D_a == m0+m1)

# 测试乘法
E_m = Alice.raw_mul(c1, c2)
D_m = Alice.dec_mul(E_m)
print(D_m == m0*m1)
