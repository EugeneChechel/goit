from __future__ import annotations

from datetime import datetime


def get_days_from_today(date: str) -> int | None:
    """
    Розраховує кількість днів між заданою датою та поточною датою.

    Args:
        date (str): Дата у форматі 'YYYY-MM-DD'.

    Returns:
        int | None: Кількість днів між заданою датою та сьогоднішньою.
                    Якщо дата в майбутньому — результат буде від'ємним.
                    Якщо формат дати неправильний — повертає None.
    """
    try:
        given_date = datetime.strptime(date, "%Y-%m-%d").date()
        today = datetime.today().date()

        difference = today - given_date
        return difference.days

    except ValueError:
        print("Помилка: неправильний формат дати. Використовуйте формат 'YYYY-MM-DD'.")
        return None

print(get_days_from_today("2021-10-09"))
print(get_days_from_today("2020-10-09"))
print(get_days_from_today("invalid-date"))