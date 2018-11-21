from pypbc import *

# params = Parameters(qbits=512, rbits=160)
# # print(params)
#
# pairing = Pairing(params)
# # print(pairing)
#
# g = Element.random(pairing, G1)
# print(g)
#
# sk = Element.random(pairing, Zr)
# print(sk)
# pk = Element(pairing, G2, value=g**sk)
# print(pk)
#
# temp = Element(pairing, GT)
# print(temp)
#
# bi = pairing.apply(g, g)
# print(bi)
#
# hash_value = Element.from_hash(pairing, G1, "hashofmessage")
# print(hash_value)

params = Parameters(qbits=128, rbits=100)
pairing = Pairing(params)
P = Element.random(pairing, G1)
Q = Element.random(pairing, G2)
r = Element.random(pairing, Zr)
e = pairing.apply(P, Q)
print("params =", str(params))
print("pairing =", str(pairing))
print("P =", str(P))
PP = Element(pairing, G1, value=str(P))
print("PP =", str(PP))
assert P == PP
print("Q =", str(Q))
print("r =", str(r))
print("e =", str(e))
ee = Element(pairing, GT, value=str(e))
print("ee =", str(ee))
print("len(P) =", len(P))
print("P[0] = 0x%X" % (P[0]))
print("P[1] = 0x%X" % (P[1]))
assert len(P) == 2
print("len(Q) =", len(Q))
print("Q[0] = 0x%X" % (Q[0]))
print("Q[1] = 0x%X" % (Q[1]))
assert len(P) == 2
P0 = Element.zero(pairing, G1)
P1 = Element.one(pairing, G1)
print("P0 =", str(P0))
print("P1 =", str(P1))
Q0 = Element.zero(pairing, G2)
Q1 = Element.one(pairing, G2)
print("Q0 =", str(Q0))
print("Q1 =", str(Q1))
rP = P * r
print("rP =", str(rP))
