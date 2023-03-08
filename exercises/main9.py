input()
v = [int(i) for i in input().split()]

for i in range(len(v)):
    if v[i] % v[len(v)-1] == 0 :
        print(v[i], end=" ")

