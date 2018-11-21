from pp_ridge_regression import *

"""
明文上进行岭回归训练
"""
# 明文上计算 A=XTX+lam*I, lam=0.01, 并验证密文
x = np.mat(data_x)
mat_lam = np.mat(np.identity(n_col)*0.01)
A = x.T * x + mat_lam
# print(A)
A1 = A.tolist()  # 转化成列表
# print(A1)
# print("验证XTX+lam*I:", [[decrypt(enc_A[i][j]) == Element(pairing, GT, value=pow(bi, round(A1[i][j]*10**4)))
#                         for i in range(n_col)] for j in range(n_col)])
# print()

# 计算 b=XTy, 并验证密文
b = x.T * np.mat(data_y)
b1 = b.tolist()
# print(b1)
# print("验证XT*y:", [decrypt(enc_b[i]) == pow(bi, round(b1[i][0]*10**4)) for i in range(n_col)])
print()
b_Ar = b + A*r1
list_b_Ar = b_Ar.tolist()
# print(list_b_Ar)
print()

# 求解 w = A^-1 * b
w = A.I * b
w = [w[i, 0] for i in range(n_col)]
print("------------------------------------- 明文下的模型: ---------------------------------")
print(w)
print()

# 计算并验证AR的密文
R1 = np.mat(R1)
AR = A*R1
AR1 = AR.tolist()
# print([pow(bi, round(AR1[i][j])) for j in range(n_col) for i in range(n_col)])
# print(AR)
# print("验证A*R:",[decrypt(enc_AR[i][j]) == pow(bi, round(AR1[i][j]*10**4)) for i in range(n_col) for j in range(n_col)])
print()

# 建立一个字典, 用来存放线性对元素及其本原
dict_find = {}
for i in range(n_col):
    for j in range(n_col):
        dict_find[str_AR[i][j]] = round(AR1[i][j]*10**4)
    dict_find[str_b_Ar[i]] = round(list_b_Ar[i][0])
# print(dict_find)


"""ACS进行密文运算"""

start = time.time()

# 求(AR)^-1,将运算后的元素扩大10^10倍后取整, 为实际结果的10^6倍
inv_AR = np.mat(AR.I*10**10).astype(int)
print("AR的逆:")
# print(inv_AR)
print()

# 计算(AR)^-1 *(b+Ar)
temp = np.mat(inv_AR * b_Ar).astype(int)
temp1 = [int(temp[i, 0]) for i in range(n_col)]

# 计算 enc(A^-1 *b+r) = enc(R)^temp
enc_M = [vec_cdot(enc_R[i], temp1) for i in range(n_col)]
print("Enc(A^-1 * b + r):")
# print(enc_M)

enc_w = [BiHE._add(enc_M[i], enc_r1[i]) for i in range(n_col)]

end = time.time()
t2_ACS = end - start

print("ACS cost time: {}s".format(t1_ACS + t2_ACS))

"""
DR最对最终结果执行解密操作:
"""
plain_w = [DR.raw_dec(enc_w[i], DR_sk) for i in range(n_col)]
print("-------------------w的明文:-----------------------------")
print(plain_w)
# print([pow(bi, int(round(w[i]*10**6))) for i in range(n_col)])
