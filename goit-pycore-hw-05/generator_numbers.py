import re
from collections.abc import Callable, Generator


def generator_numbers(text: str) -> Generator[float, None, None]:
    """
    Знаходить у тексті всі дійсні числа, відокремлені пробілами,
    і повертає їх по одному як генератор.
    """
    pattern = r"(?<=\s)\d+\.\d+(?=\s)"

    for number in re.finditer(pattern, text):
        yield float(number.group())


def sum_profit(text: str, func: Callable[[str], Generator[float, None, None]]) -> float:
    """
    Обчислює загальну суму чисел у тексті,
    використовуючи передану функцію-генератор.
    """
    return sum(func(text))


text = (
    "Загальний дохід працівника складається з декількох частин: "
    "1000.01 як основний дохід, доповнений додатковими надходженнями "
    "27.45 і 324.00 доларів."
)

total_income = sum_profit(text, generator_numbers)
print(f"Загальний дохід: {total_income}")