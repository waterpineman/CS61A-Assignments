a = 1
def g(h):
    a = 2
    return lambda y: a * h(a) * y
g(lambda y: a + y)(a)