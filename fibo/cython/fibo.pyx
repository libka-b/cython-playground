cdef double fibo_c(int n):
    cdef int i
    cdef double a = 0
    cdef double b = 1
    for i in range(n):
        a, b = a + b, b
    return a


cpdef fibo(int n):
    return fibo_c(n)
