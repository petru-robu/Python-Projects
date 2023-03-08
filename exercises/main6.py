n = input()
n = int(n)

for i in range(n):
    for k in range(i):
        print(" ", end="")
    for j in range(n):
        print('*', end="")
    print()

for i in range(n-2, -1, -1):
    for k in range(i):
        print(" ", end="")
    for j in range(n):
        print('*', end="")
    print()

