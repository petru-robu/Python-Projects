v = [int(i) for i in input().split()]
print(v)

for i in range(len(v)):
    if v[i]%2 == 0 :
        print(i)
        for j in range (i):
            v[j] = v[j+1]
        v[i] = v[i]*2
        i+=1

print(v)
        
    