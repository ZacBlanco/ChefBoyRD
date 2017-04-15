'''Test module docstring'''

def hello():
    '''Prints "hello". Always returns 1 '''
    print("Hello")
    return 1

def fib(num):
    '''Returns the fibonacci numbers:
    Extended description:

    Args:
        num (int): Integer representing the fibonacci number

    Returns:
        int: The fibonacci number

    Throws:
        TypeError: When argument is not an int
    '''
    if not isinstance(num, int):
        raise TypeError("Number must be int")
    return 0 if num == 0 else (1 if num == 1 else fib(num-1) + fib(num-2))
