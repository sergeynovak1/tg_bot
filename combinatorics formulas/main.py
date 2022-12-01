from math import factorial


def Cb(n, k):
    if n >= k:
        return factorial(n)/(factorial(k)*factorial(n-k))
    raise Exception


def Cs(n, k):
    if n >= k:
        return factorial(n+k-1)/(factorial(k)*factorial(n-1))
    raise Exception


def Ab(n, k):
    if n >= k:
        return factorial(n)/factorial(n - k)
    raise Exception


def As(n, k):
    if n >= k:
        return n**k
    raise Exception


def Pb(n):
    if len(n) == 1:
        return factorial(n[0])
    raise Exception


def Ps(m):
    res = factorial(sum(m))
    for i in m:
        res /= factorial(i)
    return res
