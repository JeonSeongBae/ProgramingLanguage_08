def sum(n):
    """
    :type n: int
    :rtype: int
    """
    # Fill out,  Use recursion
    if n == 1 :
        return 1
    else :
        return n + sum(n - 1)


def fibonacci(n):
    """:1 1 2 3 5 8
    :type n: int
    :rtype: int
    """
    # Fill out,  Use recursion
    if n <= 2:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def factorial(n):
    """
    :type n: int
    :rtype: int
    """
    if n == 1:
        return 1
    else:
        return n * factorial(n - 1)

# Fill out,  Use recursion


def decimal_to_binary(n):
    """:
    :type n: int
    :rtype: int
    """
    # Fill out,  Use recursion
    if n == 0:
        return 0
    else :
        return (n % 2) + decimal_to_binary(n / 2) * 10

def TestRecursionFunction():
    print factorial(10)
    print sum(100)
    print fibonacci(10)
    print decimal_to_binary(15)
TestRecursionFunction()
a, b = 1, 2
print a
print b