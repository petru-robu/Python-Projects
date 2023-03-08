import numpy as np
import math

DIG = 7

def roundUp(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

def det(A):
    return roundUp(np.linalg.det(A), DIG)

def rang(A):
    return np.linalg.matrix_rank(A)


class SistemLiniar:
    def __init__(self, mat_s, mat_t):
        self.matricea_sistemului = mat_s
        self.matricea_termenilor_liberi = mat_t
        self.matricea_extinsa = np.hstack((self.matricea_sistemului, self.matricea_termenilor_liberi))

        self.m, self.n = np.shape(self.matricea_sistemului)
        if self.m == self.n:
            self.det = det(self.matricea_sistemului)
        self.rang = rang(self.matricea_sistemului)

    
    def minor(self, i, j):
        return np.delete(np.delete(self.matricea_sistemului,i,axis=0), j, axis=1)
    
    def minoriPrincipali(self):
        res = list()
        if self.m < self.n:
            k = self.m - self.n

    def rezolva(self):  
        comp,incomp,deter,nedeter = False,False,False,False
        if self.m == self.n and self.det != 0:
            #COMPATIBIL DETERMINAT
            solutions = self.rezolvaCuCramer()
            return solutions
            
    
    def rezolvaCuCramer(self):
        res = list()
        for nec in range(self.n):
            mat_nec = np.copy(self.matricea_sistemului)
            for j in range(self.n):
                mat_nec[j][nec] = self.matricea_termenilor_liberi[j]

            d_nec = det(mat_nec)
            res.append(roundUp(d_nec/self.det, DIG))
        return res



s = SistemLiniar(np.array([[4, 3, 2], [-2, 2, 3], [3, -5, 2]]), np.array([[25], [-10], [-4]]))

print(s.matricea_sistemului, end="\n\n")
print(s.minor(0, 1), end ="\n\n")
print(s.matricea_extinsa, end="\n\n")
print(s.rezolva())


    