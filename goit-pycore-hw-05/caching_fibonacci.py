def caching_fibonacci():
    """
    Створює функцію fibonacci з кешем для збереження вже обчислених чисел Фібоначчі.
    """
    cache = {}

    def fibonacci(n):
        """
        Обчислює n-е число Фібоначчі з використанням рекурсії та кешу.
        """
        if n <= 0:
            return 0

        if n == 1:
            return 1

        if n in cache:
            return cache[n]

        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci


# Приклад використання
fib = caching_fibonacci()

print(fib(10))  # 55
print(fib(15))  # 610