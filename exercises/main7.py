n = int(input())

l = n*3 - 2

for i in range(n-1):
    for j in range(n - i - 1):
        print("#", end="")
    for j in range(l - 2*(n - i - 1)):
        print("*", end="")
    for j in range(n - i - 1):
        print("#", end="")
    print()

for i in range(n):
    for j in range(l):
        print("*", end="")
    print()

for i in range(n-1):
    for j in range(i + 1):
        print("#", end="")
    for j in range(l - 2*(i+1)):
        print("*", end="")
    for j in range(i + 1):
        print("#", end="")
    print()

    