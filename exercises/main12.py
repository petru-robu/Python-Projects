n = int(input())
v = [int(i) for i in input().split()]

minim = maxim = v[0]

for el in v:
    if el<minim:
        minim = el
    if el>maxim:
        maxim = el

print(minim, maxim)

