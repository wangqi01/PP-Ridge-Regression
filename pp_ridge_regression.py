import numpy as np
import pandas as pd
from sklearn.utils import shuffle
from scenario import *
import time

# 先进行数据的预处理,读取数据等操作
data = pd.read_excel('./data.xlsx')
data = shuffle(data)    # 打乱数据的顺序
data_train = np.array(data[:])
data_x = data_train[:700, :8]     # 取10条数据
data_y = data_train[:700, -2:-1]
data_X = data_x*100     # 将原始数据放大100倍,变成整数
data_Y = data_y*100
m_row = len(data_X)  # 训练数据条数
n_col = 8  # 属性个数

enc_X = []
enc_XT = []
enc_Y = []

"""
DP对数据进行加密, 对X矩阵进行逐元素加密
"""
start = time.time()

enc_X = [[encrypt(int(data_X[i][j])) for j in range(n_col)] for i in range(m_row)]
print("----------------------------------- 加密的X矩阵: -----------------------------------")
# print(enc_X)
print()
enc_Y = [encrypt(int(data_Y[i])) for i in range(m_row)]
print("----------------------------------- 加密y矩阵: -----------------------------------")
# print(enc_Y)
print()

end = time.time()
t_DP = end - start
print("DP encrypt data cost time: {}s".format(t_DP))

"""
CS对密文进行重加密
"""
start = time.time()

start1 = time.time()

for row in range(m_row):
    for col in range(n_col):
        enc_X[row][col] = transfer(enc_X[row][col], reKey)
    enc_Y[row] = transfer(enc_Y[row], reKey)
print("------------------------------------ 重加密X和y: -----------------------------------")
# print(enc_X, enc_Y)
# print()
enc_XT = [[enc_X[i][j] for i in range(m_row)] for j in range(n_col)]  # X转置的加密

end1 = time.time()
print("CS re-encryption cost time: {}".format(end1 - start1))

"""
CS进行矩阵运算
"""

# 求XTX, 此时已扩大了10^4倍
enc_XTX = [[vec_dot(enc_XT[i], enc_XT[j]) for j in range(n_col)] for i in range(n_col)]
print("------------------------------------ XTX 的密文: -----------------------------------")
# print(enc_XTX)
# print()

# print("解密验证:", [[decrypt(enc_XTX[i][j]) == decrypt(vec_dot(enc_XT[i], enc_XT[j]))
#                  for i in range(n_col)] for j in range(n_col)])

# 生成矩阵 lam*I, 取lam=0.01, 需扩大10^4倍, 并将其转化成列表形式
mat_lam = np.identity(n_col)*100
list_lam = mat_lam.tolist()

# 加密 lam*I, 直接采取线性对的加密方式
enc_list_lam = [[CS.raw_enc(ACS_pk, Element(pairing, GT, value=pow(bi, int(mat_lam[i][j]))))
                 for j in range(n_col)] for i in range(n_col)]
# print(enc_list_lam)
# print(decrypt(enc_list_lam[0][0]) == pow(bi, Element(pairing, Zr, value=2000)))
# print(decrypt(enc_list_lam[0][1]) == pow(bi, Element(pairing, Zr, value=0)))

# 计算XTX+lam*I的密文, 此时对应的明文为原始的10^4倍
enc_A = [[BiHE._add(enc_XTX[i][j], enc_list_lam[i][j]) for i in range(n_col)] for j in range(n_col)]
print("------------------------------------- XTX+lam*I 的密文: ---------------------------------")
# print(enc_A)
# print()

# 生成一个随机整数方阵, 每个元素取1~100的整数, 并加密
R = np.random.randint(1, 100, size=[n_col, n_col])
R1 = R
R = [[int(R[i, j]) for j in range(n_col)] for i in range(n_col)]
RT = [[R[i][j] for i in range(n_col)] for j in range(n_col)]
enc_R = [[CS.raw_enc(DR_pk, Element(pairing, GT, value=pow(bi, R[i][j]))) for i in range(n_col)] for j in range(n_col)]
# print("------------------------------------- R 的密文: ---------------------------------")
# print(enc_R)
# print()

# 计算(XTX+lam*I)*R的密文, 其中R为明文矩阵, XTX+lam*I为密文矩阵
enc_AR = [[vec_cdot(enc_A[i], RT[j]) for j in range(n_col)] for i in range(n_col)]
# print("----------------------------- (XTX+lam*I)*R 的密文: ------------------------------")
# print(enc_AR)
# print()

# 生成维度为n_col*1的随机矩阵r,并计算A*r的密文
r = np.random.randint(1, 100, size=[n_col, 1])
r1 = r
r = [int(r[i, 0]) for i in range(n_col)]
# print("--------------------------------------- r 的密文: ---------------------------------")
# enc_r = [CS.raw_enc(ACS_pk, Element(pairing, GT, value=pow(bi, r[i]))) for i in range(n_col)]
# print(enc_r)
# print()
# print("------------------------------------- (-r*10^6) 的密文: ---------------------------------")
# enc_r1 = [CS.raw_enc(DR_pk, Element(pairing, GT, value=pow(bi, -r[i]*10**6))) for i in range(n_col)]
# # print(enc_r1)
# print()
enc_Ar = [vec_cdot(enc_A[i], r) for i in range(n_col)]
print("-------------------------------- (XTX+lam*I)*r 的密文: -----------------------------")
# print(enc_Ar)
# print()
print()

# 计算b=XTy
enc_b = [vec_dot(enc_XT[i], enc_Y) for i in range(n_col)]
print("-------------------------------------- XTy的密文: -----------------------------------")
# print(enc_b)
print()

# 计算 b+A*r的密文
enc_b_Ar = [BiHE._add(enc_Ar[i], enc_b[i]) for i in range(n_col)]
print("----------------------------------- XTy+A*r 的密文: ---------------------------------")
# print(enc_b_Ar)
print()

end = time.time()
t_CS = end - start
print("CS cost time: {}s".format(t_CS))

print("------------------------------------- (-r*10^6) 的密文: ---------------------------------")
enc_r1 = [CS.raw_enc(DR_pk, Element(pairing, GT, value=pow(bi, -r[i]*10**6))) for i in range(n_col)]
# print(enc_r1)
print()

"""
ACS执行解密及之后的一些运算
"""
start = time.time()

# 解密AR, 得到的实际上是e(g,g)的幂次方
plain_AR = [[decrypt(enc_AR[i][j]) for i in range(n_col)] for j in range(n_col)]
print("------------------------------------- 解密 A*R:(得到的是e(g,g)^(AR)) ---------------------------------")
# print(plain_AR)
print()
# str_AR = [[str(plain_AR[i][j]) for j in range(n_col)] for i in range(n_col)]

# 解密b+A*r
plain_b_Ar = [decrypt(enc_b_Ar[i]) for i in range(n_col)]
print("------------------------------------- 解密 b+A*r:(得到的是e(g,g)^(b+Ar)) ---------------------------------")
# print(plain_b_Ar)
print()
# str_b_Ar = [str(plain_b_Ar[i]) for i in range(n_col)]

end = time.time()
t1_ACS = end - start

str_AR = [[str(plain_AR[i][j]) for j in range(n_col)] for i in range(n_col)]
str_b_Ar = [str(plain_b_Ar[i]) for i in range(n_col)]