import random


def get_numbers_ticket(min: int, max: int, quantity: int) -> list[int]:
    """
    Генерує відсортований список унікальних випадкових чисел
    у заданому діапазоні.

    Args:
        min (int): Мінімальне можливе число, не менше 1.
        max (int): Максимальне можливе число, не більше 1000.
        quantity (int): Кількість чисел для вибору.

    Returns:
        list[int]: Відсортований список унікальних випадкових чисел.
                   Якщо параметри некоректні — повертає порожній список.
    """
    if min < 1 or max > 1000:
        return []

    if min > max:
        return []

    if quantity < 1 or quantity > (max - min + 1):
        return []

    numbers = random.sample(range(min, max + 1), quantity)

    return sorted(numbers)

lottery_numbers = get_numbers_ticket(1, 49, 6)
print("Ваші лотерейні числа:", lottery_numbers)