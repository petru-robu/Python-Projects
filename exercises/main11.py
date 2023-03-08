n = int(input("Introduceti nr: "))
v = [int(i) for i in input().split()]

i = 0
j = len(v) - 1

while i < j:
    print(v[i], v[j], end=" ")
    i+=1
    j-=1

if len(v) % 2 == 1:
    print(v[int(len(v)/2)])

