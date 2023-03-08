# # a = 7
# #
# # print(a)
# #
# # a = "dani"
# #
# # print(a)
# #
# # # liste
# #
# # x = [] # lista vida
# # y = list() # tot lista vida
# #
# # x.append(7) # push la final
# # x.append("dani")
# # print(x)
# #
# # x = []
# #
# # for i in range(1,101):
# #     x.append(i)
# #
# # print(x)
# #
# x = [i for i in range(0,101)]
# #
# # print(x)
# #
# # for i in range(len(x)):
# #     print(i) # merge de la 0 la size-1
# # len(x) este 100
# # for i in range(0, len(x) + 1, 2):
# #     print(i)

# print(x[3:8])


# mat = [[1 for i in range(5)] for j in range(5)]

# print(mat[2])

# print(f"maximul in lista {x[2:8]} este {max(x[2:8])}") # f de la format


# def f(a: int, b: int):
#     print(a+b)
    
# # sa se afiseze primele 30 nr prime (hint cu functie de verif nr prim)
# # from math import sqrt
# import math
# def estePrim(a: int):
#     if a < 2:
#         return False
#     if a == 2:
#         return True
#     if a % 2 == 0:
#         return False
#     for i in range(3, int(math.sqrt(a))+1, 2):
#         if a % i == 0:
#             return False
#     return True

# found = 0
# prime = []
# k = 3

# while(found < 30):
#     if estePrim(k):
#         found+=1
#         prime.append(k)
#     k+=1

# print(prime)


a = [int(x) for x in input("Lista a = ").split(" ")]
#b = [int(x) for x in input("Lista b = ").split(" ")]

# for i in range(len(a)):
#     for j in range(i+1, len(a)):
#         if a[i] > a[j]:
#             a[i], a[j] = a[j], a[i]

# print(a)

a = 1
b = a
a = 3
print(b)

'''
-Tupluri
-Sortari predefinite
'''